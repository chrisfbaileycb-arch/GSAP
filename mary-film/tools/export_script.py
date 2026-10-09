#!/usr/bin/env python3
"""Export timeline.json as a readable shooting script: script/FULL_SCRIPT.md (re-run after editing the timeline)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def clock(s):
    return f"{int(s // 60)}:{int(s % 60):02d}"


def main():
    tl = json.loads((ROOT / "timeline.json").read_text())
    out = [f"# {tl['title']} - shooting script", "",
           "Generated from `timeline.json` by `tools/export_script.py`. Edit the timeline, not this file.", ""]
    t, act = 0.0, None
    for it in tl["items"]:
        if it["act"] != act:
            act = it["act"]
            out += [f"## {act}", ""]
        status = {"clip": "footage exists", "still": "still exists", "slate": "**TO GENERATE**", "card": "title card"}[it["type"]]
        out.append(f"### {clock(t)}  {it['id']}  ({it['dur']}s, {status})")
        if it["type"] == "card":
            out += ["", "> " + it["text"].replace("\n", "  \n> "), ""]
        else:
            out += ["", it.get("desc") or f"Footage matching: _{it['match']}_", ""]
        for v in it.get("vo", []):
            out.append(f"- **{v['who']}** (+{v['at']}s) [{v['id']}]: {v['text']}")
        out.append("")
        t += it["dur"]
    out.append(f"Total runtime: {clock(t)}")
    dest = ROOT / "script" / "FULL_SCRIPT.md"
    dest.write_text("\n".join(out) + "\n")
    print("wrote", dest)


if __name__ == "__main__":
    main()
