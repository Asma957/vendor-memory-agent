"""Memory layer.

This module has two parts:
1. Hindsight (long-term memory): retain / recall / list_memories
2. Supersession Ledger: ACTIVE vs OUTDATED status of every vendor term.
   When a new value arrives for the same term, the old value is automatically
   marked "superseded" (this is the Intelligent Forgetting).
"""
import json
import re
from datetime import date, datetime

from hindsight_client import Hindsight

import config

MISSION = (
    "I am a procurement negotiation memory for a company's purchasing team. "
    "I remember how each vendor negotiates (when they give discounts, when they say no first, "
    "what they are flexible or firm on) and the exact contract terms agreed. "
    "When a newer contract or policy replaces an older term, the older term becomes outdated "
    "and must never be presented as current."
)

LIVE_FILE = config.DATA_DIR / "live_events.json"
SEED_FILE = config.DATA_DIR / "seed_events.json"
FLAG_FILE = config.DATA_DIR / f"seeded_{config.BANK_ID}.flag"


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


# ---------------------------------------------------------------- Hindsight
def get_client():
    return Hindsight(
        base_url=config.HINDSIGHT_BASE_URL,
        api_key=config.HINDSIGHT_API_KEY,
        timeout=120.0,
    )


def ensure_bank(client):
    """Create the bank. If it already exists the error is ignored (not fatal)."""
    try:
        client.create_bank(
            bank_id=config.BANK_ID,
            name="Vendor Memory Agent",
            mission=MISSION,
            disposition={"skepticism": 3, "literalism": 3, "empathy": 3},
            enable_observations=True,
        )
        return "Memory bank ready"
    except Exception as e:  # already exists, or an option is unsupported
        return f"Bank note: {str(e)[:150]}"


def hindsight_has_data(client):
    try:
        res = client.list_memories(bank_id=config.BANK_ID, limit=1)
        return (res.total or 0) > 0
    except Exception:
        return False


def is_seeded(client=None):
    if FLAG_FILE.exists():
        return True
    return bool(client) and hindsight_has_data(client)


def retain_event(client, ev):
    kind_label = "Contract update" if ev["kind"] == "contract_update" else "Negotiation"
    client.retain(
        bank_id=config.BANK_ID,
        content=ev["text"],
        context=f"{ev['vendor']} - {kind_label}",
        timestamp=datetime.fromisoformat(ev["date"]),
        document_id=f"{config.BANK_ID}-{ev['id']}",
        metadata={"vendor": ev["vendor"], "kind": ev["kind"], "event_date": ev["date"]},
        tags=[slug(ev["vendor"])],
        retain_async=False,
    )


def seed_all(client, progress=None):
    """Retain all synthetic history in Hindsight."""
    ensure_bank(client)
    events = load_seed()["events"]
    for i, ev in enumerate(events, 1):
        retain_event(client, ev)
        if progress:
            progress(i, len(events), ev["vendor"])
    FLAG_FILE.write_text(datetime.now().isoformat())
    return len(events)


def recall_memories(client, vendor, question, budget="mid"):
    """Recall relevant memories: first with the vendor tag, then without it if nothing is found."""
    query = f"{vendor}: {question}"
    items = []
    try:
        res = client.recall(bank_id=config.BANK_ID, query=query, budget=budget,
                            max_tokens=3000, tags=[slug(vendor)])
        items = res.results or []
    except Exception:
        items = []
    if not items:
        res = client.recall(bank_id=config.BANK_ID, query=query, budget=budget, max_tokens=3000)
        items = res.results or []
    return [{"text": r.text, "type": r.type} for r in items]


def hindsight_observations(client, vendor):
    """Hindsight's own consolidated observations (for the Hindsight view tab)."""
    try:
        res = client.list_memories(bank_id=config.BANK_ID, type="observation",
                                   search_query=vendor, limit=30)
        items = res.items or []
    except Exception:
        res = client.list_memories(bank_id=config.BANK_ID, search_query=vendor, limit=60)
        items = [i for i in (res.items or []) if i.fact_type == "observation"]
    return [{"text": i.text, "proof_count": i.proof_count, "state": i.state,
             "invalidation_reason": i.invalidation_reason} for i in items]


