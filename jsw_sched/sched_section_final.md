## Scheduling and Ayrshare calls (Scheduler)

Added 10/22 from the jsw-content-scheduling skill, /workspace/ayr\_sienna.py, /workspace/jsw\_sched/post.sh and the 10/22 run logs (madison\_pass\_1022\_1352.json, gabriela\_rev\_1022\_1331.json, run\_1022\_1200/REPORT.md). Base URL: <code>https://api.ayrshare.com/api</code> (app.ayrshare.com/api also works). Never print key values.<br /><b>Key files (paths only):</b>

- Ayrshare API key: <code>/home/box/agent-data/secrets/JSW-ayrshare-api-key.txt</code> → header <code>Authorization: Bearer <key></code>
- Profile keys: <code>/home/box/agent-data/secrets/JSW-<model>-ayrshare-profile-key.txt</code> → header <code>Profile-Key: <key></code>. Sienna is the Default profile, so she sends no Profile-Key.
- X OAuth1 consumer keys: <code>/home/box/agent-data/secrets/x-ayrshare-consumer-keys.json</code> (read by <code>H(True)</code> in <code>/workspace/ayr_sienna.py</code>)
- Helper scripts: <code>/workspace/ayr_sienna.py</code> (<code>H(x=False)</code> builds headers), <code>/workspace/jsw_sched/post.sh tag model file schedISO platformsJSON caption title</code> (upload, then post). Logs go to <code>/workspace/jsw_sched/<model>_<action>_<MMDD_HHMM>.json</code> and <code>run_<MMDD_HHMM>/REPORT.md</code>.

### 1. Find Reviewer PASSes and check md5s

