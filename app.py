
# SmartCart AI Customer Support Desk
# Streamlit application using four AutoGen agents.

import asyncio
import csv
from pathlib import Path

import pandas as pd
import streamlit as st

from team import process_complaint


LOG_FILE = Path("logs/tickets.csv")

st.set_page_config(
    page_title="SmartCart AI Support Desk",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 SmartCart AI Customer Support Desk")

st.write(
    "An AI-powered customer support system using "
    "AutoGen, OpenAI, Python and Streamlit."
)

st.divider()

st.subheader("Submit a Customer Complaint")

customer_name = st.text_input(
    "Customer Name (Optional)"
)

order_id = st.text_input(
    "Order ID (Optional)"
)

complaint = st.text_area(
    "Enter Customer Complaint",
    height=130,
    placeholder="Example: My order is 10 days late..."
)

submit = st.button(
    "Submit Complaint",
    type="primary"
)

if submit:

    if not complaint.strip():
        st.warning("Please enter a complaint.")

    else:
        with st.spinner("Four AI agents are processing your complaint..."):

            try:
                messages = asyncio.run(
                    process_complaint(
                        complaint=complaint,
                        customer_name=customer_name,
                        order_id=order_id
                    )
                )

                st.success("Agent workflow finished.")

                st.subheader("AI Agent Workflow")

                agent_names = {
                    "Customer_Query_Agent": "1. Customer Query Agent",
                    "Knowledge_Base_Agent": "2. Knowledge Base Agent",
                    "Resolution_Agent": "3. Resolution Agent",
                    "Log_Agent": "4. Log Agent"
                }

                for message in messages:

                    source = message["source"]

                    if source in agent_names:
                        with st.expander(
                            agent_names[source],
                            expanded=True
                        ):
                            st.write(message["content"])

                st.subheader("Customer Support Response")

                resolution_messages = [
                    m for m in messages
                    if m["source"] == "Resolution_Agent"
                    and "Customer_Response:" in m["content"]
                ]

                if resolution_messages:
                    st.info(resolution_messages[-1]["content"])
                else:
                    st.warning("No final customer response was found.")

                # Read the latest saved ticket
                if LOG_FILE.exists():

                    with LOG_FILE.open(
                        "r",
                        encoding="utf-8-sig",
                        newline=""
                    ) as f:
                        rows = list(csv.DictReader(f))

                    if rows:

                        latest = rows[-1]

                        st.subheader("Ticket Status")

                        st.write(
                            "Ticket ID:",
                            latest["ticket_id"]
                        )

                        if latest["status"] == "Escalated":
                            st.error("🔴 ESCALATED — Human Review Required")

                            st.write(
                                "Reason:",
                                latest["escalation_reason"]
                            )
                        else:
                            st.success("🟢 RESOLVED")

            except Exception as error:
                st.error(f"Error: {error}")

st.divider()

st.subheader("Customer Ticket Log")

if LOG_FILE.exists():

    df = pd.read_csv(LOG_FILE, encoding="utf-8-sig")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.download_button(
        label="Download Ticket Log (CSV)",
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name="smartcart_tickets.csv",
        mime="text/csv"
    )

else:
    st.info("No customer tickets recorded yet.")

st.caption("Buildathon Project | AutoGen Multi-Agent Customer Support")
