# JSW 100% automation plan (locked 2026-09-05)

One brain (JSW AI) + droplet org. No extra bots until posting is live.
`go_live` stays OFF until Sam flips it after a week that looks right.

## Lanes

| Lane | What | Engine |
|---|---|---|
| SFW social (TikTok/IG/YT/FB/Reddit) | stills + talking clips | Higgsfield → Ayrshare |
| X tease | lingerie/bikini stills + carousels, **no nudity** | Zen Collabs/Photoshoot/Variations → Ayrshare (twitter) |
| Fanvue | explicit stills, PPV, DMs/upsell | Zen (undress/Variations) → Fanvue API (not Ayrshare) |
| NSFW video | parked until natural motion is solved | Zen i2v later |

## Already built on the droplet

- `content_engine.py` — concept → caption → approvals queue (Grok)
- `ayr_poster.py` — publish approved/scheduled posts via Ayrshare; gated by `go_live`
- `fanvue_client.py` — OAuth PKCE, tokens in vault; scopes include `write:post`, `write:media`, `read:chat` (no `write:chat` yet)
- Approvals UI, playbooks, bios, `go_live` flag
- Per-persona Ayrshare profile keys in vault

## Target loop (once accounts are up)

1. **Create** — Zen/Higgsfield keepers → Variations carousels (X) / undress (Fanvue) → Face Swap if needed → library folders (sfw / x / fanvue)
2. **Queue** — content_engine picks format + caption in persona voice → approvals (auto-approve after trust week, or Sam spot-check)
3. **Post** — ayr_poster for social/X on schedule; Fanvue poster daemon for Fanvue posts/PPV
4. **Engage** — inbox daemon: like/comment on niche posts; reply to comments in voice; never break character; AI-disclosed in bio already
5. **Fanvue money** — welcome message, chat replies, PPV upsells, tip thanks (needs `write:chat` + chat read loop)
6. **Measure** — collector metrics → scoreboard → next day's concepts

## Gaps to close (order)

1. **Accounts** — Ayrshare profiles for all 6; Fanvue OAuth for 5 remaining (Sam ID verify); handles filled
2. **Creative factory** — Collabs+Face Swap recipe locked (Miami); Variations + undresser under test; Sienna face plate upgrade; NSFW video parked
3. **Fanvue write path** — post media + caption via API; add `write:chat` scope if Fanvue allows; welcome + upsell scripts in playbooks
4. **Engagement daemon** — Ayrshare/history + platform comment APIs where available; rate limits; human-sounding cadence
5. **Inbox/DM router** — Fanvue chats + social DMs → persona reply → optional PPV offer rules
6. **Scheduler** — week calendar per couple; X lingerie vs Fanvue explicit split; no cross-posting nudes to SFW
7. **Flip `go_live`** — only after a dry week of queued content Sam likes

## Safety

- `go_live != 1` → poster holds
- No minors / no real-person impersonation
- X = no nudity; Fanvue = explicit OK
- Approvals on until Sam trusts the week
- One credit wallet on Zen; don't auto-buy packs

## Bots

Stay on one JSW assistant with per-platform rules. Optional later: couple-scoped chats. Do not fan out new bots for TikTok vs Fanvue.

## Night of 2026-09-05 — progress

- **Creative factory locked for stills:** Collabs (body keepers + prompt) → Face Swap Seedream 5 Pro Face 2K → Variations 3:4 2K ×5 (X) → Image Editor Flux Klein LoRA Undress Woman V3 (Fanvue). Miami Nights is the proof path (`gabriela_valentina_collab_v2_faceswap.png` → `miami_variations_1-5.png` + `miami_fanvue_undress_1.png`).
- **Video under test:** research + experiment order in `NSFW_VIDEO_RESEARCH.md` (Seedance Pro Fast kiss first, then Wan 2.7 Spicy; angled near-kiss still if both fake). No credit spend in the research write-up itself.
- **Accounts still next:** Ayrshare profiles + remaining Fanvue OAuth / ID verify remain the launch blocker after creative.
- **`go_live` off.** Do not post. Do not flip the flag overnight.


## Night of 2026-09-05 — kiss i2v results (03:17 ET)

Clips generated on Zen Video Generator (no login wall, no safety refusal):

| File | Engine | Credits | Specs |
|---|---|---|---|
| `miami_kiss_seedance_v1.mp4` | Seedance 2.0 Spicy | 13 | ~5s, 834×1112 |
| `miami_kiss_wan_v1.mp4` | Wan 2.7 Spicy | 13 | ~5s, 830×1108 |

Source still: `miami_fanvue_undress_1.png` (Miami undress keeper).

Notes:
- Seedance Pro Fast was not available in the UI path used overnight; fell back to Seedance 2.0 Spicy + Wan 2.7 Spicy.
- Prior Sam verdict on similar engines: rejected as “super AI” / waxy — these need Sam review in the morning.
- Account inventory written: `ACCOUNT_INVENTORY_2026-09-05.md` (go_live OFF; Ayrshare keys missing Sienna+Charlotte; only Sienna handles visible).
- Next if both kiss clips fail realism: Collabs near-kiss still → Face Swap → i2v (experiment 3 from NSFW_VIDEO_RESEARCH.md). Park stock face-swap unless Zen fails completely.
- Do not post. Do not flip go_live.


## Night of 2026-09-05 — near-kiss stills (~03:45 ET)

Exp 3 after Seedance/Wan undress kiss rejects: Collab+FaceSwap+Undress done.
- Keepers: `miami_nearkiss_collab_v1.png`, `miami_nearkiss_faceswap.png`
- Undress pose loss: `miami_nearkiss_undress.png` (front-facing) — skip for kiss i2v
- i2v queued from faceswap with fixed-camera prompt


## Night of 2026-09-05 — near-kiss i2v (~03:55 ET)

- Saved: `miami_nearkiss_kiss_seedance_v1.mp4` (Seedance 2.0 Mini Spicy, 13 cr)
- Source: `miami_nearkiss_faceswap.png` (not undress)
- Sam review in morning. Early undress kiss clips (`miami_kiss_seedance_v1.mp4`, `miami_kiss_wan_v1.mp4`) are rejects.

## 2026-09-08 — stills-only launch
Sam: near-kiss Seedance not realistic enough. Park NSFW video. Proceed toward go-live with stills (X tease + Fanvue undress) once accounts are ready. Do not require NSFW video for first live week.


## 2026-09-09 — Org Studio vs Zen LoRA gap

Org `/api/zen/templates` + tool list: **no `flux_klein_lora`** (404 upstream). Undress search returns 0. Zen **app** still shows LoRA cards including **Undress Woman V3**.

Workaround: generate Undress in Zen app; save to library only (no Fanvue publish; only Sienna Fanvue-approved for live).

Claude TODO on droplet: map Flux Klein LoRA tool correctly in Org Studio; fix upload UI stuck on `uploading…` (missing `.catch()` / timeout).
