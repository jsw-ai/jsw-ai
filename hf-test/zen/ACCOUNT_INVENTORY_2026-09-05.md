# JSW Social / Fanvue Account Readiness Inventory

**Checked:** 2026-09-05 03:00 UTC-4  
**Org:** `https://206-81-3-238.sslip.io/org/`  
**Scope:** read-only. No posts, approvals, go-live changes, OAuth connections, or passwords entered.

## Go-live

- **Live posting: OFF — holding (safety gate).** Seen on Approvals.
- No go-live control was changed.
- Approval queue is populated; approved items are not publishing while live posting is off. Fanvue is described by the UI as publishing through its own service.

## Visible global integrations

- **Fanvue one-time connection: connected.** Fanvue OAuth Client ID and Client Secret are shown as stored in the vault; an `oauth_tokens` entry is also present. The UI does not expose a per-model Fanvue account/ID-verification flag.
- **X:** Consumer Key and Consumer Secret shown as stored.
- **Ayrshare:** profile keys shown as stored for **Camille, Gabriela, Madison, and Valentina** only. No Sienna or Charlotte Ayrshare profile key was visible. The vault showed instructions pointing to the Ayrshare dashboard, but no direct Ayrshare platform/link inventory was exposed without opening another service.

## Per-model summary

| Model | Handles visible in profile | Fanvue connected? (visible evidence) | Ayrshare / platform evidence visible |
|---|---|---|---|
| Sienna Blake | TikTok `@siennablake0320`; X `@BlakeSienn39605` | Global connection is connected; **Fanvue folder: 5**; 0 Fanvue subs. Per-model connection flag not shown. | No Ayrshare key visible. Profile/calendar visibly uses Instagram, TikTok, and X destinations; not proof of Ayrshare linkage. |
| Camille | None shown | Global connection is connected; **Fanvue folder: 0**; 0 Fanvue subs. Per-model flag not shown. | Ayrshare profile key stored. Calendar shows Instagram and TikTok items; no explicit linked-platform list. |
| Charlotte | None shown | Global connection is connected; **Fanvue folder: 0**; 0 Fanvue subs. Per-model flag not shown. | No Ayrshare key visible. Calendar shows Instagram, X, and TikTok items; no explicit linked-platform list. |
| Madison | None shown | Global connection is connected; **Fanvue folder: 0**; 0 Fanvue subs. Per-model flag not shown. | Ayrshare profile key stored. Calendar shows Instagram and TikTok items; no explicit linked-platform list. |
| Gabriela | None shown | Global connection is connected; **Fanvue folder: 0**; 0 Fanvue subs. Per-model flag not shown. | Ayrshare profile key stored. No scheduled platform items visible. |
| Valentina | None shown | Global connection is connected; **Fanvue folder: 0**; 0 Fanvue subs. Per-model flag not shown. | Ayrshare profile key stored. No scheduled platform items visible. |

## Gaps blocking 100% automation

1. Live posting remains OFF; the approval queue still needs human review and the UI shows rejected/pending items.
2. Ayrshare profile-key coverage is only visible for 4/6 models; Sienna and Charlotte are missing keys. Platform linkage itself is not displayed, so stored keys do not prove that Instagram/TikTok/X accounts are linked.
3. Only Sienna has visible social handles. Camille, Charlotte, Madison, Gabriela, and Valentina have no handles shown in their profiles.
4. Fanvue is globally connected, but per-model account mapping and ID-verification state are not exposed. Five models have no Fanvue-library items; all visible Fanvue-sub metrics are 0.
5. Fanvue-ready NSFW/reference coverage is incomplete: the profile UI reports no NSFW refs for Sienna, Camille, Gabriela, and Valentina (Charlotte and Madison show an NSFW ref). This may block automated Fanvue content generation.

## Sam’s checklist when awake

- Confirm/complete Fanvue creator **ID verification** and confirm each model’s Fanvue account mapping; the dashboard did not expose verification state.
- In Ayrshare, verify/link the intended Instagram, TikTok, and X accounts without relying solely on a stored key; add the missing Sienna and Charlotte profile-key configuration only after the links are confirmed.
- Fill in and verify handles for the five profiles where none are shown.
- Complete missing Fanvue NSFW/reference assets where required, while keeping platform/content policy boundaries clear.
- Review the pending/rejected approval queue. Keep live posting OFF until the queue and account readiness are deliberately approved; only then decide whether to enable go-live.

## Screenshots

- Scoreboard: `ACCOUNT_INVENTORY_2026-09-05_scoreboard.png`
- Credential vault: `ACCOUNT_INVENTORY_2026-09-05_vault.png`
- Approvals / go-live safety gate: `ACCOUNT_INVENTORY_2026-09-05_approvals.png`

All three screenshots are alongside this report in `/workspace/hf-test/zen/`.
