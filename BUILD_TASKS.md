# JSW BUILD TASKS - for Claude Code, running on the droplet (/opt/jsw)

Read CLAUDE.md first (operating rules + guardrails). This is the deep-build task list, in order.
Handed off 2026-10-24 from the session that built the foundation. Sam is often on his phone - batch
your questions, and follow the "try 3 real fixes yourself, then escalate" rule.

## Already done - do NOT redo
- Code is here at /opt/jsw (GitHub main = this; remote git@github.com:jsw-ai/jsw-ai.git via deploy
  key /opt/jsw-ai/.deploy_key; old droplet code preserved on branch old-droplet-backup).
- Python venv at /opt/jsw/.venv with the face/identity stack installed AND verified (cv2,
  onnxruntime, insightface all import). requirements.txt is in /opt/jsw.
- Transferred data in /opt/jsw-data: SHARED_LEARNINGS.md, identity_packs.json, jsw_library/
  (INDEX/SUMMARY only - the actual photos are NOT here yet).
- Temporary transfer user jswxfer exists (Grok's SSH key authorized) for pulling more data from
  grok-vm by rsync into /opt/jsw-data/. Remove it (userdel -r jswxfer) once transfers are done.
- op (1Password CLI) 2.30.3 installed 2026-10-24 at /usr/local/bin/op from the direct binary release
  (signature verified against 1Password key 3FEF9748469ADBE15DA7CA80AC2D62742012EA22). Root-only
  secrets dir /etc/jsw (0700) created; op.env not written yet - waiting on Sam's token.

## Progress log
- 2026-10-24 Task 1 DONE: /etc/jsw/op.env (root 600) holds the JSW service-account token; `op vault list`
  sees vault JSW. Item refs: Higgsfield = op://JSW/ykb2dlrqmzfulc2hz5qqjziyzq/{username=key id,
  password=secret}; GeeLark = op://JSW/7h4mzmkqm5dyfefguroh6tjbr4/password (Bearer token, + traceId
  header; base https://openapi.geelark.com). Load with `set -a; . /etc/jsw/op.env; set +a`.
