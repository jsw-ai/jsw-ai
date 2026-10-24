# VIRALITY_BACKFILL.md (2026-10-21, ET)
Tool: user-Higgsfield `virality_predictor` (model `brain_activity`). **Cost: 0 credits per call** (no transactions logged), but the account is limited to **2 concurrent jobs and 20 generations per day**, so only 16 of the 20 most recent posted videos are scored so far; v17-v20 rerun tomorrow. Clips were mapped from the tracker (`jsw_tracker/out/posts.json`, cross-posts merged, views summed across platforms; IG views are null in the tracker) to files via captions.json / posted logs. Some mappings are best-effort (marked approx in list.tsv notes). Scores are predictive proxies 0-100.

| model | clip | file | overall | hook | viral | engagement | views (sum) | notes |
|---|---|---|---|---|---|---|---|---|
| Charlotte | Lounge to matchday swipe | charlotte_03_bayern_fitcheck.mp4 | 42 | 26 | 42 | 31 | 1409 | weak hook (<30): first 3 s not stopping scroll; peak at 9 s; peaks late, front-load the payoff; sustain 100 |
| Madison | NYC iced coffee lipsync | lipsync1_new_york_growing_on_me.mp4 | 55 | 38 | 58 | 50 | 1275 | strong hook; peak at 8 s; peaks late, front-load the payoff; sustain 100 |
| Valentina | legs gone dance | valentina_dance1_9x16.mp4 | 43 | 27 | 43 | 34 | 740 | weak hook (<30): first 3 s not stopping scroll; peak at 6 s; sustain 98 |
| Valentina | buying the next one cafe | valentina_lipsync3_cafe_9x16.mp4 | 53 | 32 | 60 | 46 | 604 | ok hook; peak at 8 s; peaks late, front-load the payoff; sustain 100 |
| Madison | 7am pilates | ig_reel_pilates_1148am.mp4 | 46 | 28 | 45 | 39 | 486 | weak hook (<30): first 3 s not stopping scroll; peak at 7 s; sustain 98 |
| Valentina | salsa red flag ls2 | ls2.mp4 | 53 | 33 | 58 | 46 | 475 | ok hook; peak at 8 s; peaks late, front-load the payoff; sustain 100 |
| Valentina | I called it car lipsync | valentina_lipsync2_car_9x16.mp4 | 54 | 36 | 57 | 48 | 461 | strong hook; peak at 8 s; peaks late, front-load the payoff; sustain 100 |
| Valentina | mom has notes ls1 | ls1.mp4 | 52 | 33 | 57 | 45 | 418 | ok hook; peak at 8 s; peaks late, front-load the payoff; sustain 100 |
| Valentina | hora colombiana ls3 | ls3.mp4 | 58 | 39 | 63 | 55 | 414 | strong hook; peak at 8 s; peaks late, front-load the payoff; sustain 100 |
| Madison | golden hour montage | montage2_v4.mp4 | 43 | 26 | 42 | 35 | 283 | weak hook (<30): first 3 s not stopping scroll; peak at 11 s; peaks late, front-load the payoff; sustain 100 |
| Charlotte | flying Bayern away | charlotte_02_flying_bayern_away.mp4 | 41 | 26 | 41 | 31 | 277 | weak hook (<30): first 3 s not stopping scroll; peak at 7 s; sustain 92 |
| Charlotte | ex-footy leg day | charlotte_01_exfooty_legday.mp4 | 44 | 28 | 42 | 35 | 240 | weak hook (<30): first 3 s not stopping scroll; peak at 7 s; sustain 98 |
| Madison | pickleball resort | madison_03_resort_pickleball.mp4 | 48 | 33 | 48 | 39 | 95 | ok hook; peak at 6 s; sustain 100 |
| Madison | packing to airport | madison_01_packing_to_airport.mp4 | 46 | 30 | 45 | 36 | 89 | ok hook; peak at 9 s; peaks late, front-load the payoff; sustain 100 |
| Madison | Scottsdale golf | madison_02_golf_day.mp4 | 55 | 36 | 61 | 49 | 18 | strong hook; peak at 8 s; peaks late, front-load the payoff; sustain 100 |
| Charlotte | Munich rooftop pool | charlotte_03_munich_rooftop.mp4 | 43 | 28 | 40 | 32 | 0 | weak hook (<30): first 3 s not stopping scroll; peak at 8 s; peaks late, front-load the payoff; sustain 100 |

## Summary
- 16 scored. Overall median 47.0, range 41-58. Hook scores are low everywhere (26-39): no clip has a strong first 3 s.
- Talking/lip-sync clips score higher (median 53.5) than silent montages/transitions (median 43.5).
- Correlation of overall score with summed views: r = 0.05 (n=16; views are tiny and IG views missing, so weak evidence). The top-viewed clip (Charlotte lounge-to-matchday, 1,409 views) scored only 42, so the predictor misses swipe-transition and YouTube Shorts distribution effects.

## Suggested pass threshold
- **Overall >= 50 AND hook >= 33** to schedule without changes; 45-49 = fix the hook (open on the punchline/payoff, text in first frame, motion in first 0.5 s) and re-score; < 45 = re-cut or drop. Treat it as a hook check, not a veto, until 30+ posts with views let us recalibrate (target: re-fit weekly against tracker views).
- Rule of thumb from peaks: most clips peak at 7-9 s of an 8-9 s clip, so the payoff lands too late. Move the best moment into 0-3 s.
