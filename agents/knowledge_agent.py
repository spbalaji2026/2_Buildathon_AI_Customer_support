
# Agent 2: Knowledge Base Agent
# Searches company policy documents using keyword matching.

import re
from pathlib import Path

from autogen_agentchat.agents import AssistantAgent


# Locate the company knowledge base folder
KB_FOLDER = Path(__file__).resolve().parent.parent / "knowledge_base"


def search_kb(query: str) -> str:
    """Search company documents and return relevant passages."""

    stop_words = {
        "the", "and", "for", "with", "this", "that",
        "from", "have", "been", "your", "what",
        "when", "where", "will", "would", "could",
        "should", "about", "please", "customer",
        "order", "issue", "problem"
    }

    # Convert complaint into searchable words
    query_words = set(re.findall(r"[a-z]+", query.lower()))

    query_words = {
        word for word in query_words
        if len(word) > 2 and word not in stop_words
    }

    # Expand common complaint terms
    synonyms = {
        "late": {"delayed", "delivery", "shipping"},
        "delay": {"delayed", "delivery", "shipping"},
        "shoes": {"product", "return"},
        "broken": {"damaged", "defective", "replacement"},
        "blender": {"product", "damaged"},
        "password": {"login", "reset"},
        "refund": {"return", "refund"},
        "charged": {"billing", "payment"},
    }

    expanded_words = set(query_words)

    for word in query_words:
        expanded_words.update(synonyms.get(word, set()))

    matches = []

    # Search all company policy documents
    for file_path in KB_FOLDER.glob("*.md"):

        content = file_path.read_text(encoding="utf-8")
        passages = content.split("\n\n")

        for passage in passages:

            passage_words = set(
                re.findall(r"[a-z]+", passage.lower())
            )

            # Calculate keyword similarity
            score = len(
                expanded_words.intersection(passage_words)
            )

            filename = file_path.name.lower()

            # Give priority to the relevant policy
            if {"late", "delay", "delayed", "shipping"}.intersection(query_words):
                if filename == "shipping_policy.md":
                    score += 5

            if {"refund", "return", "money"}.intersection(query_words):
                if filename == "refund_policy.md":
                    score += 5

            if {"password", "login", "account"}.intersection(query_words):
                if filename == "account_and_login.md":
                    score += 5

            if {"broken", "damaged", "defective", "replacement"}.intersection(query_words):
                if filename == "product_faq.md":
                    score += 5

            # Save only matching passages
            if score >= 3:
                matches.append(
                    (score, file_path.name, passage.strip())
                )

    # Sort highest scoring passages first
    matches.sort(key=lambda item: item[0], reverse=True)

    if not matches:
        return "NO_MATCH: No relevant company policy found."

    results = []

    for score, filename, passage in matches[:5]:
        results.append(
            f"Source: {filename}\n"
            f"Passage: {passage}"
        )

    return "\n\n".join(results)


def create_knowledge_agent(model_client):
    """Create the AutoGen Knowledge Base Agent."""

    return AssistantAgent(
        name="Knowledge_Base_Agent",
        model_client=model_client,
        tools=[search_kb],
        description="Searches SmartCart company policies and FAQs.",
        system_message="""
You are SmartCart's Knowledge Base Agent.

Your responsibility is to search company policies.

Rules:
1. Read the customer complaint and Query Agent analysis.
2. Call the search_kb tool using relevant search terms.
3. Return matching passages and source filenames.
4. Never invent company policies.
5. If NO_MATCH is returned, report that no policy was found.
6. Do not write the final customer response.
"""
    )
