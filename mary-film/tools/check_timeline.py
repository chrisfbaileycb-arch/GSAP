#!/usr/bin/env python3
"""Sanity-check timeline.json: total runtime, voice-line pacing, overlaps, asset coverage.

Usage: python3 tools/check_timeline.py [--assets assets]
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORDS_PER_SEC = 2.3  # slow, measured narration; real TTS output is measured by build.py when files exist


def load(path=ROOT / "timeline.json"):
    return json.loads(Path(path).read_text())


def est_len(text):
    return max(1.0, len(re.findall(r"\b[\w']+\b", text)) / WORDS_PER_SEC)


def find_asset(folder, needle):
    needle = needle.lower()
    for p in sorted(Path(folder).glob("*")):
        if p.is_file() and needle in p.name.lower():
            return p
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets", default=str(ROOT / "assets"))
    ap.add_argument("--timeline", default=str(ROOT / "timeline.json"))
    args = ap.parse_args()
    tl = load(args.timeline)
    t = 0.0
    lines = []
    problems = 0
    have = {"clip": 0, "still": 0, "slate": 0, "card": 0}
    missing = []
    for it in tl["items"]:
        have[it["type"]] = have.get(it["type"], 0) + 1
        if it["type"] in ("clip", "still"):
            folder = Path(args.assets) / ("clips" if it["type"] == "clip" else "stills")
            if not find_asset(folder, it["match"]):
                missing.append(it["id"])
        for v in it.get("vo", []):
            s = t + v["at"]
            lines.append((s, s + est_len(v["text"]), v["id"], it["id"]))
        t += it["dur"]
    lines.sort()
    for a, b in zip(lines, lines[1:]):
        if b[0] < a[1] - 0.05:
            print(f"OVERLAP  {a[2]} ({a[3]}) ends ~{a[1]:.1f}s but {b[2]} ({b[3]}) starts {b[0]:.1f}s")
            problems += 1
    total = t
    voice = sum(b - a for a, b, *_ in lines)
    print(f"items: {sum(have.values())}  ({', '.join(f'{k}={v}' for k, v in have.items())})")
    print(f"runtime: {total:.0f}s = {int(total // 60)}:{int(total % 60):02d}   target {tl['target_seconds']}s")
    print(f"voice lines: {len(lines)}  est. speech {voice:.0f}s ({100 * voice / total:.0f}% of runtime)")
    if abs(total - tl["target_seconds"]) > 30:
        print("WARNING runtime is more than 30s from target")
        problems += 1
    slates = [it["id"] for it in tl["items"] if it["type"] == "slate"]
    print(f"shots still to generate ({len(slates)}): {', '.join(slates)}")
    if missing:
        print(f"clip/still files not found in {args.assets} ({len(missing)}): {', '.join(missing)}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