- 2026-10-24 Task 2 PARTIAL: Higgsfield auth OK (GET /v1/custom-references/list 200; Soul 2 estimate
  0.050 cr / $0.004 at 2k). Test gen for Sienna ba97f512 -> 403 not_enough_credits; 0 credits spent.
  API account needs credits (purchase = Sam's yes). No balance endpoint known. Approved Sienna soul is
  ba97f512 (f9700355 in api_notes.md/probe_hf.py is the older id). hf-test/balance.py GENERATES images
  despite its name - do not run it as a balance check.
- 2026-10-24 GeeLark auth OK (POST /open/v1/phone/list 200): only 1 phone, "Cloud phone
  profile_template"; no per-model phones yet.
- 2026-10-24 19:40 Higgsfield REST catalog (GET /models, 91 models; snapshot in session scratchpad):
  NO Seedream of any version, no Nano Banana/GPT Image. Has soul/v2 standard + image-to-image,
  kling-video/v3.0 {std,pro,4k}/image-to-video, seedance 2.0/2.5, qwen-image-3 edit. Old pipeline
  ran seedream_v5_pro via the Higgsfield MCP (`generate_image`) on the APP account, not REST - so
  Hard Rule #1 stills are not REST-callable with this key. Path forward = Higgsfield MCP connector on
  the app account (claude.ai Higgsfield connector is available here, unauthenticated).
- 2026-10-24 GeeLark recheck 19:40: still 1 phone (template), 0 proxies, 0 groups. Sam says 10 were
  bought - not visible to this API key yet. Endpoints proxy/list, group/list, tag/list work.
- 2026-10-24 proxies.json landed (6 models, Decodo ISP static, http, host isp.decodo.com, one port per
  model: madison 10001, gabriela 10004, camille 10005, valentina 10006, charlotte 10007, sienna
  10008). Moved to /etc/jsw/proxies.json (root 600). NOT loaded into 1Password: the service account
  is read-only. Not yet assigned in GeeLark (no model phones exist).
- 2026-10-24 Reference rsync list written: /opt/jsw-data/RSYNC_REFS_FILELIST.txt (44 files, approved
  packs sienna/charlotte/madison/gabriela/camille_v3, valentina skipped; paths relative to
  /workspace/hf-test).
- 2026-10-24 Sam (ANSWERS2.md): no Higgsfield sign-in by bot; HOLD phone config + no API phone creation
  until he confirms no extra cost; proxies stay in /etc/jsw/proxies.json (not 1Password).
- 2026-10-24 Higgsfield REST callable (estimate-only, 0 credits spent): soul/v2 standard + image-to-image
  0.050 cr; qwen-image-3 edit/t2i 0.640; z-image/turbo 0.240; grok-imagine-image-2.0 0.960; recraft
  v4.1 pro 3.360; marketing-studio/image 5.965; kling 3.0 std i2v 5s 8.568, pro 11.424; kling o3
  image-reference 5.712; seedance 2.0 token-metered. Still no Seedream -> Hard Rule #1 stills not
  possible on this key; nearest REST edit (soul/v2/image-to-image) is NOT the approved method.
- 2026-10-24 Task 4 (partial): jsw_post/geelark.py written - TikTok (task/add, markAI), IG Reels
  (aiTag), YT Shorts (isDisclosureMandatory), FB Reels, X, Reddit video; temp upload; task status;
  Reviewer-PASS gate (abs path + md5 + per-platform caption + transition), caption lint, live-post
  ledger dedupe, maxTryTimes 0 on TikTok. Live needs --live AND /etc/jsw/GO_LIVE (absent). Dry-run
  tested on the template phone id; gate tests all block as expected. phones.json mapping empty.
  Gaps: X RPA is video-only (no X image posts); X/FB/Reddit RPA have no AI-label field.
- 2026-10-24 GeeLark plan (pay/plan/info): Pro, $198.40/mo, 20 profiles, 6 monthly-rental devices
  (Sam said 10), parallels 0; wallet $0 + $19.84 gift. Created 6 phones (Sam authorized, ANSWERS3) with
  chargeMode 1 (monthly; chargeMode 0 = pay-per-minute, never used): ids in jsw_post/phones.json,
  group "JSW models", tag = model, proxy = model's AdsPower Decodo port, Android 12, app language
  English (RPA needs English, failCode 20008). Wallet unchanged after. All 6 show hasBind=False and
  availableMonthlyRentals still 6 -> binding to the monthly devices is NOT done; no bind API exists.
  Phones NOT started (an unbound start could bill per-minute). 4 spares NOT created (no prepaid
  capacity). All 6 report country USA incl. Camille/Gabriela/Valentina (region follows proxy IP).
- 2026-10-24 GeeLark team apps added + auto-install ON for group "JSW models": TikTok 47.4.3,
  Instagram 452.0.0.48.64, YouTube 21.42.243, Facebook 583.0.0.39.55, X 12.35.0, Reddit 2026.42.0.
  They install when each phone first starts (app/install needs a running phone, error 42002).
- 2026-10-24 Task 3 DONE: refs arrived (44/44, 126 MB, /opt/jsw-data/hf-test). identity_gate.py
  rewired: refs/packs from /opt/jsw-data (env JSW_REF_ROOT / JSW_PACKS), venv /opt/jsw/.venv, 0.78
  centroid for stills (all sources) and EVERY video frame (no-face frames skipped, framing = notes),
  camille -> camille_v3, DRAFTED/RETIRED packs refused (valentina). best_ref 0.74 kept on stills.
  Verified: all 5 packs load, every face ref has a face; LOO centroid: sienna .747-.835 (3 video-frame
  refs < .78), charlotte .769-.921, madison .860-.911, gabriela .798-.941, camille_v3 .781-.857.
- 2026-10-24 Higgsfield key replaced by Sam (Ultra account, key id 44cb871b...). Vault item stores the
  combined "id:secret" in the username field, password empty -> use `Key <username>`. Auth 200, same
  91-model catalog (no Seedream), empty custom-references. Test gen -> 403 not_enough_credits, 0 spent.
  Higgsfield help center: API bills a separate prepaid USD balance (top up at open.higgsfield.ai,
  min $5); plan credits apply only to web app / MCP / CLI.
- 2026-10-24 Login order (ANSWERS5): Gmail first on each phone, then social apps via Sign in with
  Google; Google new-device challenges -> Sam after 3 tries. Planned tool: GeeLark rpa/task/googleLogin
  (email, password, code2fa), then per-app logins. NOT built/run yet: (a) conflicts with CLAUDE.md
  "won't type a password into a login form" - needs Sam's explicit ruling; (b) phones unbound/not
  started. Vault check: no model login item has a TOTP field; Sienna has no Gmail item (only
  "Email (wc2026fans)"); Outlook items for charlotte/madison/gabriela/valentina have no password;
  every item has an unlabelled "Field 6" (STRING, 14-17 chars, not TOTP/base32) - meaning unknown.
- 2026-10-24 Sam ruling: Sam signs in each model's Gmail himself in the GeeLark app; the bot NEVER
  automates Google sign-in (googleLogin RPA not to be used). After Gmail is in per model, the bot does
  the social Sign-in-with-Google logins + reads email 2FA codes from that inbox. Phones re-verified
  ready (6/6 exist, correct name + proxy port, monthly); still unbound (hasBind False) - Sam to bind in
  the GeeLark app first. Waiting on Sam: per-model "Gmail is in" confirmation.

## Credentials
All in 1Password, vault "JSW" (Business): Higgsfield API key, GeeLark (API key + bearer), and every
model's Gmail/social/Fanvue login + TOTP. A read-only service-account token for that vault was
created by Sam - ASK SAM for it to wire secrets. Never print credential values.

## Guardrails (also in CLAUDE.md - enforce these)
- Disclosure stays on (platform AI label on every post, AI in every bio); never deny AI if asked.
- Adults only. Deletes and purchases need Sam's explicit yes. Never post as Sam in Slack.
- You won't type passwords into login forms, create accounts, or solve CAPTCHAs - escalate to Sam.
  (A login script using the op CLI + the model logins is the right way to automate logins.)
- Quote credit cost before generating; verify state before/after each action (avoid double-posts).

## Tasks, in order
1. Secrets. Reinstall op. Get the service-account token from Sam; store it root-only (e.g.
   /etc/jsw/op.env as OP_SERVICE_ACCOUNT_TOKEN=..., mode 600). Verify 'op read' pulls the Higgsfield
   and GeeLark keys from the JSW vault. Keep values out of logs/commits.
2. Prove generation. Read hf-test/gen_api_base.py, hf-test/balance.py, hf-test/probe_hf.py to learn
   how the code calls Higgsfield. With the key set, run the lightest call (balance) to confirm auth
   end-to-end, then one test image for an approved model (Sienna soul_id
   ba97f512-0ed0-4c56-9480-5abe167b06d1). Report exact credits.
3. Reference images. From /opt/jsw-data/identity_packs.json, collect the approved face_refs/body_refs
   (relative to /workspace/hf-test) for the APPROVED packs - sienna, charlotte, madison, gabriela,
   camille_v3 (valentina is DRAFTED_UNAPPROVED; skip for now). Have Sam relay to Grok an rsync of
   exactly those files + voicerefs-from-sam/*.mp3 to jswxfer@206.81.3.238:/opt/jsw-data/hf-test/
   (preserve relative paths). Then wire the identity gate (identity_gate.py / MODEL_CONTENT_PROCESS.md)
   to those refs at threshold 0.78.
4. Posting. Learn how the code posts (Ayrshare + the GeeLark layer). Wire GeeLark (api key + bearer).
   Build the TextVerified+GeeLark SMS-2FA login flow from CLAUDE.md (prefer TOTP/email). Do a DRY-RUN
   post and get Sam's explicit go-ahead before any real/live post.
5. Run-loop (the big one - it never existed). Build the autonomous orchestration that runs, per the
   Notion Hard Rules: generate -> Reviewer PASS gate (0.78) -> schedule -> post, on the daily quota,
   per model, escalating the human-only steps to Sam. Run as systemd services (jsw-*); Sam may need
   to approve service installs.
6. Verify + commit. Keep secrets out of git. Commit and push to main (deploy key). Update Notion
   (Hard Rules / Tools pages) and this file as the system changes.

## Source of truth & coordination
- Notion is canonical process (links in CLAUDE.md). Set up the Notion connector so you can read it;
  until then work from CLAUDE.md + the hf-test/*.md docs (HIGGSFIELD_EXPERT_GUIDE, LIPSYNC_METHOD,
  MODEL_CONTENT_PROCESS, CONTENT_RECIPE, VALENTINA_PIPELINE, SHARED_LEARNINGS).
- grok-vm (the old runtime) still holds the photos and any fan data; move them via Sam->Grok using
  the jswxfer rsync path above.
