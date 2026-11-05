
# Test the knowledge base retrieval function

from agents.knowledge_agent import search_kb

query = "My order is 10 days late and delivery is delayed"

result = search_kb(query)

print("\nKNOWLEDGE BASE SEARCH RESULTS\n")
print(result)
