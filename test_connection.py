"""Quick check: are Hindsight and Groq both working?  python test_connection.py
(Uses a separate 'connection-test' bank so nothing enters the demo memory.)"""
import config
import memory
from llm import chat

TEST_BANK = "connection-test"
client = memory.get_client()
try:
    client.create_bank(bank_id=TEST_BANK, name="Connection Test")
except Exception as e:
    print("create_bank note:", str(e)[:150])
client.retain(bank_id=TEST_BANK, content="Acme Supplies gave us a 5% discount after a 12-month commitment.",
              context="connection test", retain_async=False)
res = client.recall(bank_id=TEST_BANK, query="Which vendor gave a discount?", budget="low")
print("Hindsight OK. Recall results:", len(res.results))
for r in res.results:
    print(" -", r.text)
print("Groq reply:", chat("You are terse.", "Say 'Groq OK' and nothing else."))
