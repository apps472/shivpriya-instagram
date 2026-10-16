# Shivpriya Texchem - Instagram Auto-Post (free)

Runs on GitHub Actions (free). Every day at 10:00 AM IST it publishes the next post in `posts/queue.json` to @shivpriya.texchem.

## One-time setup
1. Create a **public** GitHub repo, e.g. `shivpriya-instagram` (public so Instagram can fetch the images).
2. Upload everything in this folder (including `.github/workflows/`).
3. Repo -> Settings -> Secrets and variables -> Actions:
   - **Secret** `IG_TOKEN` = your Instagram access token (paste it yourself)
   - **Variable** `IG_USER_ID` = 17841445041013343
4. Actions tab -> "Instagram auto-post" -> **Run workflow** for a test post.

## Adding more posts
Edit `POSTS` in `tools/make_posts.py`, run `python3 tools/make_posts.py`, upload the new `posts/` files.
Supported types in queue.json: image, carousel, reel (.mp4), story.

The token refresh workflow runs on the 1st and 15th so the 60-day token never expires.
