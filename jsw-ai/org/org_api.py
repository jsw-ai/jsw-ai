"""JSW AI org — control panel (Flask).

Password-protected. First visit sets the admin password (never transits chat).
Pages: scoreboard, org chart / agents, and a secure vault input for credentials.
Runs on :5061.
"""
import sys, os, json, time, secrets as _secrets
sys.path.insert(0, os.path.dirname(__file__))
import db, vault, scoreboard, build_org, metrics, board, org_page, sops, playbooks_page
import model_data, model_page, tag_page, zen_client, studio_page, posts, approvals_page
from flask import Flask, request, session, redirect, url_for, Response, send_file, abort
from werkzeug.security import generate_password_hash, check_password_hash

BASE = os.path.dirname(__file__)
FLASK_KEY_PATH = os.path.join(BASE, "secrets", "flask.key")

def _settings_init():
    con = db.connect()
    con.execute("CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, value TEXT)")
    con.commit(); con.close()

def setting_get(k):
    _settings_init()
    con = db.connect()
    r = con.execute("SELECT value FROM settings WHERE key=?", (k,)).fetchone()
    con.close()
    return r["value"] if r else None

def setting_set(k, v):
    _settings_init()
    con = db.connect()
    con.execute("INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (k, v))
    con.commit(); con.close()

def _flask_secret():
    if not os.path.exists(FLASK_KEY_PATH):
        os.makedirs(os.path.dirname(FLASK_KEY_PATH), exist_ok=True)
        fd = os.open(FLASK_KEY_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        os.write(fd, _secrets.token_hex(32).encode()); os.close(fd)
    return open(FLASK_KEY_PATH).read()

app = Flask(__name__)
app.secret_key = _flask_secret()
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_prefix=1)
from datetime import timedelta
app.permanent_session_lifetime = timedelta(days=30)

CSS = """<style>
body{font-family:-apple-system,Segoe UI,Roboto,sans-serif;background:#0f1115;color:#e6e6e6;margin:0}
a{color:#7aa2f7;text-decoration:none} .wrap{max-width:1100px;margin:0 auto;padding:24px}
nav{background:#161922;padding:12px 24px;border-bottom:1px solid #262b36}
nav a{margin-right:18px;font-weight:600}
h1{font-size:22px} h2{font-size:16px;color:#9aa5b1;margin-top:28px}
table{width:100%;border-collapse:collapse;margin-top:8px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid #222732;font-size:14px}
th{color:#9aa5b1;font-weight:600}
.card{background:#161922;border:1px solid #262b36;border-radius:10px;padding:16px;margin-top:12px}
.pill{display:inline-block;padding:2px 8px;border-radius:12px;font-size:12px;background:#222732}
.run{background:#1f3d2b;color:#7ee2a8}.idle{background:#2a2f3a;color:#9aa5b1}.err{background:#3d1f1f;color:#f7a2a2}
input,select{background:#0f1115;border:1px solid #333a48;color:#e6e6e6;padding:8px;border-radius:6px;width:100%;box-sizing:border-box}
button{background:#7aa2f7;color:#0f1115;border:0;padding:9px 16px;border-radius:6px;font-weight:700;cursor:pointer}
label{display:block;margin-top:10px;font-size:13px;color:#9aa5b1}
</style>"""

def page(body, nav=True):
    if nav:
        n = ('<nav><a href="%s">Scoreboard</a><a href="%s">Models</a><a href="%s">Studio</a><a href="%s">Approvals</a><a href="%s">Tag</a><a href="%s">Org</a><a href="%s">Playbooks</a><a href="%s">Vault</a>'
             '<a href="%s" style="float:right">Logout</a></nav>' %
             (url_for("home"), url_for("models_index"), url_for("studio_root"), url_for("approvals_route"), url_for("tag_page_route"), url_for("org"), url_for("playbooks_page_route"), url_for("vault_page"), url_for("logout")))
    else:
        n = ""
    try:
        root = url_for("home").rstrip("/")
    except Exception:
        root = ""
    rootjs = '<script>window.ORG_ROOT=%s;</script>' % json.dumps(root)
    return Response(CSS + rootjs + n + '<div class="wrap">' + body + '</div>', mimetype="text/html")

def logged_in():
    return session.get("auth") is True

def require(f):
    def g(*a, **k):
        if not setting_get("admin_hash"):
            return redirect(url_for("setup"))
        if not logged_in():
            return redirect(url_for("login"))
        return f(*a, **k)
    g.__name__ = f.__name__
    return g

def _cred_form(title, sub, btn, err=""):
    return page('<h1>' + title + '</h1>' + (('<p>' + sub + '</p>') if sub else '') + err +
                '<form method=post><label>Username</label><input name=user autocomplete=username>'
                '<label>Password</label><input name=pw type=password autocomplete=current-password>'
                '<button style="margin-top:14px">' + btn + '</button></form>', nav=False)

@app.route("/setup", methods=["GET", "POST"])
def setup():
    if setting_get("admin_hash"):
        return redirect(url_for("login"))
    if request.method == "POST":
        user = request.form.get("user", "").strip()
        pw = request.form.get("pw", "")
        if len(user) < 3 or len(pw) < 8:
            return _cred_form("Create your login", "", "Create login",
                              '<p style="color:#f7a2a2">Username min 3 characters, password min 8.</p>')
        setting_set("admin_user", user)
        setting_set("admin_hash", generate_password_hash(pw))
        session.permanent = True
        session["auth"] = True
        return redirect(url_for("home"))
    return _cred_form("Welcome to JSW Org",
                      "Create your login once — you'll stay signed in after that. Set here in your browser, never sent through chat.",
                      "Create login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if not setting_get("admin_hash"):
        return redirect(url_for("setup"))
    err = ""
    if request.method == "POST":
        u = request.form.get("user", "").strip()
        p = request.form.get("pw", "")
        if u == (setting_get("admin_user") or "") and check_password_hash(setting_get("admin_hash"), p):
            session.permanent = True
            session["auth"] = True
            return redirect(url_for("home"))
        err = '<p style="color:#f7a2a2">Wrong username or password.</p>'
    return _cred_form("JSW Org — Login", "", "Log in", err)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
@require
def home():
    return page(board.BODY)

@app.route("/api/board")
@require
def api_board():
    return Response(json.dumps(metrics.board_data()), mimetype="application/json")

def role_title(name, kind, pname=None):
    if name == "ceo": return "CEO"
    if name.startswith("dept_head:"): return "Head of " + name.split(":", 1)[1].capitalize()
    if name.startswith("manager:"):
        t = name.split(":", 1)[1]
        return ("Platforms" if t == "platforms" else t) + " · Manager"
    if name.startswith("reviewer:"): return name.split(":", 1)[1] + " · Content Reviewer"
    if name.startswith("model:"): return (pname or name.split(":", 1)[1].title()) + " · Model"
    if name.startswith("platform:"): return name.split(":", 1)[1].capitalize() + " Specialist"
    if name.startswith("function:"): return name.split(":", 1)[1].replace("_", " ").title()
    if name.startswith("support:"): return name.split(":", 1)[1].capitalize()
    return name

def _agents_full():
    con = db.connect()
    rows = con.execute("SELECT a.*, p.name pname, p.slug pslug, t.name tname FROM agents a "
                       "LEFT JOIN personas p ON p.id=a.persona_id "
                       "LEFT JOIN teams t ON t.id=a.team_id").fetchall()
    tasks = con.execute("SELECT agent_id, title FROM tasks WHERE status IN ('in_progress','pending') "
                        "ORDER BY priority, created_at").fetchall()
    con.close()
    curtask = {}
    for tk in tasks:
        curtask.setdefault(tk["agent_id"], tk["title"])
    out = []
    for a in rows:
        cfg = json.loads(a["config_json"] or "{}")
        out.append({"id": a["id"], "name": a["name"], "kind": a["kind"], "status": a["status"],
                    "title": role_title(a["name"], a["kind"], a["pname"]),
                    "persona": a["pname"], "slug": a["pslug"], "team": a["tname"],
                    "reports_to": cfg.get("reports_to"), "interval": cfg.get("interval"),
                    "last_beat": cfg.get("last_beat"), "current_task": curtask.get(a["id"])})
    return out

@app.route("/org")
@require
def org():
    return page(org_page.BODY)

@app.route("/api/org")
@require
def api_org():
    return Response(json.dumps({"agents": _agents_full()}), mimetype="application/json")

@app.route("/api/agent/<int:aid>")
@require
def api_agent(aid):
    allx = _agents_full()
    me = next((a for a in allx if a["id"] == aid), None)
    if not me:
        return Response("{}", mimetype="application/json")
    byname = {a["name"]: a for a in allx}
    boss = byname.get(me["reports_to"])
    me["reports_to_obj"] = {"id": boss["id"], "title": boss["title"]} if boss else None
    me["direct_reports"] = [{"id": a["id"], "title": a["title"]} for a in allx if a["reports_to"] == me["name"]]
    con = db.connect()
    ev = con.execute("SELECT ts, detail_json FROM events WHERE actor=? ORDER BY ts DESC LIMIT 25",
                     ("agent:%d" % aid,)).fetchall()
    con.close()
    me["log"] = [{"ts": e["ts"], "msg": json.loads(e["detail_json"] or "{}").get("msg", "")} for e in ev]
    me["sop"] = sops.get_sop(aid)
    return Response(json.dumps(me), mimetype="application/json")

@app.route("/api/sop/<int:aid>", methods=["POST"])
@require
def api_sop_set(aid):
    data = request.get_json(silent=True) or request.form
    sops.set_sop(aid, data.get("sop", ""))
    db.log_event("agent:%d" % aid, "log", {"msg": "Instructions (SOP) updated by operator"})
    return Response(json.dumps({"ok": True}), mimetype="application/json")

@app.route("/playbooks")
@require
def playbooks_page_route():
    return page(playbooks_page.BODY)

@app.route("/api/playbook")
@require
def api_playbook():
    return Response(json.dumps(sops.get_playbooks()), mimetype="application/json")

@app.route("/api/playbook/set", methods=["POST"])
@require
def api_playbook_set():
    data = request.get_json(silent=True) or request.form
    sops.set_playbook(data.get("scope", ""), data.get("body", ""))
    return Response(json.dumps({"ok": True}), mimetype="application/json")

@app.route("/api/activity")
@require
def api_activity():
    allx = {a["id"]: a for a in _agents_full()}
    con = db.connect()
    ev = con.execute("SELECT ts, actor, detail_json FROM events WHERE actor LIKE 'agent:%' "
                     "ORDER BY ts DESC LIMIT 60").fetchall()
    con.close()
    out = []
    for e in ev:
        try:
            aid = int(e["actor"].split(":")[1])
        except Exception:
            continue
        a = allx.get(aid)
        out.append({"ts": e["ts"], "title": a["title"] if a else e["actor"],
                    "kind": a["kind"] if a else "", "msg": json.loads(e["detail_json"] or "{}").get("msg", "")})
    return Response(json.dumps(out), mimetype="application/json")

@app.route("/api/agent/<int:aid>/<action>", methods=["POST"])
@require
def api_agent_ctl(aid, action):
    status = {"start": "running", "stop": "idle"}.get(action)
    if status:
        con = db.connect()
        con.execute("UPDATE agents SET status=? WHERE id=?", (status, aid))
        con.commit(); con.close()
        db.log_event("agent:%d" % aid, "log",
                     {"msg": "Agent %s by operator" % ("started" if status == "running" else "stopped")})
    return Response(json.dumps({"ok": True, "status": status}), mimetype="application/json")

@app.route("/models")
@require
def models_index():
    return page(model_page.INDEX)

@app.route("/model/<slug>")
@require
def model_view(slug):
    return page(model_page.BODY)

@app.route("/api/model/<slug>")
@require
def api_model(slug):
    data = model_data.model_json(slug)
    if not data:
        return Response(json.dumps({"error": "not found"}), status=404, mimetype="application/json")
    return Response(json.dumps(data), mimetype="application/json")

@app.route("/model/<slug>/<gallery>/<int:i>")
@require
def model_img(slug, gallery, i):
    imgs = model_data.persona_media(slug, category=gallery)
    if i < 0 or i >= len(imgs):
        abort(404)
    return send_file(imgs[i])

@app.route("/tag")
@require
def tag_page_route():
    return page(tag_page.BODY)

@app.route("/api/untagged")
@require
def api_untagged():
    return Response(json.dumps({"images": model_data.untagged_images()}), mimetype="application/json")

@app.route("/api/tag/set", methods=["POST"])
@require
def api_tag_set():
    data = request.get_json(silent=True) or request.form
    ok = model_data.set_photo_tag(int(data.get("idx", -1)), data.get("slug", ""), data.get("category", ""))
    return Response(json.dumps({"ok": bool(ok)}), mimetype="application/json")

@app.route("/content_img/<int:idx>")
@require
def content_img(idx):
    p = model_data.image_by_index(idx)
    if not p:
        abort(404)
    return send_file(p)

@app.route("/api/post_media/<int:pid>/<int:n>")
@require
def api_post_media(pid, n):
    """Serve the nth media file (0 = main path) of a content_items post — image OR video."""
    con = db.connect()
    r = con.execute("SELECT path, extra_paths FROM content_items WHERE id=?", (pid,)).fetchone()
    con.close()
    if not r:
        abort(404)
    paths = [r["path"]]
    try:
        paths += json.loads((r["extra_paths"] if "extra_paths" in r.keys() else "") or "[]")
    except Exception:
        pass
    if n < 0 or n >= len(paths) or not paths[n] or not os.path.isfile(paths[n]):
        abort(404)
    return send_file(paths[n])

@app.route("/model/<slug>/ref/<which>")
@app.route("/model/<slug>/ref/<which>/<int:i>")
@require
def model_ref(slug, which, i=0):
    if which not in ("face", "body", "back", "waist", "xfanvue"):
        abort(404)
    p = model_data.reference_image(slug, which, i)
    if not p:
        abort(404)
    return send_file(p)

@app.route("/api/ref/upload", methods=["POST"])
@require
def api_ref_upload():
    slug = request.form.get("slug", "")
    which = request.form.get("which", "")
    f = request.files.get("file")
    if which not in ("face", "body", "back", "waist", "xfanvue") or not f or not slug:
        return Response(json.dumps({"error": "need slug, which=face|body|back, file"}), mimetype="application/json")
    ext = (f.filename or "x.png").rsplit(".", 1)[-1].lower()
    if ext not in ("png", "webp", "jpg", "jpeg"):
        ext = "png"
    try:
        dest = model_data.add_reference(slug, which, data=f.read(), ext=ext)
        return Response(json.dumps({"ok": True, "path": dest,
                                    "count": len(model_data.reference_images(slug, which))}),
                        mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"error": str(e)[:200]}), mimetype="application/json")