- <b>Input:</b> JSW Content Reviews DB <mention url="https://app.notion.com/p/4dc6d10098254f0eaf107e39004770af" /> (notion-search or fetch, then filter rows with Verdict = PASS that aren't on the calendar yet).
- <b>Each PASS must name:</b> the exact file path with its version (<code>_v2</code>), the md5, the platforms, and the exact caption for each platform (plus the Reddit subreddit and title).
- <b>Check:</b> <code>md5sum <path></code> has to match the md5 in the review row. Also <code>ffprobe -v error -show_entries stream=codec_name,profile,pix_fmt,width,height -show_entries format=size <path></code> → h264 Main, yuv420p, 9:16, under 15 MB.
- <b>Pass:</b> the md5 matches, every field is present, and the post is inside the quota and spacing rules. <b>Fail:</b> a missing or mismatched md5, a missing platform or caption, a FAIL verdict, or a pass claimed only by a model bot. Don't schedule; send it back to the model bot or Reviewer and log the reason.
- <b>Common failures:</b> the file was re-exported after the pass, so the md5 changed → send it back to the Reviewer. The row points at <code>_v1</code> but <code>_v2</code> exists → use only the exact path in the pass.

### 2. Upload media

1. <code>GET /media/uploadUrl?fileName=<basename>&contentType=mp4</code> (jpeg for stills), with the Authorization header and Profile-Key (except for Sienna). The response is <code>{uploadUrl, accessUrl}</code>.
2. <code>curl -sf -X PUT -H "Content-Type: video/mp4" --upload-file <file> "<uploadUrl>"</code>
3. Put <code>accessUrl</code> in <code>mediaUrls</code> in the post body.

- <b>Pass:</b> uploadUrl isn't null and the PUT returns 2xx. <b>Fail:</b> <code>uploadUrl</code> is null → log the response without uploadUrl (post.sh prints <code>UPLOADURL FAIL</code>). A PUT failure is usually a wrong Content-Type or an expired URL → request a new uploadUrl and try again.

### 3. POST /post for each platform

Call <code>POST /post</code> with the body <code>{post, platforms:[...], mediaUrls:[accessUrl], isVideo:true, scheduleDate:"<UTC ISO Z>", ...options}</code>. Save the returned <code>id</code> and the response to the run log. Pass means <code>status:"success"</code> with an <code>id</code>; check with <code>GET /post/<id></code> that it shows <code>status: pending</code> and the right scheduleDate.

- <b>TikTok:</b> <code>tikTokOptions:{isAIGenerated:true}</code>. No TikToks between 12 and 7 AM model-local time.
- <b>IG:</b> <code>instagramOptions:{isAIGenerated:true, shareReelsFeed:true}</code> (<code>trialParams</code> is allowed for Trial Reels). The AI label <b>can't be added after publishing</b>, so a post missing it has to be pulled and re-created before it goes live.
- <b>YouTube:</b> <code>youTubeOptions:{title, visibility:"public", shorts:true, containsSyntheticMedia:true, thumbNail:<url>}</code>
- <b>X:</b> headers from <code>H(True)</code> (Bearer plus <code>X-Twitter-OAuth1-Api-Key</code> / <code>X-Twitter-OAuth1-Api-Secret</code>) <b>plus</b> Profile-Key. Sienna uses the Default profile, so she gets no Profile-Key. Without OAuth1 it fails with <b>419</b> <code>x_credentials_required</code>. A 419 saying "has not completed BYO linking" means the X account has to be linked in the Ayrshare dashboard by hand; skip it and report.
- <b>Reddit:</b> validate first (the pass names the subreddit and gives proof of its AI rule). A post to the model's own profile uses <code>redditOptions:{title, subreddit:"u_<username>"}</code> (for example Gabriela <code>u_Fresh_Membership8984</code>). Sienna's profile target fails with <b>SUBREDDIT\_NOEXIST</b>: don't schedule it; pull the post and report it until a working target is confirmed.
- <b>FB:</b> platform <code>facebook</code> and the passed caption.

### 4. Spacing and slotting

- Leave at least <b>2 h between posts on the same platform and account</b> (check pending posts first with <code>GET /history</code> or the post IDs on the calendar). One file goes to one platform only.
- Use the model's local time; scheduleDate is always UTC.
- Windows: the Shorts test runs one early-evening slot (about 5-7:30 PM model-local) plus one late-night slot (about 10-11 PM). Stagger models with similar content and keep the same format off the same day.
- <b>Fail:</b> a clash → move the new post, or PATCH the existing one (see step 5), and log it (for example "X golf moved to 8:30 PM").

### 5. Caption changes and time moves

- <b>Caption change:</b> only after a new Reviewer pass. <code>POST /post</code> the new body first, then <code>DELETE /post</code> with <code>{id:<old>}</code> (only for <b>pending</b> posts). Log <code><old>_delete: 200</code> and the new id, and update the calendar row title to the new id.
- <b>Time move:</b> <code>PATCH /post</code> with body <code>{id, scheduleDate:"<UTC>"}</code>, then check with <code>GET /post/<id></code>.

### 6. Deletes

- Pending posts: <code>DELETE /post {id}</code> (add H(True) for X).
- <b>TikTok and IG posts can't be deleted through Ayrshare</b> → ask the model bot to delete them by hand in the app, then set the row to Pulled.
- <b>X deletes need the OAuth1 headers</b> (H(True)).
- Deleting a <b>live</b> post needs Samuel's own explicit yes.

### 7. Retry

<code>PUT /api/post/retry</code> with body <code>{id}</code> for a failed post, after the cause is fixed (OAuth1 headers or relinking). Check with <code>GET /post/<id></code>. If it fails again, re-create the post and pull the old one.

### 8. Notion calendar rows

Posts DB <mention url="https://app.notion.com/p/fa052f8010e14317b6b3dc9547367e13" />: the title <b>ends with the Ayrshare ID</b> (for example <code>Madison X s7b · vM5HryOPC6hWZnOiBRwJ</code>). Fill in model, platform, date, slot with time zone, caption and file path, and put the <b>review link in Asset link</b>. Status is <b>Scheduled</b>, then <b>Posted</b> (add the URL from <code>GET /history</code>) or <b>Pulled</b> (with the reason).

### 9. Caption rules (pre-flight check on every caption)

- Never mention AI, and never deny it.
- Fanvue: Sienna and Charlotte only, and **never in a scheduled caption**. Fanvue links go only in the X bio, the pinned post and Reddit (set by hand). Never on TikTok, IG, YT or FB. No links at all on spicy X teases.
- Music: put the Apple Music link in the caption on X, YT, FB and Reddit. X song captions carry the link per the JSW AI caption rule (10/22, 2:06 PM ET), which overrides the older no-URLs-on-X rule; each URL in an X post costs $0.20. Use "link in bio" on TikTok and IG. No Spotify and no "everywhere". Gabriela stays on "coming soon".
- The caption has to match the Reviewer pass exactly; any edit goes back to the Reviewer.

### 10. Daily quota (per model)

| Platform | Max per day |
| --- | --- |
| X | 5 |
| TikTok | 3 |
| IG | 1 Reel + 3 stories |
| YouTube | 2 |
| FB | 1 |
| Reddit | 2 |

Count pending plus posted for the model-local day before you schedule. Anything over the quota → hold it for the next day and report.
