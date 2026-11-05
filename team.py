
# Connects the four AutoGen agents into one team.

import os

from dotenv import load_dotenv

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import (
    TextMentionTermination,
    MaxMessageTermination
)

from agents.query_agent import create_query_agent
from agents.knowledge_agent import create_knowledge_agent
from agents.resolution_agent import create_resolution_agent
from agents.log_agent import create_log_agent
from ticket_logger import log_ticket


async def process_complaint(complaint, customer_name="", order_id=""):
    """Process one complaint through four AI agents."""

    load_dotenv()

    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    try:
        # Create four specialized agents
        query_agent = create_query_agent(model_client)
        knowledge_agent = create_knowledge_agent(model_client)
        resolution_agent = create_resolution_agent(model_client)
        log_agent = create_log_agent(model_client, log_ticket)

        # Stop after Log Agent says LOGGED.
        termination = (
            TextMentionTermination("LOGGED", sources=["Log_Agent"])
            | MaxMessageTermination(16)
        )

        # Agents speak in the order provided.
        team = RoundRobinGroupChat(
            participants=[
                query_agent,
                knowledge_agent,
                resolution_agent,
                log_agent
            ],
            termination_condition=termination
        )

        task = f"""
Process this SmartCart customer complaint.

Customer name: {customer_name or 'Not provided'}
Order ID: {order_id or 'Not provided'}
Original complaint: {complaint}

Workflow:
1. Customer Query Agent classifies the complaint.
2. Knowledge Base Agent searches company documents.
3. Resolution Agent writes a grounded customer reply.
4. Log Agent saves the ticket using log_ticket.

Each agent must perform only its assigned responsibility.
"""

        result = await team.run(task=task)

        # Return messages for inspection and later Streamlit display
        messages = []

        for message in result.messages:
            if hasattr(message, "content"):
                messages.append({
                    "source": message.source,
                    "content": str(message.content)
                })

        return messages

    finally:
        await model_client.close()
