
# Saves customer complaints to a CSV file.

import csv
from datetime import datetime
from pathlib import Path
from threading import Lock

LOG_FILE = Path(__file__).resolve().parent / "logs" / "tickets.csv"
LOG_LOCK = Lock()

COLUMNS = [
    "ticket_id", "timestamp", "customer_name", "order_id",
    "complaint", "category", "urgency", "sentiment",
    "kb_sources", "response", "confidence",
    "status", "escalation_reason"
]


def log_ticket(
    customer_name: str,
    order_id: str,
    complaint: str,
    category: str,
    urgency: str,
    sentiment: str,
    kb_sources: str,
    response: str,
    confidence: str,
    status: str,
    escalation_reason: str
) -> str:
    """Save one customer complaint and its resolution."""

    # Enforce escalation rules in Python, not only in the LLM.
    reasons = []

    if urgency.strip().lower() == "high":
        reasons.append("High urgency")

    if sentiment.strip().lower() == "angry":
        reasons.append("Angry customer")

    if confidence.strip().lower() == "low":
        reasons.append("Low confidence")

    if not kb_sources.strip() or "NO_MATCH" in kb_sources.upper():
        reasons.append("No matching knowledge document")

    complaint_lower = complaint.lower()

    if any(word in complaint_lower for word in [
        "lawyer", "legal action", "sue", "fraud",
        "scam", "charged twice", "charged three times",
        "double charged", "payment dispute",
        "unauthorized charge"
    ]):
        reasons.append("Legal, fraud or payment dispute")

    if status.strip().lower() == "escalated" and escalation_reason.strip():
        reasons.append(escalation_reason.strip())

    final_status = "Escalated" if reasons else "Resolved"
    final_reason = "; ".join(dict.fromkeys(reasons))

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with LOG_LOCK:
        # Count existing tickets to create a ticket ID
        existing_count = 0

        if LOG_FILE.exists():
            with LOG_FILE.open("r", encoding="utf-8-sig", newline="") as f:
                existing_count = sum(1 for _ in csv.DictReader(f))

        ticket_id = f"TKT-{existing_count + 1:04d}"

        new_file = not LOG_FILE.exists() or LOG_FILE.stat().st_size == 0

        with LOG_FILE.open("a", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=COLUMNS)

            if new_file:
                writer.writeheader()

            writer.writerow({
                "ticket_id": ticket_id,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "customer_name": customer_name,
                "order_id": order_id,
                "complaint": complaint,
                "category": category,
                "urgency": urgency,
                "sentiment": sentiment,
                "kb_sources": kb_sources,
                "response": response,
                "confidence": confidence,
                "status": final_status,
                "escalation_reason": final_reason
            })

    return f"Ticket {ticket_id} saved successfully. Status: {final_status}"
