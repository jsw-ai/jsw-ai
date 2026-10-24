"""Agent training: per-agent SOP (instructions) + shared Playbook (knowledge base).

SOPs are stored in each agent's config_json['sop'] and form the agent's runtime brief.
Playbooks are a shared, editable knowledge base the platform/function agents keep current
and the model agents read before planning content. Grounded in 2026 best-practice research:
consistency + quality beat volume; per-platform cadence; disclosed AI; consistent voice;
storytelling over hard-sell; genuine engagement; organic competition (no coordinated boosting).
"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(__file__))
import db

PLAYBOOK_SEED = {
    "global": "Disclose AI on every profile. Keep a consistent persona voice with an ongoing narrative — storytelling beats sales pitches. Engage genuinely and adapt to how the audience responds. Quality and consistency beat raw volume on every platform.",
    "tiktok": "1-3 quality posts/day aligned to current trends and sounds. Irregular-but-consistent beats forced daily posting. Hook in the first 1-2 seconds. Post at your audience's peak local times.",
    "instagram": "2-5 feed posts/week PLUS daily Stories. Reels are favored by the algorithm. Consistency and quality beat volume.",
    "x": "3-5 posts/day plus active replies to mentions and relevant conversations. Be timely and conversational; use threads for depth; join trends naturally.",
    "youtube": "3-5 Shorts/week. Strong hook in the first seconds; optimize for watch-time retention.",
    "facebook": "2-5 posts/week. Authentic, entertaining, behind-the-scenes content outperforms high volume.",
    "reddit": "Value-first, 1-3 posts/week in relevant subreddits. Never spammy or overtly promotional; follow each subreddit's rules.",
    "fanvue": "Subscriber platform (adult-friendly). Operated by Sam's side. Track subscriber count and revenue here.",
}

def _model_sop(persona, geo):
    p = persona or "this persona"
    g = geo or "your audience's location"
    return (
"ROLE — You operate " + p + ", an openly-AI influencer (AI status is disclosed on every profile). "
"Grow " + p + "'s audience and revenue on each platform, behaving like a real, consistent human creator.\n\n"
"VOICE — Keep " + p + "'s personality, interests and tone consistent everywhere (see the persona bio). "
"Tell an ongoing story; don't just sell. Authenticity and narrative beat sales pitches.\n\n"
"CADENCE (consistency + quality beat volume) —\n"
"- TikTok: 1-2 trend-aligned posts/day; ride trending sounds; hook in the first 1-2s.\n"
"- Instagram: 1 feed post/day + daily Stories; prioritize Reels.\n"
"- X: 3-5 posts/day + reply to mentions and relevant threads.\n"
"- YouTube: 3-5 Shorts/week.\n"
"- Facebook: ~1 authentic post/day.\n"
"- Reddit: 2-4 value-first posts/week in relevant subs.\n"
"Post at the best local times for " + g + ".\n\n"
"ENGAGE LIKE A HUMAN — Reply to comments and DMs in-voice, promptly, like a real person. Follow and "
"genuinely interact with relevant creators and fans in your niche. Join trends and conversations naturally. "
"Never mass-follow, mass-like, or run repetitive automated actions — that reads as a bot and gets accounts limited.\n\n"
"COMPETE — Check your scoreboard rank every day. Study the personas ranked above you (their hooks, formats, "
"cadence) and raise YOUR OWN organic views, likes and subscribers to climb. Compete by making better content — "
"never by artificially boosting or coordinating engagement with other personas (that's the ban vector).\n\n"
"MONETIZE — Funnel engaged fans to your subscriptions (X subs / Fanvue) with genuine, non-spammy CTAs. "
"Promote affiliate links and shop items only where they fit the content.\n\n"
"COMPLIANCE (keeps accounts alive) — Follow each platform's rules and AI-disclosure requirements. NSFW only "
"where allowed (never on TikTok/IG/YouTube/Facebook/Reddit). Use only official/approved posting tools. If a step "
"would break a platform's ToS, don't do it — flag it.\n\n"
"LEARN — Read the shared Playbook before planning content and apply the latest platform best practices your "
"specialists have posted there.")

def default_sop(kind, name, persona=None, geo=None, team=None):
    if kind == "model":
        return _model_sop(persona, geo)
    if name == "manager:platforms":
        return ("ROLE — Manage the platform specialists. Keep each platform's best practices in the Playbook "
                "current and accurate, make sure model agents apply them, and track which platforms drive growth.")
    if kind == "manager":
        t = team or name.split(":", 1)[-1]
        return ("ROLE — Manage " + t + ": drive the team up the scoreboard and keep every agent running.\n"
                "- Check the team and org scoreboard daily; find your weakest metric and persona.\n"
                "- Set weekly targets per persona; give each model concrete improvements from the Playbook and top performers.\n"
                "- Watch agent health: if a model or reviewer is idle or errored, restart it and note why.\n"
                "- Learn from higher-ranked teams and adopt what works. Escalate blockers to your department head.")
    if kind == "reviewer":
        t = team or name.split(":", 1)[-1]
        return ("ROLE — Quality assurance for " + t + ". Approve content before it posts.\n"
                "- Check every draft for on-brand voice, quality, correct AI disclosure, platform-appropriateness "
                "(no NSFW on SFW platforms) and ToS compliance.\n"
                "- Approve, or return it with specific notes.\n"
                "- Continuously refine your rubric from what performs vs. flops, and write learnings to the Playbook.")
    if kind == "platform":
        plat = name.split(":", 1)[-1]
        return ("ROLE — " + plat.capitalize() + " specialist. Research what's working on " + plat + " right now and keep the Playbook current.\n"
                "- Track trends, formats, sounds, hashtags, best posting times and algorithm changes on " + plat + ".\n"
                "- Write concrete, current best practices to the shared Playbook under '" + plat + "'.\n"
                "- Only recommend tactics that comply with " + plat + "'s ToS and keep accounts safe.")
    if kind == "function":
        fn = name.split(":", 1)[-1]
        m = {
            "content_creator": "Research the best-performing content ideas, hooks and formats across platforms; teach the model agents and write findings to the Playbook.",
            "comment_dm": "Define best practices for replying to comments and DMs in-voice and funneling fans to subscriptions — genuine, prompt, never spammy. Teach the model agents.",
            "affiliate": "Research how to promote affiliate links naturally and profitably; teach the model agents where and how to place them.",
            "shop": "Research running and promoting TikTok/X/Shopify shops; teach the model agents how to drive sales.",
            "subscription": "Research how to convert followers into X and Fanvue subscribers; teach the model agents the best funnels and offers.",
        }
        return "ROLE — " + m.get(fn, "Teach the model agents your specialty and write findings to the Playbook.")
    if name == "ceo":
        return ("ROLE — CEO of the org. Own overall results.\n"
                "- Track the org scoreboard daily; set weekly priorities across teams.\n"
                "- Keep department heads and managers accountable; unblock teams.\n"
                "- Watch org-wide agent health and compliance.")
    if name.startswith("dept_head:"):
        d = name.split(":", 1)[-1]
        return ("ROLE — Head of " + d.capitalize() + ". Oversee your area, roll performance up to the CEO, "
                "and support your reports with priorities and unblocking.")
    if name.startswith("support:"):
        s = name.split(":", 1)[-1]
        m = {
            "onboarding": "Provision everything a new persona needs (email/proxy/AdsPower profile/platform setup). NOTE: the actual account SIGN-UPS (CAPTCHA/phone verification) are done by Sam; prepare everything else so a new persona can go live fast.",
            "compliance": "Track each platform's evolving ToS and AI-disclosure rules. Keep the org compliant so accounts stay alive; warn agents before any step that would break a platform's rules.",
            "accounting": "Track revenue and expenses per persona and team once money flows; keep the books.",
            "reporting": "Produce regular performance reports from the scoreboard and metrics for Sam and the CEO agent.",
        }
        return "ROLE — " + m.get(s, "Support the org.")
    return "ROLE — Support the org's goals."

def apply_default_sops(overwrite=False):
    con = db.connect()
    rows = con.execute("SELECT a.id, a.name, a.kind, a.config_json, p.name pname, p.geo geo, t.name tname "
                       "FROM agents a LEFT JOIN personas p ON p.id=a.persona_id "
                       "LEFT JOIN teams t ON t.id=a.team_id").fetchall()
    for r in rows:
        cfg = json.loads(r["config_json"] or "{}")
        if cfg.get("sop") and not overwrite:
            continue
        cfg["sop"] = default_sop(r["kind"], r["name"], r["pname"], r["geo"], r["tname"])
        con.execute("UPDATE agents SET config_json=? WHERE id=?", (json.dumps(cfg), r["id"]))
    con.commit(); con.close()

def get_sop(aid):
    con = db.connect()
    r = con.execute("SELECT config_json FROM agents WHERE id=?", (aid,)).fetchone()
    con.close()
    return json.loads(r["config_json"] or "{}").get("sop", "") if r else ""

def set_sop(aid, sop):
    con = db.connect()
    r = con.execute("SELECT config_json FROM agents WHERE id=?", (aid,)).fetchone()
    if r:
        cfg = json.loads(r["config_json"] or "{}"); cfg["sop"] = sop
        con.execute("UPDATE agents SET config_json=? WHERE id=?", (json.dumps(cfg), aid))
        con.commit()
    con.close()

def init_playbooks():
    con = db.connect()
    con.execute("CREATE TABLE IF NOT EXISTS playbooks(scope TEXT PRIMARY KEY, body TEXT, updated_at REAL)")
    con.commit(); con.close()

def seed_playbooks(force=False):
    init_playbooks()
    con = db.connect()
    for scope, body in PLAYBOOK_SEED.items():
        if force:
            con.execute("INSERT INTO playbooks(scope,body,updated_at) VALUES(?,?,?) "
                        "ON CONFLICT(scope) DO UPDATE SET body=excluded.body, updated_at=excluded.updated_at",
                        (scope, body, time.time()))
        else:
            con.execute("INSERT OR IGNORE INTO playbooks(scope,body,updated_at) VALUES(?,?,?)",
                        (scope, body, time.time()))
    con.commit(); con.close()

def get_playbooks():
    init_playbooks()
    con = db.connect()
    rows = con.execute("SELECT scope, body, updated_at FROM playbooks ORDER BY scope").fetchall()
    con.close()
    return [dict(r) for r in rows]

def set_playbook(scope, body):
    init_playbooks()
    con = db.connect()
    con.execute("INSERT INTO playbooks(scope,body,updated_at) VALUES(?,?,?) "
                "ON CONFLICT(scope) DO UPDATE SET body=excluded.body, updated_at=excluded.updated_at",
                (scope, body, time.time()))
    con.commit(); con.close()
