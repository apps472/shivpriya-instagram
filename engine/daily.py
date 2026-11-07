"""Runs on GitHub Actions every night: renders the next days of the 1-year plan into _media/ (pushed to the 'media' branch)
and adds their posts to posts/queue.json. Env AHEAD = days ahead to build (default 2)."""
import os, sys, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build, cal
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
today = datetime.datetime.now(IST).date(); ahead = int(os.environ.get("AHEAD") or 2)
end = cal.START + datetime.timedelta(days=364)
days = [today + datetime.timedelta(days=k) for k in range(-1, ahead + 1)]
days = [d for d in days if cal.START <= d <= end]
print("Building:", [d.isoformat() for d in days])
q = json.load(open("posts/queue.json")); have = {p["id"] for p in q}; added = 0
for d in days:
    for it in build.build("_media", d):
        if it["id"] not in have: q.append(it); have.add(it["id"]); added += 1
json.dump(q, open("posts/queue.json", "w"), indent=2, ensure_ascii=False)
print(f"Added {added} queue items; window has {len(days)} days")
open(os.environ.get("GITHUB_OUTPUT", "/dev/null"), "a").write(f"built={len(days)}\n")
