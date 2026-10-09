#!/usr/bin/env python3
"""Synthesize a sparse, ancient-toned ambient bed (low drone + breath) with ffmpeg only.

Copyright-free by construction. It is a placeholder-quality bed: swap in a real
score any time with `build.py --score yourtrack.wav`.
"""
import argparse
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seconds", type=int, default=610)
    ap.add_argument("--out", default="build/score.wav")
    a = ap.parse_args()
    d = a.seconds
    # D minor-ish open drone: D2, A2, D3, F3, A3 with slow independent tremolos, plus soft filtered noise "breath"
    tones = [(73.42, 0.50, 0.10), (110.00, 0.35, 0.13), (146.83, 0.30, 0.11), (174.61, 0.12, 0.17), (220.00, 0.10, 0.12)]
    inputs, labels = [], []
    for i, (f, vol, trem) in enumerate(tones):
        inputs += ["-f", "lavfi", "-i", f"sine=frequency={f}:sample_rate=48000:duration={d}"]
        labels.append(f"[{i}:a]volume={vol},tremolo=f={trem}:d=0.55[t{i}]")
    n = len(tones)
    inputs += ["-f", "lavfi", "-i", f"anoisesrc=color=pink:sample_rate=48000:amplitude=0.25:duration={d}"]
    labels.append(f"[{n}:a]bandpass=f=420:width_type=h:w=500,tremolo=f=0.15:d=0.9,volume=0.10[breath]")
    mix = "".join(f"[t{i}]" for i in range(n)) + "[breath]"
    graph = ";".join(labels) + f";{mix}amix=inputs={n + 1}:normalize=0,lowpass=f=1200,aecho=0.8:0.6:900|1700:0.35|0.25," \
        f"aformat=channel_layouts=stereo,afade=t=in:d=6,loudnorm=I=-26:TP=-3[out]"
    cmd = ["ffmpeg", "-y", "-v", "error"] + inputs + ["-filter_complex", graph, "-map", "[out]", "-t", str(d), a.out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-1500:])
    print("wrote", a.out)


if __name__ == "__main__":
    main()
