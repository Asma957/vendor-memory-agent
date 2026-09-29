# How we use Hindsight memory

| Hindsight feature | Where we use it |
|---|---|
| `create_bank` (mission, disposition, observations on) | One bank per app. Mission tells Hindsight it is a procurement negotiation memory. |
| `retain` (content, context, timestamp, document_id, metadata, tags) | Every negotiation and every contract update is retained with its real date, vendor tag and `kind` metadata. |
| `recall` (vendor tag filter, budget) | Before every brief, the agent recalls that vendor's memories. Falls back to untagged recall if the tag filter returns nothing. |
| Observations (auto-consolidation) | Hindsight consolidates conflicting facts (old term -> new term) and keeps history. Shown in the Memory Panel's "Hindsight view" tab. |
| `list_memories` | Powers the "Hindsight view" tab (observations, evidence count, state). |

## Intelligent forgetting
Contract updates are retained with explicit supersession language ("supersedes the earlier 5%..."), so Hindsight's own consolidation sees the conflict. On top of that, the app keeps a small **Supersession Ledger**: when a new term arrives for the same term key, the old one is marked *superseded* and the Smart agent is told to use only ACTIVE terms. This makes forgetting deterministic and visible in the UI, and does not depend on consolidation timing.

## Why memory is central
Without Hindsight there is no vendor history to recall: the brief is built from recalled negotiation memories (behaviour patterns, past concessions) plus the ledger. The Baseline vs Smart toggle uses the same Hindsight memory, so the difference you see comes from supersession handling, not from different data.