# ------------------------------------------------------------------- events
def load_seed():
    return json.loads(SEED_FILE.read_text(encoding="utf-8"))


def load_live():
    if LIVE_FILE.exists():
        try:
            return json.loads(LIVE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


def load_events():
    events = load_seed()["events"] + load_live()
    return sorted(events, key=lambda e: (e["date"], e["id"]))


def vendor_names():
    return [v["name"] for v in load_seed()["vendors"]]


def find_vendor(text):
    t = text.lower()
    for v in vendor_names():
        if v.lower() in t or v.split()[0].lower() in t:
            return v
    return None


# ------------------------------------------------------------------- ledger
def build_ledger(events=None):
    """{vendor: {"terms": [...], "patterns": [...]}}
    A new term on the same key marks the older one as superseded."""
    events = events or load_events()
    ledger = {v: {"terms": [], "patterns": []} for v in vendor_names()}
    current = {}
    for ev in events:
        vendor = ev["vendor"]
        ledger.setdefault(vendor, {"terms": [], "patterns": []})
        for t in ev.get("terms", []):
            old = current.get((vendor, t["key"]))
            if old and old["status"] == "active":
                old["status"] = "superseded"
                old["replaced_by"] = {"value": t["value"], "date": ev["date"]}
            rec = {"key": t["key"], "label": t["label"], "value": t["value"],
                   "date": ev["date"], "event_id": ev["id"],
                   "status": "active", "replaced_by": None}
            ledger[vendor]["terms"].append(rec)
            current[(vendor, t["key"])] = rec
        if ev.get("pattern"):
            ledger[vendor]["patterns"].append({"date": ev["date"], "text": ev["pattern"]})
    return ledger


def ledger_prompt(vendor_ledger):
    active = [t for t in vendor_ledger["terms"] if t["status"] == "active"]
    old = [t for t in vendor_ledger["terms"] if t["status"] == "superseded"]
    lines = ["ACTIVE TERMS (valid today):"]
    lines += [f"- {t['label']}: {t['value']} (since {t['date']})" for t in active] or ["- none"]
    lines += ["", "OUTDATED TERMS (superseded, never present these as current):"]
    lines += [f"- {t['label']}: {t['value']} (from {t['date']}) -> replaced on "
              f"{t['replaced_by']['date']} by: {t['replaced_by']['value']}" for t in old] or ["- none"]
    lines += ["", "VENDOR BEHAVIOUR PATTERNS (from past negotiations):"]
    lines += [f"- {p['text']} (noted {p['date']})" for p in vendor_ledger["patterns"]] or ["- none"]
    return "\n".join(lines)


# --------------------------------------------------------- live contract update
def add_live_update(client, vendor, key, label, value, description):
    """Add a contract update: retain in Hindsight and update the ledger."""
    ledger = build_ledger()
    old = next((t for t in ledger[vendor]["terms"] if t["key"] == key and t["status"] == "active"), None)
    today = date.today().isoformat()
    prev = f" (previously: {old['value']})" if old else ""
    text = (f"CONTRACT UPDATE effective {today}: {vendor} {description.strip().rstrip('.')}. "
            f"New term: {label} is now {value}. This supersedes the earlier {label} term{prev}. "
            f"The earlier {label} term is outdated and no longer valid.")
    ev = {"id": f"live-{datetime.now():%Y%m%d%H%M%S}", "date": today, "vendor": vendor,
          "kind": "contract_update", "text": text,
          "terms": [{"key": key, "label": label, "value": value}], "pattern": None}
    retain_event(client, ev)  # Hindsight first; if it fails the local file is not changed
    live = load_live()
    live.append(ev)
    LIVE_FILE.write_text(json.dumps(live, indent=2), encoding="utf-8")
    return ev
