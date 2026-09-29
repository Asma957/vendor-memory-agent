Why Your Procurement AI Needs to Forget: Building a Vendor Memory Agent with Hindsight
Built by Team Ignite Minds (J. Asma, S. Shabana, R. Ragini, R. Khedha, A. Geetika, M. Thriveni)

Links: Live Demo | GitHub Repository

The Problem: Remembering Is Not Enough
A procurement rep is meeting a key logistics vendor tomorrow. Their AI assistant remembers the 5% volume discount, the fuel surcharge waiver, and Net 45 payment terms from last January. What it does not know is that the vendor issued a revised contract in August: 3% discount, a 6% fuel surcharge, and Net 30.

The rep walks in quoting terms that no longer exist. The assistant did not lack memory. It lacked the ability to tell which memories are still valid.

Most agent memory demos focus purely on recall. In real-world business decisions, the harder question is: what is still true today?

What We Built
Vendor Memory Agent is a negotiation coach for procurement teams, built on Hindsight, the agent memory system from Vectorize. Learn more in the Hindsight documentation.

It focuses on two core capabilities:

Negotiation Memory: Tracks how each vendor behaves—who pushes back first, who softens after a longer commitment, who remains firm on SLAs, and who offers deeper discounts at quarter-end.

Intelligent Forgetting (Supersession): When a new contract or policy arrives, older terms are marked superseded. The agent never presents outdated terms as current and explicitly tells the representative what was replaced.

Welcome view of the AI-powered Vendor Memory Agent interface.[cite: 1]

Baseline vs. Smart Agent
The application features a side-by-side Baseline vs. Smart comparison answering the same query from the same Hindsight memory bank:

Baseline Agent: Treats every recalled memory as active/current.

Smart Agent: Understands temporal context and supersession, correctly filtering out stale data.

Selecting comparison modes in Brief Studio to evaluate baseline versus smart memory recall.[cite: 3]

How Hindsight Is Used
Hindsight serves as the core memory layer for the entire application:

Retain: Stores negotiations and contract updates with timestamps, vendor tags, and event metadata.

Recall: Retrieves filtered vendor memories before every briefing.

Observations: Background consolidation of related historical facts.

Bank Mission: Configured with specific procurement rules where newer contractual terms override older ones.

Dashboard tracking vendor memories, active valid terms, and contract updates.[cite: 4]

Making Forgetting Visible & Reliable
To ensure real-time responsiveness without depending entirely on background asynchronous consolidation, we introduced a Supersession Ledger on top of Hindsight:

When a new contract term is added, the legacy term is immediately flagged as superseded.

The Memory Panel color-codes terms: Active terms in teal and Outdated/Struck-through terms in amber (showing what replaced them).

Users can add a contract update live and instantly observe the old term transitioning to outdated status.

Negotiation Brief showing side-by-side verification of active terms versus outdated terms.[cite: 2]

Honest Notes
Memory and forgetting mechanisms are evolving concepts. Our contribution focuses on applying this to business decision support, making supersession visually verifiable, and demonstrating the operational risk of naive memory recall through side-by-side execution.

What’s Next
Source Integration: Connect live contract PDFs, ERP systems, and email threads as automated memory sources.

Approval Workflows: Implement manager validation before superseding high-value contract terms.

Outcome Tracking: Measure the success rate of tactical recommendations over time.

Tech Stack
Memory Layer: Hindsight by Vectorize

LLM Engine: Groq

Frontend / UI: Streamlit

Language: Python