@app.route("/api/ref/promote", methods=["POST"])
@require
def api_ref_promote():
    d = request.get_json(silent=True) or {}
    slug, which = d.get("slug", ""), d.get("which", "body")
    if which not in ("face", "body", "back", "waist", "xfanvue"):
        return Response(json.dumps({"error": "which must be face|body|back|waist|xfanvue"}), mimetype="application/json")
    try:
        imgs = model_data.persona_media(slug, category=d.get("category", "sfw"))
        idx = int(d.get("idx", -1))
        if not (0 <= idx < len(imgs)):
            return Response(json.dumps({"error": "bad image index"}), mimetype="application/json")
        dest = model_data.add_reference(slug, which, src_path=imgs[idx])
        return Response(json.dumps({"ok": True, "path": dest,
                                    "count": len(model_data.reference_images(slug, which))}),
                        mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"error": str(e)[:200]}), mimetype="application/json")

@app.route("/studio")
@require
def studio_root():
    return redirect(url_for("studio_view", slug="sienna"))

@app.route("/studio/<slug>")
@require
def studio_view(slug):
    return page(studio_page.BODY)

@app.route("/api/zen/tools")
@require
def api_zen_tools():
    try:
        return Response(json.dumps(zen_client.list_tools()), mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"error": str(e)[:200], "tools": []}), mimetype="application/json")

