
import asyncio
import os

from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

from agents.query_agent import create_query_agent


async def main():
    # Load the OpenAI API key from .env
    load_dotenv()

    # Connect AutoGen to the OpenAI model
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    # Create our first agent
    query_agent = create_query_agent(model_client)

    # Sample customer complaint
    complaint = (
        "My order is 10 days late and nobody is responding. "
        "I am very disappointed!"
    )

    # Ask the agent to analyze the complaint
    result = await query_agent.run(task=complaint)

    print("\nCUSTOMER QUERY AGENT OUTPUT\n")
    print(result.messages[-1].content)

    # Close the model connection
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
