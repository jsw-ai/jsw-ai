# Higgsfield Virality Predictor: how to use it (JSW team)
Researched 2026-10-21, 10:15 PM EDT (America/Detroit).

## 1. What Higgsfield says it is for
- App page (https://higgsfield.ai/apps/virality-predictor): "Drop the clip: a hook you're testing, an ad before launch, a reel sitting in drafts. Any format, vertical or horizontal, **up to 15 seconds**." A modeled audience "watches" it; you get a virality score, a peak hook timestamp, a hold rate and a brain-region heatmap. Pitched as "the closest thing to a test screening before you hit publish."
- Launch post, 2026-05-09 (https://www.linkedin.com/posts/higgsfield_introducing-virality-predictor-quick-activity-7458988922782687232-Pn--): 1) upload any clip up to 15s, 2) get viral potential, hook score and hold rate, 3) brain heatmap, 4) "**Pair with Ad Reference** for recreated videos". Available on the platform, MCP and CLI.
- CLI README (https://github.com/higgsfield-ai/cli/): job type `brain_activity` "analyzes a **finished video** for hook strength, attention, retention, and viral potential": `higgsfield generate create brain_activity --video ./ad.mp4 --wait`.
- Official Cursor plugin skill (https://github.com/higgsfield-ai/cursor-plugin/blob/7d99efbeacc522f5b8c51b66a961fc5ea942e25a/skills/virality-prediction/SKILL.md): use it for "feedback **before posting** to TikTok, Reels, Shorts" and to "**compare two cuts of the same video**". Steps: get the video into Higgsfield (reuse the generation, or media_upload, then media_confirm for a local file), call virality_predictor, explain the signals, then recommend edits (re-cut the hook, pacing, regenerate). Guardrails: treat the scores as forecasts, and say so when confidence is low.
- Third-party coverage (https://creatorstoolbox.com/blog/higgsfield-virality-predictor, 2026-05-11): experimental, **free during the preview**, reportedly built on Meta's TRIBE v2 brain-response model.

Bottom line: it scores the **finished video**. That can be a local edit you upload or a Higgsfield generation. It is not for prompts or scripts, because it needs video. It is not part of Shorts Studio or Marketing Studio, and it has no built-in tool that makes variants and picks a winner. The only pairing Higgsfield names is Ad Reference: recreate a reference ad, then score the result. Comparing several cuts is something you do yourself.

## 2. MCP tools and how they chain
1. Local mp4: `media_upload` (returns a presigned URL), then `curl -X PUT -H "Content-Type: video/mp4" -H "If-None-Match: *"`, then `media_confirm` (type video), which gives you a media_id. For a raw Higgsfield generation, skip this step and pass the completed video job_id.
2. `virality_predictor` with `{action:"create", params:{model:"virality_predictor", medias:[{role:"video", id:<media_id or job_id>}]}}`, which returns a job_id.
3. Poll with `job_status` or `jobs_wait`. `job_display` or `virality_predictor` `{action:"preview", params:{model:"virality_predictor", job_id}}` reopens the dashboard.
4. The result is an HTML "Brain Activity Viewer" at `https://d8j0ntlcm91z4.cloudfront.net/<user>/hf_<ts>_<job_id>.html`. The embedded JSON holds the numbers (see virality_backfill/parse.py).
Related but separate tools: `video_analysis_create` (scene-by-scene breakdown of an uploaded video or a YouTube URL, useful for studying competitor or trend videos) and `shorts_studio_*` (restyles a source video into shorts). Neither one calls the predictor.

## 3. Cost
0 credits as observed. The 8 brain_activity jobs from 01:57-02:06 UTC on 10/22 (9:57-10:06 PM EDT on 10/21) do not appear in `transactions`, which only shows Seedream and Seedance spends. The free preview may end, so check `transactions` from time to time.

## 4. Output fields (from the real jobs)
`overall_score`, `brain_engagement`, `hook_score`, `viral_potential`, `sustain` (hold rate, 0-100), `peak_second`, `peak_frame_index`, `peak_score`, `global_scores_by_frame` (one value per second), plus brain-region cards and notes.

## 5. What the Reviewer backfill found (virality_backfill/, 9:48-10:09 PM EDT on 10/21)
The Reviewer uploaded 20 posted clips with their real view counts (list.tsv) and submitted 8 jobs (jobs.tsv); scores.json only holds 2 of them. Pulled results:

| clip | views | overall | hook | viral | sustain |
|---|---|---|---|---|---|
| v01 Charlotte fitcheck | 1409 | 42 | 26 | 42 | 100 |
| v02 Madison NYC lipsync | 1275 | 55 | 38 | 58 | 100 |
| v03 Valentina dance | 740 | 43 | 27 | 43 | 98 |
| v04 Valentina cafe | 604 | 53 | 32 | 60 | 100 |
| v05 Madison pilates (13s) | 486 | 46 | 28 | 45 | 98 |
| v06 Valentina ls2 | 475 | 53 | 33 | 58 | 100 |
| v07 Valentina car | 461 | 54 | 36 | 57 | 100 |
| v08 Valentina ls1 | 418 | 52 | 33 | 57 | 100 |
| v09 Valentina ls3 | 414 | 58 | 39 | 63 | 100 |

So far the scores do **not** track our real views. The two most-viewed clips that are not lipsyncs (v01, v03) scored lowest, and the lowest-viewed clip (v09) scored highest. The scores sit in a narrow band (42-58). The model seems to favor talking-to-camera lipsync, and `peak_second` is almost always the last second. Twelve clips (v09-v20) have uploads but no scores yet.

## 6. The right workflow for us
- **Where:** after local finishing (music, captions, cuts), on the exact mp4 we will post, before Reviewer approval. Higgsfield intends exactly this ("before you hit publish"). Clips must be **15 s or shorter**; trim longer cuts or score the first 15 s.
- **What to score:** the final edit, and ideally **2-3 versions of the same clip** (different hook or first second, caption timing, cut). Scoring the raw generation has little value because the predictor can't see our captions and music.
- **How to act:** use the score as a tie-breaker and a hook diagnostic, never as a pass/fail gate. Pick the version with the higher hook_score or viral_potential. If hook_score is in the bottom of our range (<30), try a stronger first second. Use `global_scores_by_frame` to spot dips. Identity, realism and platform rules still decide approval.
- **Calibrate:** finish the backfill (v10-v20) and log the score next to the 24h and 7d views in the Tracker. Revisit after about 30 posts. If the correlation stays flat or negative, drop the predictor to advisory only.

## Sources
- https://higgsfield.ai/apps/virality-predictor
- https://www.linkedin.com/posts/higgsfield_introducing-virality-predictor-quick-activity-7458988922782687232-Pn--
- https://github.com/higgsfield-ai/cli/
- https://github.com/higgsfield-ai/cursor-plugin/blob/7d99efbeacc522f5b8c51b66a961fc5ea942e25a/skills/virality-prediction/SKILL.md
- https://creatorstoolbox.com/blog/higgsfield-virality-predictor

## 7. Update 2026-10-21 ~10:30 PM EDT
- JSW AI rule: virality_predictor is ADVISORY ONLY (Reviewer SOP + Content Process pages updated).
- Backfill scored v09-v16 (jobs in virality_backfill/jobs.tsv, numbers in scores.json). v17-v20 NOT scored: "Daily limit of 20 generations reached". Media ids already uploaded (ids.txt); rerun tomorrow.
- Limits seen: max 2 concurrent jobs (ultra plan, shared with other bots) and 20 generations/day. Still 0 credits in transactions.

## 8. Update 2026-10-22 9:10 AM EDT
- Rerun of v17-v20 at 9:07 AM EDT still got "Daily limit of 20 generations reached" (both requests). The limit looks like a rolling 24h window from the 9:57-10:22 PM EDT 10/21 jobs. Reviewer rerun moved to 10:45 PM EDT 10/22.