@app.route("/api/zen/tool/<name>")
@require
def api_zen_tool(name):
    try:
        return Response(json.dumps(zen_client.tool_detail(name)), mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"error": str(e)[:200]}), mimetype="application/json")

@app.route("/api/zen/generate", methods=["POST"])
@require
def api_zen_generate():
    data = request.get_json(silent=True) or {}
    try:
        gid = zen_client.create_generation(data.get("slug", ""), data.get("category", "sfw"),
                                           data.get("tool", ""), data.get("input") or {})
        return Response(json.dumps({"id": gid}), mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"error": str(e)[:300]}), mimetype="application/json")

@app.route("/api/zen/status/<gid>")
@require
def api_zen_status(gid):
    try:
        return Response(json.dumps(zen_client.poll(gid)), mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"gid": gid, "status": "unknown", "error": str(e)[:200]}), mimetype="application/json")

@app.route("/api/zen/jobs/<slug>")
@require
def api_zen_jobs(slug):
    try:
        return Response(json.dumps({"jobs": zen_client.jobs_for(slug)}), mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"jobs": [], "error": str(e)[:200]}), mimetype="application/json")

@app.route("/api/zen/upload", methods=["POST"])
@require
def api_zen_upload():
    f = request.files.get("file")
    if not f:
        return Response(json.dumps({"error": "no file"}), mimetype="application/json")
    tmp = os.path.join("/tmp", "zen_up_" + (f.filename or "img").replace("/", "_"))
    f.save(tmp)
    try:
        aid = zen_client.upload_asset(tmp)
        return Response(json.dumps({"asset_id": aid}), mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"error": str(e)[:300]}), mimetype="application/json")

