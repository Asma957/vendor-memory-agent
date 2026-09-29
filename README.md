# Vendor Memory Agent

A negotiation-memory agent for procurement reps, built on **Hindsight** (Vectorize) for *Hack With Hyderabad 3.0*.

**Pitch:** the agent doesn't just remember, it knows when old deal terms are outdated, so a rep never walks into a negotiation with wrong pricing or the wrong strategy.

## What it does
- **Negotiation Memory:** remembers how each vendor negotiates (says no first, flexible on X, firm on Y, quarter-end pressure).
- **Intelligent Forgetting:** when a new contract or policy arrives, older terms are marked **superseded** and are never presented as current.
- **Baseline vs Smart toggle:** same question, same Hindsight memory. Baseline treats every memory as current, Smart understands supersession.
- **Memory Panel:** active terms in green, outdated terms amber and struck through, with what replaced them.
- **Live update:** add a contract update and watch the old term turn amber and struck through.

## Quick start (Windows)
Double-click `run.bat`. The first time, Notepad opens `.env`: paste your Hindsight and Groq keys, save, close. The script then creates the virtual environment, installs libraries, checks connections, loads demo data and starts the app.

## Manual run
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env      (then add your keys)
python test_connection.py
streamlit run app.py
```
Use **Load demo data** in the sidebar once, or run `python seed.py`.

## Deploy (Streamlit Community Cloud)
1. Push the code to GitHub. Never push `.env`; `.gitignore` already excludes it.
2. On https://share.streamlit.io choose **New app**, select the repo, main file `app.py`.
3. Under **Advanced settings > Secrets**, paste `.streamlit/secrets.toml.example` with real keys.
4. Deploy. If the build fails, choose Python 3.12 in Advanced settings.

## Architecture
```
Rep question -> vendor detect -> Hindsight recall (vendor-tagged) ----+
                                                                      +--> Groq LLM -> negotiation brief
Supersession Ledger (ACTIVE vs OUTDATED terms) -- Smart agent only ---+
```
Files: `app.py` (UI), `memory.py` (Hindsight + ledger), `agents.py` (baseline/smart), `llm.py` (Groq), `seed.py`, `data/seed_events.json` (synthetic data: 3 vendors, 6-7 events each).
Hindsight details: `HINDSIGHT_MEMORY.md`. Demo script: `DEMO_SCRIPT.md`.

## Demo reset
Set a new `VENDOR_BANK_ID` in `.env`, delete `data/live_events.json`, then reload the demo data.

## Honest notes
- Memory and forgetting are known concepts. Our angle: business decision support, visible supersession and a before/after comparison.
- Data is synthetic. No real vendors.
- Hindsight consolidation is asynchronous, so new observations can take a while to appear in the Hindsight view tab.
