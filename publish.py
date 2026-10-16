"""Publish every queued item that is due (runs on GitHub Actions every 30 min).
Queue: posts/queue.json -> [{id, type: image|carousel|reel|story, files:[...], caption, at: "YYYY-MM-DD HH:MM" (IST), posted}]
Items without 'at' are posted one per run (old behaviour). Env: IG_TOKEN, IG_USER_ID (default 'me'), FORCE_NOW=1 posts the next item now."""
import json, os, sys, time, datetime, requests
API = "https://graph.instagram.com/v23.0"
TOKEN = os.environ["IG_TOKEN"]; USER = os.environ.get("IG_USER_ID") or "me"
REPO = os.environ["GITHUB_REPOSITORY"]; BRANCH = os.environ.get("GITHUB_REF_NAME", "main")
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/"
QUEUE = "posts/queue.json"
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))

def call(method, path, **params):
    params["access_token"] = TOKEN
    r = requests.request(method, f"{API}/{path}", params=params, timeout=120)
    if r.status_code >= 400: raise RuntimeError(f"API error {r.status_code}: {r.text}")
    return r.json()

def wait_ready(cid):
    for _ in range(60):
        s = call("GET", cid, fields="status_code,status").get("status_code")
        if s == "FINISHED": return
        if s == "ERROR": raise RuntimeError(f"Media {cid} failed processing: {call('GET', cid, fields='status')}")
        time.sleep(10)
    raise RuntimeError("Timed out waiting for media")

def url(f): return RAW + (f if "/" in f else "posts/" + f)
def is_vid(u): return u.lower().endswith((".mp4", ".mov"))

def publish(p):
    urls = [url(f) for f in p["files"]]; t, cap = p["type"], p.get("caption", "")
    if t == "image": cid = call("POST", f"{USER}/media", image_url=urls[0], caption=cap)["id"]
    elif t == "story":
        k = "video_url" if is_vid(urls[0]) else "image_url"
        cid = call("POST", f"{USER}/media", media_type="STORIES", **{k: urls[0]})["id"]
    elif t == "reel": cid = call("POST", f"{USER}/media", media_type="REELS", video_url=urls[0], caption=cap, share_to_feed="true")["id"]
    elif t == "carousel":
        kids = []
        for u in urls[:10]:
            kw = {"media_type": "VIDEO", "video_url": u} if is_vid(u) else {"image_url": u}
            kids.append(call("POST", f"{USER}/media", is_carousel_item="true", **kw)["id"])
        for k in kids: wait_ready(k)
        cid = call("POST", f"{USER}/media", media_type="CAROUSEL", children=",".join(kids), caption=cap)["id"]
    else: raise RuntimeError(f"Unknown type {t}")
    wait_ready(cid)
    return call("POST", f"{USER}/media_publish", creation_id=cid)["id"]

def main():
    q = json.load(open(QUEUE)); now = datetime.datetime.now(IST).strftime("%Y-%m-%d %H:%M")
    todo = [p for p in q if not p.get("posted")]
    due = [p for p in todo if p.get("at") and p["at"] <= now]
    if not due and os.environ.get("FORCE_NOW") == "1" and todo: due = [todo[0]]
    if not due and not any(p.get("at") for p in todo) and todo and os.environ.get("GITHUB_EVENT_NAME") != "schedule": due = [todo[0]]
    errors = 0
    for p in due:
        try:
            mid = publish(p); p.update(posted=True, media_id=mid, posted_at=now); print(f"Published {p['id']} -> {mid}")
        except Exception as e:
            errors += 1; p["last_error"] = str(e)[:300]; print(f"FAILED {p['id']}: {e}")
        json.dump(q, open(QUEUE, "w"), indent=2, ensure_ascii=False)
    print(f"Due {len(due)}, failed {errors}, remaining {len([p for p in q if not p.get('posted')])}")
    if errors: sys.exit(1)

if __name__ == "__main__": main()