@app.route("/api/ref/delete", methods=["POST"])
@require
def api_ref_delete():
    data = request.get_json(silent=True) or {}
    try:
        p = model_data.reference_image(data.get("slug", ""), data.get("which", ""),
                                       int(data.get("i") or 0))
        if not p:
            raise RuntimeError("no such reference photo")
        os.remove(p)
        con = db.connect()
        con.execute("DELETE FROM zen_assets WHERE path=?", (p,))
        con.commit(); con.close()
        db.log_event("model", "ref_delete", {"msg": "removed %s ref for %s" % (data.get("which"), data.get("slug"))})
        return Response(json.dumps({"ok": 1}), mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"error": str(e)[:200]}), mimetype="application/json")

@app.route("/api/zen/templates")
@require
def api_zen_templates():
    try:
        return Response(json.dumps(zen_client.templates(
            q=request.args.get("q") or None, tool=request.args.get("tool") or None,
            page=int(request.args.get("page") or 1), per=int(request.args.get("per") or 24))),
            mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"error": str(e)[:200], "templates": [], "total": 0}),
                        mimetype="application/json")

@app.route("/api/zen/enhance", methods=["POST"])
@require
def api_zen_enhance():
    data = request.get_json(silent=True) or {}
    try:
        name = None
        if data.get("slug"):
            try:
                name = (model_data.model_json(data["slug"]) or {}).get("name")
            except Exception:
                name = str(data["slug"]).title()
        return Response(json.dumps({"text": zen_client.enhance_prompt(data.get("text") or "", name)}),
                        mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"error": str(e)[:200]}), mimetype="application/json")

@app.route("/api/zen/retry", methods=["POST"])
@require
def api_zen_retry():
    data = request.get_json(silent=True) or {}
    try:
        gid = zen_client.retry(data.get("gid") or "")
        return Response(json.dumps({"id": gid}), mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"error": str(e)[:300]}), mimetype="application/json")

