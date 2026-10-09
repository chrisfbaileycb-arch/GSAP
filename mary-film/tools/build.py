#!/usr/bin/env python3
"""Assemble the film from timeline.json with ffmpeg.

  python3 tools/build.py            # full quality 1920x1080 -> build/film.mp4
  python3 tools/build.py --draft    # 640x360 quick animatic for checking pacing
  python3 tools/build.py --no-vo    # skip voice mix (score only)

Missing clips/stills become on-screen slates describing the shot, so a complete
rough cut always renders. Missing voice files are skipped and listed.
Also writes build/film.srt (captions) from the voice lines.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("ffmpeg failed:\n" + " ".join(map(str, cmd)) + "\n" + r.stderr[-2000:])
    return r


def probe_dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(path)], capture_output=True, text=True)
    return float(r.stdout.strip())


def find_asset(folder, needle):
    needle = needle.lower()
    for p in sorted(Path(folder).glob("*")):
        if p.is_file() and needle in p.name.lower():
            return p
    return None


def textfile(work, name, text):
    # drawtext reads from a file, which sidesteps all of its quoting/escaping traps
    p = work / f"{name}.txt"
    p.write_text(text)
    return str(p)


def lookup(it, assets):
    if it["type"] not in ("clip", "still"):
        return None
    return find_asset(assets / ("clips" if it["type"] == "clip" else "stills"), it["match"])


def seg_cmd(it, out, W, H, fps, assets, work):
    dur = it["dur"]
    fade = min(0.7, dur / 4)
    fades = f"fade=t=in:st=0:d={fade},fade=t=out:st={dur - fade}:d={fade}"
    common = ["-r", str(fps), "-pix_fmt", "yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-an", str(out)]
    size = f"{W}x{H}"
    fs = max(18, H // 20)
    src = lookup(it, assets)
    if it["type"] == "clip" and src:
        speed = it.get("speed", 1.0)
        fit = (f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
               f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:black,tpad=stop_mode=clone:stop_duration={dur},{fades}")
        if speed < 1.0:
            vf = f"setpts=PTS/{speed},minterpolate=fps={fps}:mi_mode=blend,{fit}"
        else:
            vf = f"fps={fps},{fit}"
        return ["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vf", vf, "-t", str(dur)] + common
    if it["type"] == "still" and src:
        frames = int(dur * fps)
        zp = (f"scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase,crop={W * 2}:{H * 2},"
              f"zoompan=z='min(1+0.0006*on,1.12)':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={size}:fps={fps},{fades}")
        return ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(src), "-vf", zp, "-t", str(dur)] + common
    # cards and slates (placeholders for anything not yet generated)
    if it["type"] == "card":
        tf = textfile(work, it["id"], it["text"])
        vf = (f"drawtext=fontfile={FONT}:textfile={tf}:fontsize={fs}:fontcolor=0xE8DCC0:"
              f"x=(w-text_w)/2:y=(h-text_h)/2:line_spacing={fs // 3},{fades}")
    else:
        desc = it.get("desc") or it.get("match", "")
        head = f"SHOT {it['id']}  -  NOT YET GENERATED" if it["type"] == "slate" else f"SHOT {it['id']}  -  FILE NOT FOUND"
        body = re.sub(r"(.{1,52})(\s+|$)", r"\1\n", desc).strip()
        tf1 = textfile(work, it["id"] + "_h", head)
        tf2 = textfile(work, it["id"] + "_b", body)
        vf = (f"drawtext=fontfile={FONT_SANS}:textfile={tf1}:fontsize={fs * 3 // 4}:fontcolor=0xC9884A:x=(w-text_w)/2:y=h*0.30,"
              f"drawtext=fontfile={FONT}:textfile={tf2}:fontsize={fs * 4 // 5}:fontcolor=0xD8D0BC:"
              f"x=(w-text_w)/2:y=h*0.42:line_spacing={fs // 3},{fades}")
    return ["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"color=c=0x0b0a09:s={size}:r={fps}:d={dur}",
            "-vf", vf, "-t", str(dur)] + common


def srt_time(s):
    ms = int(round(s * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft", action="store_true")
    ap.add_argument("--no-vo", action="store_true")
    ap.add_argument("--timeline", default=str(ROOT / "timeline.json"))
    ap.add_argument("--assets", default=str(ROOT / "assets"))
    ap.add_argument("--out", default=str(ROOT / "build"))
    ap.add_argument("--score", default=None, help="music bed (default: build/score.wav, generated if absent)")
    args = ap.parse_args()

    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg not found on PATH")
    tl = json.loads(Path(args.timeline).read_text())
    assets, out = Path(args.assets), Path(args.out)
    work = out / "work"
    work.mkdir(parents=True, exist_ok=True)
    W, H = (640, 360) if args.draft else (1920, 1080)
    fps = tl.get("fps", 24)

    segs, t, vo_events, cues = [], 0.0, [], []
    report = {"slates": [], "no_voice": []}
    for it in tl["items"]:
        seg = work / f"{it['id']}.mp4"
        run(seg_cmd(it, seg, W, H, fps, assets, work))
        segs.append(seg)
        if it["type"] == "slate" or (it["type"] in ("clip", "still") and not lookup(it, assets)):
            report["slates"].append(it["id"])
        for v in it.get("vo", []):
            f = next((assets / "vo" / f"{v['id']}.{e}" for e in ("mp3", "wav", "m4a", "ogg")
                      if (assets / "vo" / f"{v['id']}.{e}").exists()), None)
            start = t + v["at"]
            if f and not args.no_vo:
                d = probe_dur(f)
                vo_events.append((start, f))
            else:
                d = max(1.0, len(re.findall(r"\b[\w']+\b", v["text"])) / 2.3)
                report["no_voice"].append(v["id"])
            who = "" if v["who"] == "MARY" else f"{v['who'].title()}: "
            cues.append((start, start + d, who + v["text"]))
        t += it["dur"]
    total = t

    srt = [f"{i}\n{srt_time(a)} --> {srt_time(b)}\n{txt}\n" for i, (a, b, txt) in enumerate(cues, 1)]
    (out / "film.srt").write_text("\n".join(srt))

    lst = work / "list.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in segs))
    video = work / "video.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(video)])

    score = Path(args.score) if args.score else out / "score.wav"
    if not score.exists():
        run([sys.executable, str(ROOT / "tools" / "make_score.py"), "--seconds", str(int(total) + 5), "--out", str(score)])
    final = out / ("film_draft.mp4" if args.draft else "film.mp4")
    tail = f"afade=t=out:st={total - 5}:d=5,atrim=0:{total}"
    if vo_events:
        inputs = ["-i", str(video), "-i", str(score)]
        parts, labels = [], []
        for i, (st, f) in enumerate(vo_events):
            inputs += ["-i", str(f)]
            ms = int(st * 1000)
            parts.append(f"[{i + 2}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[v{i}]")
            labels.append(f"[v{i}]")
        parts.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=longest,volume=1.6,apad=whole_dur={total},asplit=2[vo_a][vo_sc]")
        parts.append("[1:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.55[bed]")
        parts.append("[bed][vo_sc]sidechaincompress=threshold=0.02:ratio=8:attack=40:release=900[ducked]")
        parts.append(f"[ducked][vo_a]amix=inputs=2:normalize=0:duration=longest,{tail}[aout]")
    else:
        inputs = ["-i", str(video), "-i", str(score)]
        parts = [f"[1:a]volume=0.8,{tail}[aout]"]
    run(["ffmpeg", "-y", "-v", "error"] + inputs + ["-filter_complex", ";".join(parts),
         "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", str(total), str(final)])

    d = probe_dur(final)
    print(f"wrote {final}  duration {d:.1f}s ({int(d // 60)}:{int(d % 60):02d})  captions: {out / 'film.srt'}")
    print(f"placeholder slates in this cut ({len(report['slates'])}): {', '.join(report['slates']) or 'none'}")
    print(f"voice lines without audio ({len(report['no_voice'])}): {', '.join(report['no_voice']) or 'none'}")


if __name__ == "__main__":
    main()
