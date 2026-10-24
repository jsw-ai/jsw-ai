# JSW Account Ban Prevention — Action Plan (researched 2026-10-21)

Scope: Sienna, Camille, Charlotte, Madison, Gabriela, Valentina on Meta (FB/IG), YouTube, TikTok, X, Reddit.
Current setup (from box): one AdsPower profile per model on MacBook-Pro-6.local; Decodo static ISP US proxies (5 models; Sienna had no proxy until tonight, so she was on Samuel's home Comcast IP); TextVerified rented SMS numbers; Ayrshare API posting; high daily quotas. Nothing on the box was changed.

Caveat up front: Meta's Inauthentic Behavior and Account Integrity policies ban accounts that "deceive Meta or our users about the identity", or that are used to evade enforcement. Antidetect browsers and proxies don't make that compliant. The safest lever is **transparency**: label each account as an AI persona, run one real business identity behind them, and use official APIs. Fingerprint hygiene only cuts down the false "linked accounts / suspicious login" signals.

## Top 10 fixes, ranked by impact

1. **Label every account as an AI persona on every platform** (all 6, all platforms).
   - IG: since 2026-08-31, unlabeled AI-person profiles get their reach limited. Turn on "AI-generated profile". Labeling does not cut reach. https://creators.instagram.com/blog/ai-generated-profile-label
   - TikTok: turn on the "AI-generated content" toggle on every post. Realistic synthetic humans require disclosure, and not disclosing can lead to removals or restrictions. https://support.tiktok.com/en/using-tiktok/creating-videos/ai-generated-content
   - YouTube: in Studio, set "Altered or synthetic content" = Yes on realistic AI people. Also avoid mass-produced, repetitive Shorts, which YPP treats as "inauthentic content". https://support.google.com/youtube/answer/14328491
   - X and Reddit: put "AI-generated persona" in the bio. X can also mark automated accounts with an "Automated" label: https://help.x.com/en/using-x/automated-account-labels
2. **Stop cross-linking banned and live accounts. Freeze Sienna's network until her identity is clean** (Sienna first, then Gabriela).
   - Her FB was disabled, and her sessions ran on the home Comcast IP, which every other device of Samuel's also uses. Meta links accounts by IP, device and phone, so a disabled account can taint the others ("evade enforcement").
   - Don't create a replacement FB for Sienna right away, and never log into any model from the home IP.
   - Run appeals only from the same profile and proxy the account normally uses.
3. **Make the login footprint consistent: one model = one AdsPower profile = one dedicated static IP, forever** (all).
   - Check that no two models share a Decodo IP, and that no profile ever falls back to a direct connection.
   - AdsPower itself warns against sharing proxy IPs and recommends one dedicated proxy per profile. https://help.adspower.com/docs/creating_browser_profiles
4. **Fix the AdsPower configuration** (all; Samuel reports AdsPower "doesn't seem to be working", so check this first).
   - WebRTC = Disabled or Forward, never Real.
   - Timezone, geolocation and language = "Based on IP".
   - Leave canvas/WebGL noise on the defaults, and keep the OS/UA consistent with a Mac (don't spoof Windows on a Mac).
   - Use a common screen resolution.
   - After launching a profile, verify it on browserscan.net / ipinfo: the IP should be the Decodo IP, the timezone should match it, and there should be no WebRTC leak.
   - A failed proxy check that silently opens without a proxy is the most common way accounts get burned.
   - Docs: https://help.adspower.com/docs/How-to-choose-WebRTC-mode , https://help.adspower.com/docs/global_settings , https://localapi-doc-en.adspower.com/docs/Awy6Dg
5. **Fix the Ayrshare/AdsPower IP mismatch** (all).
   - Ayrshare posts through each platform's official API with OAuth tokens. API publishing from a server IP is normal and is not "a login".
   - The risky part is the OAuth *linking* step. Do the Ayrshare connect flow inside each model's own AdsPower profile, behind her own proxy, so authorization comes from the usual IP and device.
   - Never connect several models' socials in one browser session.
   - Don't also post manually at the same moment the API posts.
6. **Replace rented VoIP/TextVerified numbers with real, owned SIMs or eSIMs** (all, starting with any account that has hit a checkpoint).
   - Platforms score VoIP and reused rental numbers as high-risk. If the rental expires, you can't receive recovery or 2FA codes, and that makes an appeal impossible.
   - Use one dedicated, long-lived number per model. Add authenticator-app 2FA and a recovery email you own.
   - Practitioner consensus, not an official platform statement.
7. **Cut posting velocity for any account under about 60 days old** (all; Camille's accounts are empty, so she starts clean).
   - New accounts posting at full quota from day 1 (X 5, TikTok 3, YT 2, IG 1 Reel + 3 stories) look like spam automation.
   - Follow the warm-up schedule below. Never post duplicate media across accounts. Vary captions and posting times.
   - Reddit spam policy: https://support.reddithelp.com/hc/en-us/articles/360043504051-Spam
8. **Remove Fanvue/adult links until accounts are warmed up, then use them carefully** (all with Fanvue links, especially IG, FB, TikTok and YT).
   - Meta and TikTok restrict linking to adult or sexual services. An off-platform adult link on a new account is a top disable trigger.
   - After warm-up, use a neutral SFW link hub (e.g. a Linktree-style page) with an age gate. Don't use direct Fanvue links, cloaked or redirecting links, or sexual solicitation in bios or DMs.
   - On X, adult links are allowed if media is marked sensitive.
   - On Reddit, post only in subs that allow self-promotion, and keep it to 10% or less of activity.
   - Sources: https://transparency.meta.com/policies/community-standards/adult-sexual-solicitation/ , https://www.tiktok.com/community-guidelines/en/
9. **Respect each platform's automation rules** (X, Reddit).
   - X allows automated posts through the API, but **automated likes, follows and unsolicited replies or DMs are banned**. https://help.x.com/en/rules-and-policies/x-automation
   - On Reddit, don't post through scripts. Post by hand, follow each sub's rules, and build karma by commenting first.
10. **Set up account recovery, appeals and Meta-specific hygiene** (Sienna YT/X, Gabriela FB, Charlotte IG).
    - Keep one appeal per account, filed from that account's own profile and IP. Don't open new accounts while an appeal is pending.
    - Charlotte: open IG Account Status and appeal from there.
    - Meta triggers to avoid:
      - New FB profiles that immediately create Pages or Business Manager, or run ads
      - Changing the name, birthday or photo early on
      - Mass friend requests or follows
      - Logging in from many IPs
      - Links in the first posts
      - Using a selfie-verification face that doesn't match the "person"
    - Consider using a Facebook *Page* run from Samuel's real, aged personal profile and a verified Business Portfolio, instead of fake personal profiles. That is the Meta-compliant model for AI personas. https://transparency.meta.com/policies/community-standards/inauthentic-behavior/

## Per-platform warm-up (new or recovered accounts)
Applies to all six. Start Camille now; restart Sienna and Gabriela after their appeals resolve. All activity goes through the model's own AdsPower profile and proxy.

| Platform | Days 1–7 | Days 8–21 | Days 22–45 | After 45 days |
|---|---|---|---|---|
| Instagram | Finish the profile, add the AI label, browse and like 10–20 min a day, 0–1 story | 1 post every 2–3 days, 1–2 stories a day, no links | 1 Reel a day, 3 stories | Add a SFW link hub; full quota |
| Facebook | Browse only, a few likes, no Page | 1 post every 2–3 days | 1 post a day; create a Page if needed | Links, cautiously |
| TikTok | Watch the FYP in your niche 20–30 min a day, no posting for 3–5 days | 1 video a day with the AI toggle on | 2 a day | 3 a day; bio link once eligible |
| YouTube | Watch, subscribe and finish the channel | 1 Short every 2 days, AI disclosure on | 1 a day | 2 a day |
| X | Follow 5–10 accounts a day by hand, reply by hand | 1–2 posts a day | 3 a day | 5 a day; sensitive-media flag on any adult-adjacent posts |
| Reddit | Comment only, 3–5 genuine comments a day | Get to about 100 karma or more before posting | 1 post a day in subs that allow it | 2 a day; 10% or less self-promo |

## Other sources
- Meta Account Integrity: https://transparency.meta.com/policies/community-standards/account-integrity/
- AdsPower fingerprint guide: https://help.adspower.com/docs/browser_fingerprint
- Automation rulebook (compiled 2026-10): https://www.blotato.com/research/social-media-automation-rulebook/rules.csv
- TikTok Shop AIGC disclosure rules (2026-09): https://seller-us.tiktok.com/university/essay?knowledge_id=491489038501663&lang=en
