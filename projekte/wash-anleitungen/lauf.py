#!/usr/bin/env python3
"""Erzeugt Anleitungs-Slides ueber kie.ai. Upload der Referenzen + Batch-Lauf."""
import base64, json, os, re, sys, time, threading, urllib.request, urllib.error
from datetime import date, datetime
from pathlib import Path

KEY = os.environ["KIE_API_KEY"]
BASIS = "https://api.kie.ai/api/v1"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
UP = "https://kieai.redpandaai.co/api/file-base64-upload"
EUR = 0.0043
ZIEL = Path.home() / "Medien" / f"{date.today().isoformat()}-wash-anleitungen"
ZIEL.mkdir(parents=True, exist_ok=True)
REFDB = ZIEL / "referenzen.json"
_lock = threading.Lock()

def req(url, data=None, params=None, tries=5):
    if params:
        url += "?" + urllib.parse.urlencode(params)
    body = json.dumps(data).encode() if data is not None else None
    h = {"Authorization": f"Bearer {KEY}", "Accept": "application/json", "User-Agent": UA}
    if body: h["Content-Type"] = "application/json"
    for i in range(1, tries + 1):
        try:
            r = urllib.request.Request(url, data=body, headers=h,
                                       method="POST" if body else "GET")
            with urllib.request.urlopen(r, timeout=180) as a:
                return json.loads(a.read().decode())
        except urllib.error.HTTPError as e:
            txt = e.read()[:300].decode(errors="replace")
            if e.code in (429, 500, 502, 503) and i < tries:
                time.sleep(2 ** i); continue
            raise SystemExit(f"HTTP {e.code} {url}: {txt}")
        except urllib.error.URLError as e:
            if i < tries: time.sleep(2 ** i); continue
            raise SystemExit(f"Netz: {e}")

import urllib.parse

def upload(pfad, name):
    db = json.loads(REFDB.read_text()) if REFDB.exists() else {}
    if name in db: return db[name]
    b64 = base64.b64encode(Path(pfad).read_bytes()).decode()
    r = req(UP, {"base64Data": "data:image/jpeg;base64," + b64,
                 "uploadPath": "images/wash", "fileName": name})
    url = r["data"]["downloadUrl"]
    db[name] = url; REFDB.write_text(json.dumps(db, indent=2))
    return url

def api(pfad, data=None, params=None):
    r = req(BASIS + pfad, data, params)
    if r.get("code") != 200:
        raise SystemExit(f"kie.ai {r.get('code')}: {r.get('msg')}")
    return r.get("data") or {}

def einer(job):
    eingabe = {"prompt": job["prompt"], "image_size": job.get("size", "1k")}
    if job.get("ratio"): eingabe["aspect_ratio"] = job["ratio"]
    if job.get("refs"): eingabe["image_urls"] = job["refs"]
    tid = api("/jobs/createTask", {"model": job["modell"], "input": eingabe}).get("taskId")
    if not tid: raise SystemExit("keine taskId")
    while True:
        d = api("/jobs/recordInfo", params={"taskId": tid})
        st = d.get("state")
        if st == "success":
            erg = json.loads(d.get("resultJson") or "{}")
            urls = erg.get("resultUrls") or []
            cr = d.get("creditsConsumed") or 0
            ziel = ZIEL / job["datei"]
            for i in range(5):
                try:
                    rq = urllib.request.Request(urls[0], headers={"User-Agent": UA})
                    with urllib.request.urlopen(rq, timeout=300) as a, open(ziel, "wb") as f:
                        while True:
                            b = a.read(65536)
                            if not b: break
                            f.write(b)
                    break
                except Exception:
                    if i == 4: raise
                    time.sleep(2 ** i)
            with _lock:
                mp = ZIEL / "meta.json"
                alt = json.loads(mp.read_text()) if mp.exists() else []
                alt.append({"zeit": datetime.now().replace(microsecond=0).isoformat(),
                            "datei": job["datei"], "typ": "bild", "modell": job["modell"],
                            "prompt": job["prompt"], "credits": cr,
                            "eur": round(cr * EUR, 4)})
                mp.write_text(json.dumps(alt, ensure_ascii=False, indent=2))
            return job["datei"], cr, None
        if st == "fail":
            return job["datei"], 0, d.get("failMsg") or d.get("failCode") or "fail"
        time.sleep(8)

def masse(jobs, parallel=4):
    aus = []
    def arbeit(j):
        try: aus.append(einer(j))
        except SystemExit as e: aus.append((j["datei"], 0, str(e)))
        except Exception as e: aus.append((j["datei"], 0, f"{type(e).__name__}: {e}"))
    threads = []
    for j in jobs:
        t = threading.Thread(target=arbeit, args=(j,)); t.start(); threads.append(t)
        while sum(1 for x in threads if x.is_alive()) >= parallel: time.sleep(1)
    for t in threads: t.join()
    ges = sum(c for _, c, _ in aus)
    for d, c, f in sorted(aus):
        print(f"  {'FEHLER' if f else 'ok    '} {d}  {c} Cr  {f or ''}")
    print(f"Summe: {ges} Credits · {ges*EUR:.3f} €".replace(".", ","))
    return aus

if __name__ == "__main__":
    jobs = json.loads(Path(sys.argv[1]).read_text())
    masse(jobs, parallel=int(sys.argv[2]) if len(sys.argv) > 2 else 4)
