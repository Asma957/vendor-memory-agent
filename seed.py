"""Load demo data into Hindsight.  python seed.py   (skips if already loaded; use --force to reload)"""
import sys

import config
import memory

if not (config.HINDSIGHT_API_KEY and config.HINDSIGHT_BASE_URL):
    raise SystemExit("HINDSIGHT_API_KEY / HINDSIGHT_BASE_URL .env")

client = memory.get_client()
if memory.is_seeded(client) and "--force" not in sys.argv:
    print("Demo data is already loaded. Skipping.")
    raise SystemExit(0)

n = memory.seed_all(client, progress=lambda i, t, v: print(f"[{i}/{t}] retained: {v}"))
print(f"Done! {n} memories stored in Hindsight (bank: {config.BANK_ID}).")
