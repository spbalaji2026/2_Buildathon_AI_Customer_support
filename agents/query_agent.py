
# Agent 1: Customer Query Agent
# Analyzes the customer's complaint.

from autogen_agentchat.agents import AssistantAgent


def create_query_agent(model_client):
    """Create the Customer Query Agent."""

    return AssistantAgent(
        name="Customer_Query_Agent",
        model_client=model_client,
        description="Analyzes customer complaints and identifies the issue.",
        system_message="""
You are a customer complaint classification specialist
working for SmartCart online shopping.

Analyze the customer's complaint.

Return exactly these four fields:

Category: Shipping / Refund / Account / Product / Billing / Other
Urgency: Low / Medium / High
Sentiment: Happy / Neutral / Frustrated / Angry
Summary: One sentence describing the complaint.

Rules:
- Identify the main customer issue.
- Use High urgency for legal threats, suspected fraud,
  serious payment disputes, or critical complaints.
- Use Angry when the customer expresses strong anger.
- Do not invent information.
- Keep the output concise.
"""
    )
