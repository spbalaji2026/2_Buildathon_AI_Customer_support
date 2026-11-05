
import asyncio

from team import process_complaint


async def main():

    complaint = (
        "My order is 10 days late and nobody is responding. "
        "I am very disappointed!"
    )

    messages = await process_complaint(
        complaint=complaint,
        customer_name="Test Customer",
        order_id="ORD-1001"
    )

    print("\n===== MULTI-AGENT WORKFLOW =====\n")

    for message in messages:
        print("\nAGENT:", message["source"])
        print(message["content"])
        print("-" * 50)


if __name__ == "__main__":
    asyncio.run(main())
