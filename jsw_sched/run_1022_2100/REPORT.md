# JSW scheduling run: Thu 10/22/2026, 9 PM ET (finished ~9:50 PM ET)
Helpers in this folder: ayr.py, md5dur.py, audit.py. Action logs: act_patch_lggv.json, act_patch_ejpl.json, act_fix_2115.json, act_repost_2QS1.json. Pending snapshot: pending_final.json (40 posts).

## Hold status
- Sienna's hold was lifted at 8:30 PM ET, and there's no new hold on the calendar banner.
- All 15 of her pulled posts were already re-created at about 8:34 PM ET, with media, OAuth1 on the X posts, durations of 7 s or more, and AI labels. md5 matches the passed u2 files (REV-382–389). Nothing needed re-creating.

## Reviewer intake (REV-348–411, since ~5:30 PM ET)
- Every PASS is already booked, and each booked file was verified by md5:
  - REV-355, 363–365, 373, 375, 376, 382–389, 395–400, 404–406, 408–410.
- PASS but not bookable because the file is under 7 s. Each was sent back to its model:
  - REV-401 Valentina mami11 IG Reel v3b (4.2 s)
  - REV-402 Valentina mami11 TikTok v3b (3.8 s)
  - REV-403 Madison pickleball IG Reel (4.6 s; REV-411 also failed the 8.1 s replacement)
  - REV-407 Charlotte matchday/recovery YT Short v9 (4.73 s)
- PASS with a placeholder caption, so held: REV-360 Gabriela collab clink v8 ("@<CHARLOTTE_HANDLE>"). Filling in the handle is a caption change, so it has to go back to the Reviewer.
- Already handled elsewhere:
  - REV-394 Charlotte Tegernsee YT (IYj2) was deleted at 8:35 PM ET by another bot, and its Notion row is already Pulled.
  - REV-354 collab v5 (doehscIZ YT) no longer exists in Ayrshare, and its Notion row is already Pulled.
- Fails (not booked): REV-348–353, 356, 357, 361, 362, 366–372, 377–381, 390–393, 411.

## Booked (new)
- Gabriela Reddit KU3aYneLxc0XHMdtQ8er, Fri 7:00 PM ET, u_Fresh_Membership8984. This is a repost of failed 2QS1agXn with the same media, title and body.

## Fixed / moved
- Valentina X spacing (2h rule; 8:15 and 8:50 PM were already live):
  - LGGVm5l5: 9:45 → 10:50 PM ET Thu
  - 7wBxHeb4: 11:30 PM → 12:50 AM ET Fri
  - U0qRKH8X: 10:55 PM Thu → Sat 10/24 1:00 PM ET. Its S8 still can't post on Fri because R1 TikTok uses S8 that day (REV-376).
- Sienna X ejpL9abY: 9:25 → 10:00 PM ET Thu, to keep 2h after the 8 PM live X. It's still byok.
- Charlotte X LO5LBV76 → re-created as Vuz0YPrqjPOXnwi39gwz (Fri 7 PM ET) with media marked SENSITIVE, which REV-395 requires and the old post was missing.
- Charlotte X VePwd2UU → re-created as gX2hDgdqVDv0U5fJorV6 (Fri 1:30 PM ET) with the REV-408 caption "recovered. mostly." The booked caption had an unreviewed " darling 😇".

## Pulled
- None as net pulls. The two old Charlotte ids were deleted only after their replacements were verified.
- Deleted earlier tonight by other bots: Valentina uoOHCgVe (Notion set to Pulled), Sienna jWfKag97, Charlotte dDc7WBVC, Charlotte IYj2yedb.

## Failures since 6:30 PM ET
- Charlotte IG HjQPPcZf (8 PM): code 161. Instagram is now unlinked from Charlotte's Ayrshare profile, which needs a relink. Her pending IG posts (yT50 7 AM, 08ui 9 AM, vvj5 11 AM, IvxrV2vL 4:30 PM Fri) will fail unless she's relinked first.
- Gabriela Reddit 2QS1agXn (9 PM): code 121 SUBREDDIT_NOEXIST on her own profile sub. jNHC10ly posted fine to the same sub at 5 PM, so I reposted it as KU3a (Fri 7 PM ET).
- Other entries were creation-time 137 duplicate rejects by model bots: Valentina 1HTNk98T, Madison tnckEIfh, and my first LO5L attempt P8C1lZsl. Nothing went out.

## Unreviewed bookings
- None found. Every pending post booked since 6:12 PM matches a PASS by md5. Charlotte IvxrV2vL, OAiTW and q9WQ have PASS rows (REV-406/409/410) that carry no caption text.

