# Why Your Procurement AI Needs to Forget: Building a Vendor Memory Agent with Hindsight

*Built for Hack With Hyderabad 3.0 by [TEAM NAMES]. Code: [GITHUB_LINK]. Live demo: [DEPLOYED_LINK].*

## The problem: remembering is not enough

A procurement rep is meeting a key logistics vendor tomorrow. Their AI assistant remembers the 5% volume discount, the fuel surcharge waiver and Net 45 payment terms from last January. What it does not know is that the vendor issued a revised contract in August: 3% discount, a 6% fuel surcharge and Net 30.

The rep walks in quoting terms that no longer exist. The assistant did not lack memory. It lacked the ability to tell which memories are still true.

Most agent memory demos focus on recall. In business decisions, the harder question is *what is still valid*.

## What we built

**Vendor Memory Agent** is a negotiation coach for procurement teams, built on Hindsight, the agent memory system from Vectorize. It does two things:

1. **Negotiation memory.** It remembers how each vendor behaves: who says no first, who softens after a longer commitment, who is firm on SLAs, who gives deeper discounts at quarter end.
2. **Intelligent forgetting.** When a new contract or policy arrives, the older term is marked *superseded*. The agent never presents it as current, and it tells the rep exactly what was replaced.

The app shows this visibly. A **Baseline vs Smart** view answers the same question from the same Hindsight memory. The Baseline treats every recalled memory as current. The Smart agent understands supersession. Any difference in the answers comes from how superseded terms are handled, not from different data.

## How Hindsight is used

Hindsight is the memory layer of the whole app, not a decoration.

- **Retain:** every negotiation and every contract update is stored with its real date, a vendor tag and metadata describing the event type.
- **Recall:** before every brief, the agent recalls that vendor's memories, filtered by vendor tag.
- **Observations:** Hindsight consolidates related facts in the background. Our Hindsight view tab shows these observations.
- **Bank mission:** the memory bank is configured with a mission describing a procurement negotiation memory where newer terms replace older ones.

Contract updates are written with explicit supersession language, so Hindsight's own consolidation can see the conflict.

## Making forgetting visible and reliable

Background consolidation is asynchronous, so we did not want the demo to depend on its timing. On top of Hindsight we added a small **Supersession Ledger**. When a new value arrives for the same term, the old value is marked *superseded* and the Smart agent is told to use only active terms. The Memory Panel shows active terms in teal and outdated terms in amber and struck through, with what replaced them.

A rep can add a contract update live and watch the old term turn outdated immediately, while the new fact is retained in Hindsight.

## Honest notes

Memory and forgetting are not new ideas. Our contribution is the angle: business decision support, supersession that users can see, and a side-by-side comparison that shows the cost of not handling it. The data in the demo is synthetic, and a baseline model can sometimes answer correctly by luck, which is why the comparison shows the recalled memories and the ledger behind each answer.

## What we would do next

- Connect real contract documents and email threads as memory sources.
- Add approval workflows so a manager confirms a supersession before it becomes active.
- Track outcomes, so the agent learns which tactics actually won concessions.

## Stack

Hindsight (Vectorize) for memory, Groq for the language model, Streamlit for the UI, Python throughout.

*Try it: [DEPLOYED_LINK]. Source: [GITHUB_LINK].*