@app.route("/api/zen/file/<gid>/<int:n>")
@require
def api_zen_file(gid, n):
    p = zen_client.file_path(gid, n)
    if not p:
        abort(404)
    return send_file(p)

@app.route("/api/posts/<slug>")
@require
def api_posts(slug):
    try:
        return Response(json.dumps({"posts": posts.list_posts(slug)}), mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"posts": [], "error": str(e)[:200]}), mimetype="application/json")

@app.route("/api/post/create", methods=["POST"])
@require
def api_post_create():
    d = request.get_json(silent=True) or {}
    try:
        pid = posts.create_post(d.get("slug", ""), d.get("category", "sfw"), int(d.get("idx", -1)),
                                d.get("platform", ""), d.get("caption", ""), d.get("hashtags", ""),
                                d.get("slot_time", ""), d.get("extra_idxs") or [])
        return Response(json.dumps({"id": pid}), mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"error": str(e)[:200]}), mimetype="application/json")

@app.route("/api/post/update", methods=["POST"])
@require
def api_post_update():
    d = request.get_json(silent=True) or {}
    try:
        posts.update_post(int(d.get("id", 0)), d)
        return Response(json.dumps({"ok": True}), mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"error": str(e)[:200]}), mimetype="application/json")

@app.route("/api/post/delete", methods=["POST"])
@require
def api_post_delete():
    d = request.get_json(silent=True) or {}
    try:
        posts.delete_post(int(d.get("id", 0)))
        return Response(json.dumps({"ok": True}), mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"error": str(e)[:200]}), mimetype="application/json")

@app.route("/api/post/gen_caption", methods=["POST"])
@require
def api_post_gen_caption():
    d = request.get_json(silent=True) or {}
    try:
        out = posts.gen_caption(d.get("slug", ""), d.get("platform", "instagram"), d.get("hint", ""))
        return Response(json.dumps(out), mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"error": str(e)[:200]}), mimetype="application/json")

@app.route("/api/golive", methods=["GET", "POST"])
@require
def api_golive():
    con = db.connect()
    if request.method == "POST":
        d = request.get_json(silent=True) or {}
        val = "1" if d.get("on") else "0"
        con.execute("INSERT OR REPLACE INTO settings(key, value) VALUES('go_live', ?)", (val,))
        con.commit()
        db.log_event("poster", "go_live", {"msg": "live posting turned %s from Approvals page"
                                           % ("ON" if val == "1" else "OFF")})
    row = con.execute("SELECT value FROM settings WHERE key='go_live'").fetchone()
    con.close()
    return Response(json.dumps({"on": bool(row and row["value"] == "1")}),
                    mimetype="application/json")

@app.route("/exports")
@require
def exports_page():
    base = "/opt/jsw-ai/exports"
    files = sorted(f for f in os.listdir(base) if f.endswith(".zip")) if os.path.isdir(base) else []
    links = "".join('<li style="margin:10px 0;font-size:16px"><a href="%s">%s</a> '
                    '<span style="color:#6b7280;font-size:13px">(%.1f MB)</span></li>'
                    % (url_for("export_file", fname=f), f,
                       os.path.getsize(os.path.join(base, f)) / 1048576.0) for f in files)
    return page("<h1>Downloads</h1><div class='card'><ul style='list-style:none;padding:0;margin:0'>%s</ul></div>"
                % (links or "<p style='color:#6b7280'>No files yet — check back shortly.</p>"))

@app.route("/export/<path:fname>")
@require
def export_file(fname):
    base = "/opt/jsw-ai/exports"
    p = os.path.normpath(os.path.join(base, fname))
    if not (p.startswith(base + "/") and os.path.isfile(p)):
        abort(404)
    return send_file(p, as_attachment=True)

@app.route("/api/photo/upload", methods=["POST"])
@require
def api_photo_upload():
    slug = request.form.get("slug", "")
    category = request.form.get("category", "sfw")
    if category not in ("sfw", "x", "fanvue"):
        return Response(json.dumps({"error": "bad folder"}), mimetype="application/json")
    files = request.files.getlist("file")
    if not files:
        return Response(json.dumps({"error": "no files"}), mimetype="application/json")
    dest_dir = os.path.join("/opt/jsw-ai/content/uploads", slug)
    os.makedirs(dest_dir, exist_ok=True)
    con = db.connect()
    n = 0
    for f in files:
        name = os.path.basename(f.filename or "photo.png").replace(" ", "_").replace("/", "_")
        if not name.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            continue
        p = os.path.join(dest_dir, "%d_%s" % (int(time.time() * 1000) + n, name))
        f.save(p)
        con.execute("INSERT OR REPLACE INTO photo_tags(path, slug, category) VALUES(?,?,?)",
                    (p, slug, category))
        n += 1
    con.commit(); con.close()
    db.log_event("model", "photo_upload", {"msg": "%d photo(s) uploaded to %s/%s" % (n, slug, category)})
    return Response(json.dumps({"ok": 1, "count": n}), mimetype="application/json")

