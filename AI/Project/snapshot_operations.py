from web_operations import (
    serp_search,
    wikipedia_search,
    reddit_search_api
)

from groq import Groq
from dotenv import load_dotenv

import os
import json

load_dotenv()

# ==================================================
# GROQ CLIENT
# ==================================================
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ==================================================
# SAFE FORMATTER
# ==================================================
def safe_format(data):

    if not data:
        return "No data found"

    try:
        return json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        )

    except Exception:
        return str(data)


# ==================================================
# LLM ANALYSIS
# ==================================================
def analyze(
    query,
    google,
    wiki,
    community
):

    prompt = f"""
You are a senior research analyst.

Your job is to synthesize information from:

1. Google Search
2. Wikipedia
3. Community Discussions
   (Reddit, Quora, Forums, User Experiences)

RULES:

- Do NOT repeat raw JSON
- Merge duplicate information
- Prefer Wikipedia for factual information
- Prefer community discussions for real-world experiences
- Mention uncertainty if sources disagree
- Be factual, concise and practical
- Use markdown formatting

==================================================
QUESTION
==================================================

{query}

==================================================
GOOGLE RESULTS
==================================================

{safe_format(google)}

==================================================
WIKIPEDIA RESULTS
==================================================

{safe_format(wiki)}

==================================================
COMMUNITY RESULTS
==================================================

{safe_format(community)}

==================================================
OUTPUT FORMAT
==================================================

# Short Summary

# Key Facts

# Community Insights

# Recommendations

# Final Conclusion
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content":
                        "You are a world-class research analyst."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return (
            response
            .choices[0]
            .message
            .content
        )

    except Exception as e:

        return f"❌ LLM Error: {e}"


# ==================================================
# RESEARCH PIPELINE
# ==================================================
def research_pipeline(query):

    print("\n🚀 AI Research Pipeline Started\n")

    try:

        # -----------------------------------------
        # GOOGLE
        # -----------------------------------------
        print("🔎 Collecting Google Results...")

        google = (
            serp_search(query)
            or {}
        )

        # -----------------------------------------
        # WIKIPEDIA
        # -----------------------------------------
        print("📘 Collecting Wikipedia Results...")

        wiki = (
            wikipedia_search(query)
            or {}
        )

        # -----------------------------------------
        # COMMUNITY SEARCH
        # -----------------------------------------
        print("💬 Collecting Community Discussions...")

        community = (
            reddit_search_api(query)
            or {}
        )

        # -----------------------------------------
        # DEBUG
        # -----------------------------------------
        print(
            "\n================ DEBUG ================\n"
        )

        print(
            "Google Results:",
            len(
                google.get(
                    "organic",
                    []
                )
            )
        )

        print(
            "Wikipedia Found:",
            bool(wiki)
        )

        print(
            "Community Results:",
            community.get(
                "total",
                0
            )
        )

        # -----------------------------------------
        # ANALYSIS
        # -----------------------------------------
        print(
            "\n🧠 Running LLM Analysis...\n"
        )

        final_answer = analyze(
            query=query,
            google=google,
            wiki=wiki,
            community=community
        )

        print(
            "\n================ FINAL ANSWER ================\n"
        )

        print(final_answer)

        return final_answer

    except Exception as e:

        print(
            f"\n❌ Pipeline Error: {e}"
        )

        return None


# ==================================================
# CLI
# ==================================================
if __name__ == "__main__":

    print(
        "\n🤖 AI Research Agent Ready"
    )

    print(
        "Type 'exit' to quit.\n"
    )

    while True:

        query = input(
            "Ask: "
        ).strip()

        if query.lower() == "exit":

            print(
                "👋 Goodbye"
            )

            break

        research_pipeline(query)