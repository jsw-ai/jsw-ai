# NSFW video research — JSW (night of 2026-09-05)

Goal: realistic **kiss** i2v from Miami Fanvue undress still, Zen-first.  
Do **not** spend Zen credits in this note itself; parent agent runs experiments.  
Do **not** post. Do **not** flip `go_live`.

**Primary still:** `/workspace/hf-test/zen/miami_fanvue_undress_1.png`  
(Source keeper: `/workspace/hf-test/zen/gabriela_valentina_collab_v2_faceswap.png` → Image Editor Flux Klein LoRA **Undress Woman V3**)

---

## A) Zen-native path (priority)

### Seedance Pro Fast — Zen's recommended kissing engine

Official guide: https://zencreator.pro/ai-university/guides/ai-kissing-video-seedance

| Why | Detail |
|---|---|
| Unrestricted on Zen | Kissing / intimate couple prompts not blocked (unlike Kling) |
| Cost | ~$0.20 / clip; 5s generates in ~30s — iterate cheaply |
| Motion strengths | Head tilt, eye close, lip contact, hair shift |

**Official kiss tips (follow exactly):**

1. **Physical action, not emotion.** Prefer `tilts head and leans in to kiss on the lips, eyes closing` over `romantic kiss`.
2. **One action per clip.** No kiss-then-hug-then-pull-away in one 5s shot.
3. **Duration:** start **5s**; use **10s** only if lean-in → kiss needs room.
4. Optional Face Swap on the still **before** i2v if identities need a refresh; Face Swap again after if faces melt.

**Recipe for JSW kiss:**

```
finished undress still (miami_fanvue_undress_1.png)
  → (optional) Face Swap Seedream 5 Pro Face 2K if faces look soft
  → Video Generator → Seedance Pro Fast
  → motion-only prompt, Enhance OFF
  → 5s first, 720p
```

**Starting-frame problem:** Official workflow wants the couple **already slightly turned toward each other / near-kiss pose**. Our Miami undress is **camera-facing** (lingerie-on-bed → same pose nude). Options:

- Accept a **front lean-in** kiss (may look weaker / more awkward).
- Or generate a **near-kiss / profile-toward-each-other** still first via Collabs + short kiss-pose prompt (or Variations), Face Swap both, Undress if needed, **then** Seedance Pro Fast i2v.

### Wan 2.7 Spicy — explicit i2v backup on Zen

- Built for explicit motion; use **motion-only** prompts; **Enhance prompt OFF**.
- Prior JSW lingerie test (`sienna_camille_collab_v1.mp4`): waxy skin, bras vanished, mangled fingers — do not reuse that “re-describe the photo + Enhance ON” recipe.
- **Undressed kiss** may behave differently (no wardrobe to strip). Worth one controlled 5s test on the same Miami undress still.
- Constrain: one action, micro-to-moderate lean/kiss, negatives for hands/warping/plastic skin.

### Identity / quality guardrails (carry from SKILL)

- Animate **finished** stills only (undress keeper, not a draft Collab).
- Prompt = motion only; do not re-name wardrobe or re-describe the photo.
- If faces melt mid-clip → Face Swap on best frame or re-still → retry.
- Kling family = SFW / censored — skip for Fanvue kiss.

---

## B) Backup path if Zen stays fake

**Legal / ethics (hard rule):** Prefer **motion transfer / character replace on AI or licensed stock ONLY**.  
Never real performers without commercial rights + explicit consent — **illegal nonconsensual deepfakes**.  
Do **NOT** scrape OnlyFans / Fanvue of real people for plates or faces.

| Option | Notes |
|---|---|
| Zen Video-to-Video `replace_nsfw` / `animate_nsfw` | Use **if available** in app; character replace onto AI body plates only |
| Imagera-style character replacement | AI or licensed stock motion → swap JSW faces/bodies |
| FaceFusion / Deep-Live-Cam | **OWN AI body plates only** — never real-person OF footage |
| Stock face-swap | Park until Sam wakes unless Zen fails completely |

**Best JSW backup (still Zen credits, better pose):**

```
Collabs (or template) with kiss / near-kiss prompt
  → Face Swap both (Seedream 5 Pro Face 2K)
  → optional Undress Woman V3 if Fanvue explicit needed
  → Seedance Pro Fast i2v
```

