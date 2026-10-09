# What Was Given Me - the Mary film (10-minute build kit)

A first-person memory film based on the Gospel of Mary, assembled from the clips, stills and plan in your
Drive folder **MaryMag Movie**, plus a new imagined prologue for the pages that did not survive.

`python3 tools/build.py` always produces a complete, correctly timed rough cut (placeholder slates stand in
for any shot not yet generated), so you can watch the pacing now and swap real footage in as it arrives.

## What exists today

| Piece | State |
|---|---|
| Story, 39 scenes, characters, continuity rules | In your Drive (`universe_bible.json`, `segment_prompts_v42.json`); mapped into `timeline.json` |
| Existing footage | 25 clips cover scenes 1-22 and 25-27 (matched by filename); 5 stills cover scenes 35-39 |
| Missing footage | **16 shots**: 7 prologue shots (P1-P7) + scenes 23, 24, 28-34. Prompts in `prompts/new_shots.md` |
| Prologue for the lost opening | Written (`timeline.json` P1-P7 + 2 cards). Clearly labelled on screen as imagined |
| Voices (5 characters, 41 lines) | Script done. Audio **not** recorded yet: `tools/tts.py` |
| Music | Synthesized ambient bed (`tools/make_score.py`), copyright-free; replace with a real score if you like |
| Captions | `build/film.srt` generated automatically |
| Runtime | 10:12 (target 10:00) |

## How to finish it

1. **Get your media next to this folder.** In Drive, download the `MaryMag Movie` folder (and
   `files-2026-08-22.zip`, which very likely holds the full-resolution originals - only ~11 full-size stills are
   loose in the folder). Put videos in `assets/clips/` and images in `assets/stills/`. Names don't need
   changing: shots are found by the words in their long filenames (`match` in `timeline.json`).
2. `python3 tools/check_timeline.py` - shows which shots are found and which are still missing.
3. **Generate the 16 missing shots** in whatever tool made the originals, using `prompts/new_shots.md`
   (same continuity text as your bible). Drop the files in `assets/clips/`, then in `timeline.json` change that
   item from `"type": "slate"` to `"type": "clip"` and add a `"match"`.
4. **Voices:** `OPENAI_API_KEY=... python3 tools/tts.py --provider openai` (or `--provider elevenlabs`).
   Character direction is in `voices.json`. Audition and re-do single lines with `--only L010,L011 --force`.
   Existing clips keep mouths closed, so any voice drops in with no lip-sync.
5. `python3 tools/build.py --draft` for a fast check, then `python3 tools/build.py` for 1080p -> `build/film.mp4`.
6. **Upload** `film.mp4` + `film.srt` to YouTube. Turn on the **altered/synthetic content** disclosure (the
   imagery and voices are AI-generated and realistic), and keep the on-screen credit.

Requirements: `ffmpeg` and `python3` (no pip packages).

## About the Anthropic API key

Anthropic's API reads and writes text and understands images. It does not produce voices or video, so it can't
replace steps 3-4. It is useful for: rewriting or tightening this script, new shot prompts, and a continuity check
(send sampled frames + the character descriptions and ask whether wardrobe or the Saviour's face rule drifted).
None of that is wired in yet; say the word and I'll add it.

## Honest notes

- **The "lost pages"**: the surviving Coptic text is missing its opening pages (and a gap in the middle). Nothing
  here claims to be that text; the prologue is an original reflection on teachings the surviving pages do contain
  (all things are joined and return to their root; sin arises when we forget this; "be of good courage"), and the
  film says so on screen. Dialogue lines in the main story follow the surviving text; please check them against
  the translation you want to credit before publishing, since translations are often under copyright.
- **Pacing**: 41 beats in 284 s was a montage. This cut gets to ~10 minutes by slowing clips (0.5-0.8x, frame
  blended), holding frames and letting lines breathe, about 54% of the runtime is speech. If it feels slow,
  shorten `dur` values in `timeline.json`; if it feels rushed, lengthen them.
- **Not tested here**: real TTS calls (no keys/network in the build environment) and your real footage (it can't
  be pulled through the Drive connector - the files are far too large). The assembly code was tested with
  synthetic clips, stills, voice and the placeholder cut.
- This folder lives inside the GSAP fork only because that was the repo available in the session; it is
  self-contained and can be moved to its own repo. The `lenis` and `react-bits` forks are web UI libraries and
  aren't used for video.
