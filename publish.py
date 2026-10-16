"""Publish the next queued post to Instagram (runs on GitHub Actions).
Env: IG_TOKEN (secret), IG_USER_ID, GITHUB_REPOSITORY, GITHUB_REF_NAME
Queue: posts/queue.json -> list of {id, type: image|carousel|reel|story, files:[...], caption, posted:false}
"""
import json, os, sys, time, requests

API = "https://graph.instagram.com/v23.0"
TOKEN = os.environ["IG_TOKEN"]
USER = os.environ.get("IG_USER_ID", "me")
REPO = os.environ["GITHUB_REPOSITORY"]
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/posts/"
QUEUE = "posts/queue.json"

def call(method, path, **params):
    params["access_token"] = TOKEN
    r = requests.request(method, f"{API}/{path}", params=params, timeout=60)
    if r.status_code >= 400:
        sys.exit(f"API error {r.status_code}: {r.text}")
    return r.json()

def wait_ready(cid):
    for _ in range(40):
        s = call("GET", cid, fields="status_code").get("status_code")
        if s == "FINISHED": return
        if s == "ERROR": sys.exit(f"Media {cid} failed processing")
        time.sleep(15)
    sys.exit("Timed out waiting for media")

def media(url, **extra):
    key = "video_url" if url.lower().endswith((".mp4", ".mov")) else "image_url"
    return call("POST", f"{USER}/media", **{key: url}, **extra)["id"]

def publish(post):
    urls = [RAW + f for f in post["files"]]
    t, cap = post["type"], post.get("caption", "")
    if t == "image":
        cid = media(urls[0], caption=cap)
    elif t == "story":
        cid = media(urls[0], media_type="STORIES")
    elif t == "reel":
        cid = call("POST", f"{USER}/media", media_type="REELS", video_url=urls[0], caption=cap)["id"]
    elif t == "carousel":
        kids = []
        for u in urls:
            extra = {"media_type": "VIDEO"} if u.lower().endswith(".mp4") else {}
            kids.append(media(u, is_carousel_item="true", **extra))
        for k in kids: wait_ready(k)
        cid = call("POST", f"{USER}/media", media_type="CAROUSEL", children=",".join(kids), caption=cap)["id"]
    else:
        sys.exit(f"Unknown type {t}")
    wait_ready(cid)
    return call("POST", f"{USER}/media_publish", creation_id=cid)["id"]

def main():
    q = json.load(open(QUEUE))
    todo = [p for p in q if not p.get("posted")]
    if not todo:
        print("Queue empty - add more posts."); return
    p = todo[0]
    mid = publish(p)
    p["posted"] = True; p["media_id"] = mid; p["posted_at"] = time.strftime("%Y-%m-%d %H:%M")
    json.dump(q, open(QUEUE, "w"), indent=2, ensure_ascii=False)
    print(f"Published {p['id']} -> {mid}. Remaining: {len(todo)-1}")

if __name__ == "__main__":
    main()
