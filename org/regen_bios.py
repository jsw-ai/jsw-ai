"""Regenerate clean, structured persona profiles from the July master notes.

Faithful synthesis (do NOT invent facts) + derived affiliate lanes from real interests.
Writes: /opt/jsw-ai/org/data/bios.json (structured, engine reads this) and a review
HTML at /var/www/html/_tmp/bios_review.html for Sam to read in the browser.
"""
import sys, os, json, re, urllib.request, html
sys.path.insert(0, "/opt/jsw-ai/org")
import content_engine as ce  # reuse _grok / _env

MASTER = "/opt/jsw-ai/org/data/personas_master.json"
BIOS = "/opt/jsw-ai/org/data/bios.json"
OUT_HTML = "/var/www/html/_tmp/bios_review.html"

FACTS = {
    "sienna": "Sienna Blake, 24, Sydney Australia. Long-distance couple with Camille (Paris).",
    "camille": "Camille, 25, Paris France. Long-distance couple with Sienna (Australia).",
    "madison": "Madison Cole, 24, New York/Hoboken USA. Long-distance couple with Charlotte (UK).",
    "charlotte": "Charlotte Hayes, 23, England UK. Long-distance couple with Madison (US).",
    "valentina": "Valentina, 23, Miami (Colombian). Same-city couple with Gabriela (Miami).",
    "gabriela": "Gabriela, 24, Miami (Brazilian). Same-city couple with Valentina (Miami).",
}

SYS = ("You are cleaning up a virtual-influencer persona profile. Using ONLY the source notes and "
       "the confirmed facts, output STRICT JSON with keys: name, age, location, distance_status "
       "(exact: 'long-distance' or 'same-city'), personality (2-3 sentences), interests (array of "
       "short strings), fitness_angle (1-2 sentences on how fitness/wellness shows up in her content), "
       "affiliate_lanes (array of 3-5 concrete monetization lanes derived from her real interests, e.g. "
       "'activewear (Gymshark/Amazon)', 'thrifted fashion hauls'), content_pillars (array of 4-6 "
       "recurring post types), voice (1-2 sentences on how she writes/talks). Do NOT invent biography "
       "not supported by the notes. Keep it grounded and specific.")


def build(slug, block):
    u = ("CONFIRMED FACTS: %s\n\nSOURCE NOTES:\n%s\n\nOutput the JSON profile now."
         % (FACTS.get(slug, ""), block[:2600]))
    out = ce._grok(SYS, u, max_tokens=900, temp=0.4)
    m = re.search(r"\{.*\}", out, re.S)
    return json.loads(m.group(0)) if m else {"name": slug, "raw": out[:500]}


def render(profiles):
    rows = []
    for slug, p in profiles.items():
        def li(x):
            return "".join("<li>%s</li>" % html.escape(str(i)) for i in (x or []))
        rows.append(
            "<div class=card><h2>%s <small>(%s)</small></h2>"
            "<p><b>Location:</b> %s &nbsp; <b>Couple:</b> %s</p>"
            "<p><b>Personality:</b> %s</p>"
            "<p><b>Interests:</b> %s</p>"
            "<p><b>Fitness angle:</b> %s</p>"
            "<p><b>Affiliate lanes:</b></p><ul>%s</ul>"
            "<p><b>Content pillars:</b></p><ul>%s</ul>"
            "<p><b>Voice:</b> %s</p></div>"
            % (html.escape(str(p.get("name", slug))), html.escape(str(p.get("age", ""))),
               html.escape(str(p.get("location", ""))), html.escape(str(p.get("distance_status", ""))),
               html.escape(str(p.get("personality", ""))),
               html.escape(", ".join(p.get("interests", []) or [])),
               html.escape(str(p.get("fitness_angle", ""))),
               li(p.get("affiliate_lanes")), li(p.get("content_pillars")),
               html.escape(str(p.get("voice", "")))))
    css = ("body{font-family:-apple-system,Segoe UI,Roboto,sans-serif;max-width:820px;margin:24px auto;"
           "padding:0 16px;background:#0f1115;color:#e6e6e6}h1{color:#fff}.card{background:#171a21;"
           "border:1px solid #262b36;border-radius:12px;padding:16px 20px;margin:16px 0}"
           "h2{margin:0 0 6px;color:#8fb6ff}small{color:#8a94a6}b{color:#cfd6e4}ul{margin:4px 0 10px}"
           "li{margin:2px 0}")
    return ("<!doctype html><meta charset=utf-8><title>Persona Bios — Review</title><style>%s</style>"
            "<h1>Persona Bios — for review</h1><p style='color:#8a94a6'>Regenerated from the July master "
            "notes + confirmed facts. Tell Claude any corrections.</p>%s" % (css, "".join(rows)))


def main():
    master = json.load(open(MASTER))
    profiles = {}
    for slug in ["sienna", "camille", "madison", "charlotte", "valentina", "gabriela"]:
        block = master.get(slug, "")
        try:
            profiles[slug] = build(slug, block)
            print("BUILT", slug, flush=True)
        except Exception as e:
            print("FAIL", slug, str(e)[:120], flush=True)
    # merge into bios.json (keep bio text; add structured profile)
    bios = json.load(open(BIOS)) if os.path.exists(BIOS) else {}
    for slug, p in profiles.items():
        bios.setdefault(slug, {})["profile"] = p
    json.dump(bios, open(BIOS, "w"), indent=2)
    os.makedirs(os.path.dirname(OUT_HTML), exist_ok=True)
    open(OUT_HTML, "w").write(render(profiles))
    print("DONE ->", OUT_HTML, flush=True)


if __name__ == "__main__":
    main()
