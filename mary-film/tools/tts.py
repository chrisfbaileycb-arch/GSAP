#!/usr/bin/env python3
"""Render every voice line in timeline.json to assets/vo/<LINE_ID>.mp3.

  OPENAI_API_KEY=...      python3 tools/tts.py --provider openai
  ELEVENLABS_API_KEY=...  python3 tools/tts.py --provider elevenlabs
  python3 tools/tts.py --provider openai --only L010,L011     # re-do specific lines
  python3 tools/tts.py --list                                  # just show the lines

NOTE: not exercised in the build session (no keys / no outbound access there). Request
shapes follow each provider's public docs; if a call fails, the error body is printed.
Anthropic's API has no speech output, which is why this uses a separate voice provider.
Lines that already exist on disk are skipped unless --force.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def post(url, headers, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json", **headers})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} from {url}: {e.read()[:500]!r}")


def openai_tts(text, voice_cfg):
    key = os.environ.get("OPENAI_API_KEY") or sys.exit("set OPENAI_API_KEY")
    return post("https://api.openai.com/v1/audio/speech", {"Authorization": f"Bearer {key}"}, {
        "model": "gpt-4o-mini-tts", "voice": voice_cfg["openai_voice"], "input": text,
        "instructions": voice_cfg["direction"], "response_format": "mp3"})


def elevenlabs_tts(text, voice_cfg):
    key = os.environ.get("ELEVENLABS_API_KEY") or sys.exit("set ELEVENLABS_API_KEY")
    vid = voice_cfg["elevenlabs_voice_id"]
    if vid == "FILL_ME":
        sys.exit("fill elevenlabs_voice_id in voices.json first")
    return post(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128", {"xi-api-key": key},
                {"text": text, "model_id": "eleven_multilingual_v2",
                 "voice_settings": {"stability": 0.6, "similarity_boost": 0.8, "style": 0.2}})


PROVIDERS = {"openai": openai_tts, "elevenlabs": elevenlabs_tts}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", choices=PROVIDERS)
    ap.add_argument("--only", help="comma-separated line ids")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    tl = json.loads((ROOT / "timeline.json").read_text())
    voices = json.loads((ROOT / "voices.json").read_text())
    lines = [v for it in tl["items"] for v in it.get("vo", [])]
    if a.only:
        want = set(a.only.split(","))
        lines = [v for v in lines if v["id"] in want]
    if a.list or not a.provider:
        for v in lines:
            print(f"{v['id']}  {v['who']:8} {v['text']}")
        return
    outdir = ROOT / "assets" / "vo"
    outdir.mkdir(parents=True, exist_ok=True)
    for v in lines:
        dest = outdir / f"{v['id']}.mp3"
        if dest.exists() and not a.force:
            print("skip", dest.name)
            continue
        dest.write_bytes(PROVIDERS[a.provider](v["text"], voices[v["who"]]))
        print("wrote", dest.name)


if __name__ == "__main__":
    main()
