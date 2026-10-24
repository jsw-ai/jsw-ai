#!/usr/bin/env python3
"""Drive a GeeLark cloud phone's screen over the shell API (Android 10/12-15): read the UI tree,
tap by text, take screenshots. Used for Sign-in-with-Google logins after Sam has signed in Gmail.

Never types passwords (CLAUDE.md); never proceeds past a sign-up screen (no account creation).

usage: phone_ui.py MODEL dump            print visible UI nodes
       phone_ui.py MODEL shot OUT.png    save a screenshot
       phone_ui.py MODEL tap REGEX       tap the first node whose text/desc matches
       phone_ui.py MODEL launch PACKAGE  open an app
       phone_ui.py MODEL accounts        Google accounts signed in (domain only)
"""
import json, re, sys, time, urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import geelark as g

# Screens that mean "this would create a new account" - stop, never continue.
SIGNUP = re.compile(r"when'?s your birthday|date of birth|create (a |your )?(username|account)|"
                    r"choose a username|sign up for|what should we call you|create your password", re.I)
# Screens a human must handle (CLAUDE.md: no CAPTCHA, no password entry) - escalate to Sam.
HUMAN = re.compile(r"captcha|verify (it'?s you|you'?re human)|drag the slider|select all images|"
                   r"enter (your )?password|puzzle", re.I)


class Phone:
    def __init__(self, model):
        self.model = model
        self.env = json.loads(g.PHONES.read_text())[model]["envId"]
        self.tok = g._token()

    def sh(self, cmd):
        d = g.call("/open/v1/shell/execute", {"id": self.env, "cmd": cmd}, self.tok)
        if not d.get("status"):
            raise RuntimeError(f"shell failed: {cmd!r}: {(d.get('output') or '')[:200]}")
        return d.get("output") or ""

    def nodes(self):
        xml = self.sh("uiautomator dump /sdcard/ui.xml >/dev/null 2>&1; cat /sdcard/ui.xml")
        xml = xml[xml.find("<?xml"):] if "<?xml" in xml else xml
        out = []
        for n in ET.fromstring(xml).iter("node"):
            b = [int(v) for v in re.findall(r"\d+", n.get("bounds", ""))]
            t, d = n.get("text") or "", n.get("content-desc") or ""
            if (t or d) and len(b) == 4:
                out.append(dict(text=t, desc=d, id=n.get("resource-id", ""), pkg=n.get("package", ""),
                                click=n.get("clickable") == "true", x=(b[0] + b[2]) // 2, y=(b[1] + b[3]) // 2))
        return out

    def screen_text(self, nodes=None):
        return " | ".join(f"{n['text'] or n['desc']}" for n in (nodes or self.nodes()))

    def check(self, nodes=None):
        """Raise if the screen is a sign-up flow or needs a human."""
        s = self.screen_text(nodes)
        if SIGNUP.search(s):
            raise StopFlow(f"SIGN-UP screen (would create an account) - stopped: {s[:300]}")
        if HUMAN.search(s):
            raise StopFlow(f"needs a human (escalate to Sam): {s[:300]}")
        return s

    def find(self, pattern, nodes=None):
        rx = re.compile(pattern, re.I)
        return next((n for n in (nodes or self.nodes()) if rx.search(n["text"]) or rx.search(n["desc"])), None)

    def tap(self, pattern, wait=3.0, nodes=None):
        n = self.find(pattern, nodes)
        if not n:
            return None
        self.sh(f"input tap {n['x']} {n['y']}")
        time.sleep(wait)
        return n

    def wait_for(self, pattern, timeout=40, step=4):
        end = time.time() + timeout
        while time.time() < end:
            ns = self.nodes()
            self.check(ns)
            n = self.find(pattern, ns)
            if n:
                return n, ns
            time.sleep(step)
        return None, self.nodes()

    def launch(self, pkg, wait=8):
        self.sh(f"monkey -p {pkg} -c android.intent.category.LAUNCHER 1 >/dev/null 2>&1")
        time.sleep(wait)

    def shot(self, out):
        t = g.call("/open/v1/phone/screenShot", {"id": self.env}, self.tok)["taskId"]
        for _ in range(20):
            time.sleep(2)
            r = g.call("/open/v1/phone/screenShot/result", {"taskId": t}, self.tok)
            if r.get("status") == 2:
                Path(out).write_bytes(urllib.request.urlopen(r["downloadLink"], timeout=60).read())
                return out
            if r.get("status") in (0, 3):
                break
        raise RuntimeError("screenshot failed")

    def google_accounts(self):
        out = self.sh("dumpsys account | grep -E 'Account \\{'")
        return sorted({n.strip() for n, _ in re.findall(r"name=([^,]+), type=(com\.google)\}", out)})


class StopFlow(Exception):
    pass


def main(a):
    if len(a) < 3:
        print(__doc__); return 2
    p = Phone(a[1])
    if a[2] == "dump":
        for n in p.nodes():
            print(f"{n['x']:4d},{n['y']:4d} {'*' if n['click'] else ' '} {n['text'] or n['desc']!r:60.60} {n['id']}")
    elif a[2] == "shot":
        print(p.shot(a[3]))
    elif a[2] == "tap":
        print(p.tap(a[3]))
    elif a[2] == "launch":
        p.launch(a[3])
    elif a[2] == "accounts":
        print([x.split("@")[-1] for x in p.google_accounts()])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
