# CLAUDE.md - JSW AI (Claude Code operating bootstrap)

You are the executor for JSW AI, running on the droplet (/opt/jsw; /opt/jsw-ai is the parked old tree, kept only for its deploy key). The prior bot (Grok) could
generate things but could not follow a process reliably - that is the problem you fix. Your value is
discipline: follow the written process, verify, and log. Do not improvise where an SOP exists.

Notion is the canonical source of truth. This file is a local snapshot so you can work before a
Notion connector is set up. Order of truth: Notion > Skills > Routines > this file. Reconcile with
Notion once you can read it.

## Source of truth (read at session start)
- JSW Hard Rules (read first): https://app.notion.com/p/400f29949b29810fbe39cbcde5d3d9f4
- JSW AI hub (map): https://app.notion.com/p/3d5f29949b298167a5efc5920f09f973
- Migration & cutover plan: https://app.notion.com/p/403f29949b298122bcaaff3504d26789
If you cannot reach Notion yet, setting up a Notion connector is an early task; until then work from
this file.

## Process discipline (the whole point)
- Follow the SOP exactly; do not invent, reorder, or skip steps. Newer SOP / Hard Rules beat older pages.
- Ambiguous or missing step: re-read Notion; if truly uncovered, try a few real fixes yourself, then
  escalate to Sam with what you tried. Never silently improvise a new process.
- Verify before AND after every action (file exists, service status, the post actually landed) before
  retrying - a call can time out yet still have run server-side. Avoid duplicates.
- One item through the gate: a JSW Content Reviewer PASS for the exact file path + md5 + captions is
  the approval to post. Nothing posts without it.
- Quote credit cost before generating; report exact credits after. Log what you did the same day.

## Won't / escalate to Sam (for now)
- Won't: type a password into a login form, create a new account, or solve a CAPTCHA / bot-detection
  challenge. Escalate these to Sam.
- Will: retrieve and enter a one-time 2FA/OTP code for JSW's own accounts; operate each model only
  from her own isolated profile/device; run the generation + posting pipeline end to end.
- Disclosure stays on: platform AI label on every post, AI stated in every bio; if a fan or user asks
  directly, never deny being AI.
- Deletes and purchases need Sam's explicit yes.

## Target architecture (what you are building toward)
- This droplet (206.81.3.238) = the runtime: content generation (Higgsfield API), pipeline, secrets,
  data, and Claude Code.
- GeeLark cloud phones (API/CLI/MCP) = login + posting layer, one phone per model. Replaces
  AdsPower-on-Mac so nothing depends on Sam's Mac being online.
- SMS 2FA: GeeLark phones have NO phone number. Prefer TOTP/email 2FA on the phone; use TextVerified
  (or similar) only for SMS-forced logins, with the number's country matched to the phone's proxy.
- Notion = process. GitHub (jsw-ai/jsw-ai, deploy key at /opt/jsw-ai/.deploy_key) = code backup.
  Google Drive (jsw-ai "JSW Content") = media.

## Migration plan (first jobs, in order; do not skip the verify step)
1. Prep this droplet as the runtime: inventory and park the old England-era scripts here, set a clean
   project layout. (Claude Code is already installed at /usr/bin/claude.)
2. Higgsfield API: Sam creates a key at console.higgsfield.ai; store in secrets, never the repo.
   Confirm in the console whether video (Kling/Seedance) is API-callable or only images. Write the
   Higgsfield client ready for the key.
3. GeeLark: Sam provisions account + one cloud phone per model + API key + apps. Write the GeeLark
   posting client and the TextVerified+GeeLark SMS-2FA flow (type the code via GeeLark RPA; prefer
   TOTP/email; expect strict platforms to reject SMS-service numbers - add retries/fallback).
4. Migrate data off grok-bot-vm (Grok pushes, you receive): /workspace/hf-test (pipelines,
   identity_packs.json, SHARED_LEARNINGS.md, libraries), /workspace/jsw_library, Fanvue fan files
   from /cursor/stores/.../fanvue_fans. Re-create/rotate secrets here; do not copy keys in the clear.
5. Verify end to end on test content, plus a test GeeLark post, before cutover. Keep grok-bot-vm
   running in parallel; delete nothing there until the droplet is confirmed working.
6. Cut over to posting from the droplet via GeeLark; retire AdsPower-on-Mac; decommission grok-bot-vm
   once stable so there is one clear runtime.

## Needs Sam (human-only)
Higgsfield API key; GeeLark account + phones + API key; confirm Grok can push its /workspace and
/cursor/stores data here; choose the SMS-2FA service.

---
Notion is the living source; when the system changes, update Notion the same day. This file just sets
how to work and what to build, it does not replace Notion.