This matches Zen's own guide (pose first → Face Swap → Seedance Pro Fast) and fixes the camera-facing Miami frame issue.

---

## C) Recommended overnight experiment order (parent agent)

1. **Seedance Pro Fast** kiss from `/workspace/hf-test/zen/miami_fanvue_undress_1.png` (5s, motion-only, Enhance OFF).
2. **Wan 2.7 Spicy** same still (5s, motion-only, Enhance OFF) — one clip only unless clearly better.
3. **If both look fake:** generate a **near-kiss / profile-toward-each-other** still via Collabs (+ Undress if needed), Face Swap, then i2v again with Seedance Pro Fast.
4. **Park stock / FaceFusion face-swap** until Sam wakes unless Zen fails completely.

### Copy-paste starter prompts (kiss)

Seedance Pro Fast (front lean-in from current still):

```
two women close-up, she tilts her head and leans in to kiss the other on the lips,
eyes closing softly, gentle hand on cheek, slow intimate motion, warm soft light,
shallow depth of field, keep same faces, smooth slow motion
```

If near-kiss still is ready:

```
close-up couple already nearly touching, soft kiss on the lips with slight head tilt,
eyes closing, hair barely moving, fixed camera, warm bedroom light, keep same faces
```

Negatives (paste):  
`flicker, ghosting, warping, plastic skin, over-smooth, bad hands, deformed fingers, extra limbs, face melt, identity change, watermark, text, logo`

---

## Status

- Stills factory locked (see SKILL + AUTOMATION_PLAN).
- Video: research ready; **experiments not run in this write-up** (no Zen credit spend here).
- `go_live` remains OFF. No posting.


## Overnight results (2026-09-05 ~03:17 ET)

| Clip | Engine | Credits | Review |
|---|---|---|---|
| `miami_kiss_seedance_v1.mp4` | Seedance 2.0 Spicy (Pro Fast unavailable in UI) | 16 | **Reject** — waxy; kiss present; faces melt on extreme zoom ~00:04 |
| `miami_kiss_wan_v1.mp4` | Wan 2.7 Spicy | 13 | **Reject** — waxy; kiss present; faces/bodies melt on zoom ~00:03+ |

Credits ~819 → ~790. Camera-facing undress still + aggressive zoom = failure mode.

**Next (exp 3):** Collabs near-kiss / profile-toward-each-other still → Face Swap → Undress if needed → i2v (prefer Seedance Pro Fast if visible; else Seedance 2.0 Spicy with **fixed camera / no zoom** in prompt).


## Exp 3 stills (2026-09-05 ~03:45 ET)

| File | Notes |
|---|---|
| `miami_nearkiss_collab_v1.png` | Genuine near-kiss / profile-facing Collab |
| `miami_nearkiss_faceswap.png` | Face Swap kept close/profile (smiling) — **use this for i2v** |
| `miami_nearkiss_undress.png` | Undress Woman V3 **broke pose** → front-facing twins — do NOT i2v from this |

Credits after stills: ~778. Next: Seedance Pro Fast (or 2.0 Spicy) i2v from faceswap with **fixed camera / no zoom**.


## Exp 3 i2v (2026-09-05 ~03:55 ET)

| Clip | Engine | Credits | Notes |
|---|---|---|---|
| `miami_nearkiss_kiss_seedance_v1.mp4` | Seedance **2.0 Mini Spicy** (Pro Fast / 2.0 Spicy not listed) | 778→765 | From `miami_nearkiss_faceswap.png`; 5s 720p; computerUse preview: clear kiss, stable faces. Independent videoReview: **Accept** — clear kiss, faces distinct/no melt, no zoom glitch; still slightly waxy/stiff (Sam morning call). |

Lesson: camera-facing undress + zoom = melt. Near-kiss still + fixed camera = much better start. Undress after near-kiss still loses pose — undress for Fanvue stills only, not as kiss i2v source unless Undress preserves profile.

## Sam verdict 2026-09-08
`miami_nearkiss_kiss_seedance_v1.mp4`: **not realistic enough to post** (better than melts, still not live-ready). NSFW video parked. Launch path: **stills-only** until motion quality is fixed.
