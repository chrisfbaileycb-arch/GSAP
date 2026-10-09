# Prompts for the 16 shots that still need generating

Paste the **STYLE BLOCK** first (or into your tool's global/style field), then the per-shot prompt.
Rules are taken from your own universe bible so new shots match the 25 clips you already have.

## STYLE BLOCK (use with every shot)

> Photorealistic cinematic drama, first-century Judea, natural light only, shallow depth of field, fine 35mm film grain, muted earth palette (ochre, olive, whitewash, warm amber), slow deliberate camera movement, no text, no modern objects. **All characters keep their mouths closed and still** (voices are added in post). The Saviour is only ever a softly backlit silhouette in a doorway or light-flare; his face is never sharply resolved or front-lit. First-person feeling: the camera is Mary's eyes whenever possible.

## CHARACTERS (copy exact wording for continuity)

- **Mary** - renowned, weathered, beautiful Judean woman, late 40s. Sun-weathered olive skin, dark hair under a simple linen head-wrap, luminous eyes holding grief and quiet authority, plain undyed linen robe with a rope belt, no jewelry, bare sandaled feet. Lived-in and real, not idealised, not a soft-glow icon.
- **Peter** - weathered first-century fisherman, early 50s, greying short beard, coarse brown wool tunic, rough grey-brown mantle over one shoulder, weathered hands. Guarded, intense eyes; the most volatile and protective of the group.
- **Andrew** - first-century disciple, early 40s, faded blue-grey linen tunic, undyed wool shawl over one shoulder, short dark beard, younger and more anxious-looking than Peter.
- **Levi** - first-century disciple, late 30s, simple ochre-tan tunic, no mantle, clean-shaven or very short beard, calm steady bearing; the group's quiet moral centre.
- **Upper room** - modest first-century upper room: whitewashed plaster walls, low wooden table, woven floor mats, a single east window pouring low morning light thick with dust, an open doorway at the far end leading to a sunlit street.

## PROLOGUE - the "lost pages" (imagined; shown after the on-screen card saying so)

**P1 (12s)** Slow aerial-feeling push over flat-roofed whitewashed rooftops at dawn, low haze, warm first light. A woman's silhouette (Mary) stands at a rooftop edge, linen head-wrap moving slightly in the wind, looking out. Quiet, reflective.

**P2 (9s)** Extreme close-up of Mary's weathered hands kneading dough on a rough wooden board, flour dust rising through a shaft of morning light. Slow, tender, everyday. No face.

**P3 (9s)** From behind: Mary walks a narrow whitewashed lane carrying a clay water jar on her shoulder; a sunlit opening glows at the far end of the lane. Camera follows at a slow steady distance.

**P4 (10s)** Macro: a single oil-lamp flame in a dark room, the wick trembling, warm amber against deep black, tiny dust motes drifting. Almost still.

**P5 (9s)** Macro: a seed resting in a weathered palm, then a slow dissolve to pale roots threading through dark soil. Soft natural light, tender.

**P6 (18s)** Wide, a courtyard at dusk. Seated listeners in a loose circle; the Teacher, a backlit silhouette against a doorway of warm light, speaks with gentle gestures. His face is never visible. Camera is low among the seated, Mary's point of view.

**P7 (11s)** Slow lateral pan across listening faces in lamplight: Peter, Andrew, Levi, Mary's own hand in the foreground. Mouths closed, eyes lifted, moved but not yet afraid.

## MISSING SCENES IN THE MAIN STORY

**S23 - Seven powers of wrath (18s, ABSTRACT)** Abstract non-literal space, full-bleed, no bars. Deep blacks with a single small point of warm amber light holding steady in the centre. Seven distinct bands of harsh reddish light flare and layer across the frame in rapid overlapping succession, like jealous fire. **Never any figures, faces, creatures, demons or architecture**; only colour, texture and light. Fine grain.

**S24 - Rest in silence (18s, ABSTRACT)** Same abstract space. All light and shadow settle into one soft, steady, warm glow that fills the frame, calm and unmoving. Pure visual silence and peace after the ascent. Very slow, almost imperceptible bloom.

**S28 - Peter accuses (14s)** Wide shot in the upper room. Peter rises abruptly from the low table, agitated, turning the room's doubt into open accusation against Mary (she is seated, small in frame, still). Andrew and the others shift uneasily. Mouths closed. Morning dust-light from the east window.

**S29 - Do you think I made this up? (16s)** Close on Mary's face, composed no longer: tears finally break through, running down weathered cheeks, hurt but not backing down, chin lifted slightly. Mouth closed. Slow push-in. Shallow focus; Peter a blurred figure at the edge of frame.

**S30 - The room holds its breath (10s)** Wide, the whole room frozen after the confrontation: Mary weeping but upright, Peter standing rigid, Andrew looking away in shame, Levi watching closely from where he sits apart. Static camera, dust hanging in the light. Tension unresolved.

**S31 - Levi stands (10s)** Medium shot: Levi rises from where he sat apart and calm, and moves toward the centre of the room with quiet, deliberate authority. Camera tilts slowly up with him.

**S32 - You have always been hot-tempered (14s)** Two-shot easing into a slow, low push-in on Levi as he faces Peter directly, calm but unyielding. The other disciples behind him fall out of focus; the room's earlier accusers reduced to shadow while Levi alone stays sharp.

**S33 - Peter's silence (10s)** Close on Peter, the fight draining out of him. He looks down, chastened. A long held beat; his hands, rough and weathered, loosen.

**S34 - Let us be ashamed (12s)** Close on Levi turning to address the whole group, steady and warm, calling them back to their purpose. Soft side-light from the east window.

## Generating them one at a time

1. Generate the still first if your tool is image-to-video; check Mary's wardrobe and that the Saviour is never front-lit.
2. Keep each clip 5-8 seconds; the timeline slows clips to 0.5-0.8x and holds the last frame to fill the slot.
3. Save as `assets/clips/<anything containing the 'match' words>.mp4` and add a `match` + `type: "clip"` to that item in `timeline.json` (replace `type: "slate"`).