@app.route("/api/post/create_global", methods=["POST"])
@require
def api_post_create_global():
    d = request.get_json(silent=True) or {}
    try:
        pid = posts.create_post_global(d.get("slug", ""), d.get("platform", ""),
                                       d.get("caption", ""), d.get("hashtags", ""),
                                       d.get("slot_time", ""), d.get("idxs") or [])
        return Response(json.dumps({"id": pid}), mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"error": str(e)[:200]}), mimetype="application/json")

@app.route("/api/post/set_slides", methods=["POST"])
@require
def api_post_set_slides():
    d = request.get_json(silent=True) or {}
    try:
        posts.set_slides(int(d.get("id", 0)), d.get("idxs") or [])
        return Response(json.dumps({"ok": True}), mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"error": str(e)[:200]}), mimetype="application/json")

@app.route("/api/post/gen_captions3", methods=["POST"])
@require
def api_post_gen_captions3():
    d = request.get_json(silent=True) or {}
    try:
        out = posts.gen_captions3(d.get("slug", ""), d.get("platform", "instagram"), d.get("hint", ""))
        return Response(json.dumps(out), mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"error": str(e)[:200]}), mimetype="application/json")

@app.route("/api/lib_idxs/<slug>/<category>")
@require
def api_lib_idxs(slug, category):
    try:
        return Response(json.dumps({"idxs": posts.lib_global_idxs(slug, category)}),
                        mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"idxs": [], "error": str(e)[:200]}), mimetype="application/json")

def _photo_path(d):
    imgs = model_data.persona_media(d.get("slug", ""), category=d.get("category", "sfw"))
    idx = int(d.get("idx", -1))
    if not (0 <= idx < len(imgs)):
        return None
    return imgs[idx]

@app.route("/api/photo/delete", methods=["POST"])
@require
def api_photo_delete():
    d = request.get_json(silent=True) or {}
    p = _photo_path(d)
    if not p:
        return Response(json.dumps({"error": "bad photo"}), mimetype="application/json")
    con = db.connect()
    used = con.execute("SELECT COUNT(*) c FROM content_items WHERE path=? OR "
                       "(extra_paths IS NOT NULL AND extra_paths LIKE ?)",
                       (p, "%" + p + "%")).fetchone()["c"]
    if used:
        con.close()
        return Response(json.dumps({"error": "photo is used in %d post(s) - delete those posts first" % used}),
                        mimetype="application/json")
    con.execute("DELETE FROM photo_tags WHERE path=?", (p,))
    con.commit(); con.close()
    try:
        os.remove(p)
    except OSError as e:
        return Response(json.dumps({"error": str(e)[:120]}), mimetype="application/json")
    return Response(json.dumps({"ok": True}), mimetype="application/json")

@app.route("/api/photo/move", methods=["POST"])
@require
def api_photo_move():
    d = request.get_json(silent=True) or {}
    p = _photo_path(d)
    ts, tc = d.get("to_slug", ""), d.get("to_category", "sfw")
    if not p or tc not in ("sfw", "x", "fanvue") or not ts:
        return Response(json.dumps({"error": "bad request"}), mimetype="application/json")
    con = db.connect()
    con.execute("INSERT OR REPLACE INTO photo_tags(path, slug, category) VALUES(?,?,?)", (p, ts, tc))
    con.commit(); con.close()
    return Response(json.dumps({"ok": True}), mimetype="application/json")

@app.route("/api/photo/save_edit", methods=["POST"])
@require
def api_photo_save_edit():
    d = {"slug": request.form.get("slug", ""), "category": request.form.get("category", "sfw"),
         "idx": request.form.get("idx", -1)}
    p = _photo_path(d)
    f = request.files.get("file")
    mode = request.form.get("mode", "copy")
    if not p or not f:
        return Response(json.dumps({"error": "bad request"}), mimetype="application/json")
    data = f.read()
    try:
        if mode == "overwrite":
            try:
                from PIL import Image
                import io as _io
                img = Image.open(_io.BytesIO(data))
                if p.lower().endswith((".jpg", ".jpeg")):
                    img = img.convert("RGB")
                img.save(p)
            except ImportError:
                import time as _t
                np_ = p.rsplit(".", 1)[0] + "_edit%d.png" % int(_t.time())
                open(np_, "wb").write(data)
                con = db.connect()
                row = con.execute("SELECT slug, category FROM photo_tags WHERE path=?", (p,)).fetchone()
                con.execute("INSERT OR REPLACE INTO photo_tags(path, slug, category) VALUES(?,?,?)",
                            (np_, row["slug"] if row else d["slug"], row["category"] if row else d["category"]))
                con.commit(); con.close()
            return Response(json.dumps({"ok": True}), mimetype="application/json")
        import time as _t
        np_ = "%s/edit_%d.png" % (p.rsplit("/", 1)[0], int(_t.time()))
        open(np_, "wb").write(data)
        con = db.connect()
        con.execute("INSERT OR REPLACE INTO photo_tags(path, slug, category) VALUES(?,?,?)",
                    (np_, d["slug"], d["category"]))
        con.commit(); con.close()
        return Response(json.dumps({"ok": True}), mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"error": str(e)[:200]}), mimetype="application/json")

