"""Check the long-lived token still works and refresh it (extends 60 days). Prints days left."""
import os, sys, requests
t = os.environ["IG_TOKEN"]
r = requests.get("https://graph.instagram.com/refresh_access_token",
                 params={"grant_type": "ig_refresh_token", "access_token": t}, timeout=30)
print(r.status_code, {k: v for k, v in r.json().items() if k != "access_token"})
if r.status_code >= 400: sys.exit(1)