## Went live since 6:30 PM ET
All are set to Posted in Notion with the link. The X posts were confirmed through the X API, and the YT, TT, FB and IG links return 200.
- Madison X 1eRhVIWP 6:30 PM https://twitter.com/MadisonCole69/status/2113397561478316165
- Valentina IG story ZToIDV1I 6:30 PM https://www.instagram.com/stories/valentina_reyes_wc26/4013850071511160679
- Charlotte X nOtyXqGg 7 PM https://twitter.com/char_hayes_26/status/2113405525404643599
- Gabriela YT oLV2j8Zs 7 PM https://youtu.be/gNyOy5ueV14
- Madison YT OYSCuKjl 7:30 PM https://youtu.be/3GUGT2-OXF4
- Charlotte Reddit S6xK5JOh 7:30 PM https://www.reddit.com/r/u_CharHayesWC26/comments/1xcy8ma/recovery_day_in_munich_after_a_22_away_day/ (Reddit blocks curl from the box, so this is Ayrshare's success status only)
- Gabriela TT TLDqOTO7 7:30 PM https://www.tiktok.com/@gabriela_santos343/video/7699638986637118740 (Notion row was already Posted)
- Valentina FB HipuzPhW 7:30 PM https://www.facebook.com/1413498831838808/posts/122113182285504444
- Sienna X n2y3YOQX 8 PM https://twitter.com/BlakeSienn39605/status/2113420697057837446
- Valentina X Pt2KqI0g 8:15 PM https://twitter.com/v_reyes_wc2026/status/2113424323130069070
- Charlotte FB vg9suT7c 8:30 PM https://www.facebook.com/1318821087988645/posts/122107946313471927
- Valentina X v6uiKRmp 8:50 PM https://twitter.com/v_reyes_wc2026/status/2113432787256594699

## Drive files not moved to 05 Posted
- Only Madison moved files tonight: 3 v4C stills (patio, pickleball, golf) at 6:31 PM ET.
- None of the other 11 posts above are in a 05 Posted folder (Charlotte, Gabriela, Sienna, Valentina, and Madison's YT).

## Boost picks (live, Reviewer boost-safe)
- No new boost-safe tags since 6 PM. The earlier picks stand:
  - Camille X Bth4kO9v
  - Sienna X fOJyOhp5, elX80ktl, b2EjW6QA
- Sienna X U3kwyzsM ("who's coming to Bali with me?", REV-157 boost-safe) goes live Fri 9 PM ET and can be boosted then.
- Gabriela LcdBA8O1 is still not boost-safe.

## Daily report, Thu 10/22 (ET)
Posted today (Ayrshare success):
- Camille: X 1, IG 1, FB 1, YT 1
- Charlotte: X 4, FB 1, Reddit 1
- Gabriela: X 3, TT 1, YT 1, Reddit 1
- Madison: X 2, FB 1, YT 1, Reddit 1
- Sienna: X 4
- Valentina: X 2, IG story 1, FB 1

Still scheduled tonight:
- Sienna X ejpL 10 PM
- Charlotte X SNNw 10:30 PM
- Madison X 3ZED 10:30 PM
- Valentina X LGGV 10:50 PM

Failed today:
- Charlotte IG 1 (161)
- Gabriela Reddit 1 (121)
- Sienna Reddit 4 (121)

Pulled today: 18 at the 6 PM run, plus earlier runs' pulls, Sienna's 15 (hold, all re-created), and the deletes by other bots listed above. Tonight: 0 net.

Skipped/held tonight: REV-401, 402, 403, 407 (under 7 s), REV-360 (placeholder caption).

Quota gaps today: nobody hit TikTok 3, IG Reel, YT 2 or Reddit 2. Sienna had no TT, IG, YT or FB live. Camille had no TT or Reddit.

## Fri 10/23 gaps (ET)
- Camille: only YT Nifztz2l at 2 PM. Thin calendar.
- Valentina: only X 7wBx at 12:50 AM. Effectively empty. Her mami11 TT/IG need 7 s+ cuts, and "two left feet" isn't reviewed yet.
- Madison: X I86L 9 AM, Reddit LMCh 12 PM, X wAWp 1 PM. No TT, IG, YT or FB.
- Gabriela: IG story 9 AM, Reddit Qxuv 10 AM, X KMp5 12:30 PM, Reddit KU3a 7 PM. No TT, YT or FB.
- Sienna: TT z0IN 7:30 AM, IG story YUCf 9 AM, X 18Fx 7 PM, IG Reel 3eGe 8 PM, X U3kw 9 PM, X QMth 11 PM.
- Charlotte: 11 posts, but her 4 IG posts will fail while IG is unlinked.
- YT Shorts on Fri: none. Camille's YT is a regular 16:9 video.

## Blockers / for JSW AI
1. Charlotte's Instagram is unlinked in Ayrshare (code 161, "log in to instagram.com and follow the instructions"). It needs a login check plus an Ayrshare relink before 7 AM ET Fri, or 4 IG posts fail.
2. Sienna's YouTube isn't linked in Ayrshare. VwBsMfbH (Sat 6 PM ET, REV-384) will fail unless it's relinked. I kept it booked so the media carries over.
3. Gabriela Reddit 121 on u_Fresh_Membership8984 for one post, while another post to the same sub worked 4 hours earlier. KU3a and Qxuv on Fri test it again. Sienna's Reddit 121s are unresolved.
4. Valentina, Madison and Charlotte cuts passed at 3.8–4.7 s, but the 7 s rule means the models must re-export at 7 s or more and get re-review.
5. REV-360 needs the confirmed Charlotte TikTok handle in its caption, then Reviewer re-review.
6. Fri is thin for Camille, Valentina and Madison, and there are no Fri YT Shorts.
7. The models aren't doing the Drive 05 Posted moves (only Madison did).