@app.route("/approvals")
@require
def approvals_route():
    return page(approvals_page.BODY)

@app.route("/api/approvals")
@require
def api_approvals():
    try:
        con = db.connect()
        rows = con.execute(
            "SELECT ci.*, p.name pname, p.slug pslug FROM content_items ci "
            "JOIN personas p ON p.id=ci.persona_id "
            "ORDER BY CASE WHEN ci.status='pending_review' THEN 0 ELSE 1 END, "
            "ci.updated_at DESC, ci.id DESC").fetchall()
        con.close()
        imgs = model_data._all_images()
        pos = {pth: i for i, pth in enumerate(imgs)}
        out = []
        for r in rows:
            try:
                extras = json.loads((r["extra_paths"] if "extra_paths" in r.keys() else "") or "[]")
            except Exception:
                extras = []
            idxs = [pos.get(r["path"])] + [pos.get(p) for p in extras]
            p0 = (r["path"] or "").lower()
            is_video = p0.endswith((".mp4", ".mov", ".webm", ".m4v"))
            out.append({"id": r["id"], "pname": r["pname"], "pslug": r["pslug"],
                        "platform": r["platform"], "caption": r["caption"] or "",
                        "hashtags": (r["hashtags"] if "hashtags" in r.keys() else "") or "",
                        "status": r["status"] or "draft", "slot_time": r["slot_time"] or "",
                        "review_notes": r["review_notes"] or "", "img_idx": pos.get(r["path"]),
                        "img_idxs": [i for i in idxs if i is not None],
                        "is_video": is_video, "nmedia": 1 + len(extras),
                        "created_at": r["created_at"]})
        return Response(json.dumps({"posts": out}), mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"posts": [], "error": str(e)[:200]}), mimetype="application/json")

# Credentials the platform actually needs: (persona, service, field, label, help)
NEEDED = [
    ("*", "x", "X_CONSUMER_KEY", "X — Consumer Key",
     "X developer app → Keys &amp; Tokens → <b>OAuth 1.0 Keys</b> → Consumer Key (~25 chars). NOT the OAuth 2.0 Client ID."),
    ("*", "x", "X_CONSUMER_SECRET", "X — Consumer Secret",
     "Same OAuth 1.0 section → Consumer Secret (~50 chars). NOT the OAuth 2.0 Client Secret."),
    ("madison", "ayrshare", "profile_key", "Ayrshare Profile Key — Madison",
     "Ayrshare dashboard → her profile → API Key (35 chars). Not the 40-char refId."),
    ("valentina", "ayrshare", "profile_key", "Ayrshare Profile Key — Valentina",
     "Ayrshare dashboard → her profile → API Key (35 chars)."),
    ("camille", "ayrshare", "profile_key", "Ayrshare Profile Key — Camille",
     "Link her socials in Ayrshare first, then copy the profile API Key."),
    ("gabriela", "ayrshare", "profile_key", "Ayrshare Profile Key — Gabriela",
     "Link her socials in Ayrshare first, then copy the profile API Key."),
    ("*", "fanvue", "FANVUE_CLIENT_ID", "Fanvue — OAuth Client ID",
     "Fanvue developer platform → your app credentials."),
    ("*", "fanvue", "FANVUE_CLIENT_SECRET", "Fanvue — OAuth Client Secret",
     "Fanvue developer platform → your app credentials."),
]

def _fv_badge():
    try:
        import fanvue_client
        return ("<span style='color:#7ee2a8'>connected</span>" if fanvue_client.connected()
                else "<span style='color:#f0a35e'>not connected &mdash; click to authorize</span>")
    except Exception as e:
        return "<span style='color:#f47174'>%s</span>" % str(e)[:60]

@app.route("/fanvue/connect")
@require
def fanvue_connect():
    import fanvue_client
    return redirect(fanvue_client.authorize_url())

@app.route("/fanvue/callback")
@require
def fanvue_callback():
    import fanvue_client
    if request.args.get("error"):
        return page("<h1>Fanvue</h1><p>Authorization failed: %s %s</p>"
                    % (request.args.get("error"), request.args.get("error_description", "")[:200]))
    try:
        fanvue_client.exchange(request.args.get("code", ""), request.args.get("state", ""))
        st, me = fanvue_client.api_get("/self")
        who = ""
        if isinstance(me, dict):
            who = me.get("handle") or me.get("displayName") or me.get("name") or ""
        return page("<h1>Fanvue connected &#10003;</h1><p>API self-check: HTTP %s %s</p>"
                    "<p><a href='%s'>Back to Vault</a></p>" % (st, who, url_for("vault_page")))
    except Exception as e:
        return page("<h1>Fanvue</h1><p>Connect failed: %s</p>" % str(e)[:250])

