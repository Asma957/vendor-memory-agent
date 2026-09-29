# Submission checklist

## Before you push
- [ ] Old Hindsight and Groq keys rotated; new keys only in `.env` and Streamlit Secrets
- [ ] `.env`, `venv/` and `data/live_events.json` are not tracked (`git status` should not list them)
- [ ] `run.bat` tested end to end with real keys
- [ ] Dry run done, best vendor chosen for the demo

## Push to GitHub
Create an empty repo on github.com first (no README), then in the project folder:
```
git init
git add .
git status
git commit -m "Vendor Memory Agent for Hack With Hyderabad 3.0"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```
Check `git status` before committing. If `.env` appears, stop and fix `.gitignore`.

## Deploy
- [ ] share.streamlit.io: New app, repo, branch `main`, file `app.py`
- [ ] Secrets pasted from `.streamlit/secrets.toml.example` with real keys
- [ ] Live link opens and *Generate brief* works from another device

## Fill placeholders
- [ ] `[GITHUB_LINK]`, `[DEPLOYED_LINK]`, `[TEAM NAMES]` in ARTICLE.md, SOCIAL_POST.md, VIDEO_SCRIPT.md, README.md

## Deliverables
- [ ] Clean GitHub repo
- [ ] Demo video recorded (VIDEO_SCRIPT.md)
- [ ] Live demo link
- [ ] Hindsight memory explanation (HINDSIGHT_MEMORY.md)
- [ ] Article published (ARTICLE.md)
- [ ] Social post published (SOCIAL_POST.md), tagging the hackathon and Hindsight/Vectorize
- [ ] 60-second demo rehearsed (DEMO_SCRIPT.md)

## Judging criteria to keep in mind
Innovation 30%, Use of Hindsight Memory 25%, Technical 20%, UX 15%, Real-world Impact 10%.
