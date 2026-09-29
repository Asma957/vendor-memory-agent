"""Two agents: Baseline (treats every memory as current) and Smart (understands supersession)."""
import memory
from llm import chat

FORMAT = (
    "Write a concise negotiation brief, at most 250 words, in plain Markdown. Use exactly these ### headings: "
    "Current terms, Vendor behaviour, Strategy for tomorrow (3-4 bullets), Watch-outs. "
    "Use exact numbers. Do not use tables, backticks or code formatting. "
    "Always reply in clear, professional English."
)

BASELINE_SYSTEM = (
    "You are a procurement assistant. You receive memory snippets recalled from long-term memory "
    "about a vendor. Treat every recalled memory as a current, valid fact and use the numbers in them. "
    + FORMAT
)

SMART_SYSTEM = (
    "You are the Vendor Memory Agent, a negotiation coach for procurement reps. "
    "You receive (a) memories recalled from Hindsight long-term memory and (b) a Supersession Ledger that "
    "states which terms are ACTIVE and which are OUTDATED. Rules: "
    "use ONLY ACTIVE terms as current terms; never quote an OUTDATED term as current; "
    "if a recalled memory contradicts the ledger, the ledger wins. "
    "Add a final ### heading 'Outdated - do not use' with one plain-text bullet per superseded term, "
    "written as: old term, then the word 'replaced by', then the new term, so the rep does not walk in with old pricing. "
    "Adapt the strategy using the vendor's behaviour patterns. " + FORMAT
)


def _format_memories(mems):
    return "\n".join(f"- {m['text']}" for m in mems) or "- (no memories found)"


def baseline_brief(client, vendor, question):
    mems = memory.recall_memories(client, vendor, question)
    user = f"Rep request: {question}\nVendor: {vendor}\n\nRecalled memories:\n{_format_memories(mems)}"
    return {"answer": chat(BASELINE_SYSTEM, user).replace("`", ""), "memories": mems, "ledger_text": None}


def smart_brief(client, vendor, question):
    mems = memory.recall_memories(client, vendor, question)
    ledger_text = memory.ledger_prompt(memory.build_ledger()[vendor])
    user = (f"Rep request: {question}\nVendor: {vendor}\n\n"
            f"Recalled memories (Hindsight):\n{_format_memories(mems)}\n\n"
            f"Supersession Ledger:\n{ledger_text}")
    return {"answer": chat(SMART_SYSTEM, user).replace("`", ""), "memories": mems, "ledger_text": ledger_text}