@app.route("/vault")
@require
def vault_page():
    meta = vault.list_secrets()
    have = {(m["persona"], m["service"], m["name"]) for m in meta}
    check, opts = [], []
    for i, (p, s, n, label, helptxt) in enumerate(NEEDED):
        ok = (p, s, n) in have
        check.append(
            "<tr><td>%s</td><td style='color:%s;font-weight:700'>%s</td>"
            "<td style='color:#6b7280;font-size:12px'>%s</td></tr>"
            % (label, "#7ee2a8" if ok else "#f7d67a", "stored" if ok else "missing", helptxt))
        opts.append("<option value='%d'>%s%s</option>" % (i, label, " (stored — will overwrite)" if ok else ""))
    rows = "".join(
        "<tr><td>%s</td><td>%s</td><td style='font-family:monospace'>%s</td>"
        "<td><form method=post action='%s' style='margin:0'>"
        "<input type=hidden name=persona value='%s'><input type=hidden name=service value='%s'>"
        "<input type=hidden name=name value='%s'>"
        "<button style='background:#3d1f1f;color:#f7a2a2;padding:4px 10px;font-size:12px'>Delete</button>"
        "</form></td></tr>"
        % (m["persona"], m["service"], (m["name"][:14] + "…") if len(m["name"]) > 15 else m["name"],
           url_for("vault_del"), m["persona"], m["service"], m["name"])
        for m in meta) or "<tr><td colspan=4 style='color:#6b7280'>Nothing stored yet.</td></tr>"
    slugs = [p["slug"] for p in db.get_personas()]
    popts = "".join("<option value='%s'>%s</option>" % (s, s) for s in (["*"] + slugs))
    body = ("<h1>Credential Vault</h1>"
            "<p style='color:#9aa5b1'>Only the <b>secret value</b> is encrypted. Never paste a key into the "
            "label fields &mdash; pick what you are adding from the list and put the key itself in the "
            "<b>Secret value</b> box.</p>"

            "<p style='margin:10px 0'><a href='" + url_for("fanvue_connect") + "'>&#9889; Connect Fanvue (one-time)</a> &mdash; " + _fv_badge() + "</p>"
            "<h2>What the platform still needs</h2>"
            "<table><tr><th>Credential</th><th>Status</th><th>Where to get it</th></tr>"
            + "".join(check) + "</table>"

            "<h2 style='margin-top:24px'>Add a credential</h2>"
            "<div class=card><form method=post action='" + url_for("vault_set") + "'>"
            "<label>What are you adding?</label>"
            "<select name=preset onchange=\"var c=this.value==='custom';"
            "document.getElementById('cust').style.display=c?'block':'none';\">"
            + "".join(opts) + "<option value='custom'>Something else (custom)</option></select>"
            "<div id='cust' style='display:none'>"
            "<label>Persona (or * for shared)</label><select name=persona>" + popts + "</select>"
            "<label>Service</label><input name=service placeholder='e.g. instagram, gmail, fanvue'>"
            "<label>Label for this field <span style='color:#6b7280'>(a name, NOT the key)</span></label>"
            "<input name=name placeholder='e.g. password, api_key'>"
            "</div>"
            "<label style='margin-top:10px'>Secret value <span style='color:#7ee2a8'>(this is the part that gets "
            "encrypted &mdash; paste the actual key here)</span></label>"
            "<input name=value type=password placeholder='paste the key / secret here'>"
            "<button style='margin-top:14px'>Save to vault</button></form></div>"

            "<h2 style='margin-top:24px'>Stored</h2>"
            "<table><tr><th>Persona</th><th>Service</th><th>Label</th><th></th></tr>" + rows + "</table>")
    return page(body)

@app.route("/vault/set", methods=["POST"])
@require
def vault_set():
    preset = request.form.get("preset", "custom")
    value = request.form.get("value", "")
    if preset != "custom":
        try:
            p, s, n = NEEDED[int(preset)][:3]
        except Exception:
            return redirect(url_for("vault_page"))
        persona, service, name = p, s, n
    else:
        persona = request.form.get("persona", "*").strip() or "*"
        service = request.form.get("service", "").strip()
        name = request.form.get("name", "").strip()
    if service and name and value:
        vault.set_secret(persona, service, name, value)
        db.log_event("vault", "set", {"persona": persona, "service": service, "name": name})
    return redirect(url_for("vault_page"))

@app.route("/vault/delete", methods=["POST"])
@require
def vault_del():
    try:
        vault.delete_secret(request.form.get("persona", ""), request.form.get("service", ""),
                            request.form.get("name", ""))
        db.log_event("vault", "delete", {"msg": "credential removed from vault"})
    except Exception:
        pass
    return redirect(url_for("vault_page"))

@app.route("/api/scoreboard")
@require
def api_scoreboard():
    return Response(json.dumps({"personas": scoreboard.persona_scores(),
                                "teams": scoreboard.team_scores()}), mimetype="application/json")

if __name__ == "__main__":
    db.init_db(); vault.init_vault(); metrics.seed_sample(); build_org.seed_activity()
    sops.apply_default_sops(); sops.seed_playbooks()
    app.run(host="0.0.0.0", port=5061)
