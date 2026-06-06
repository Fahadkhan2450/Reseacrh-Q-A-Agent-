from typing import Dict, Any


# ==================================================
# PROMPT TEMPLATES
# ==================================================
class PromptTemplates:

    # ==================================================
    # GOOGLE ANALYSIS
    # ==================================================
    @staticmethod
    def google_analysis_system() -> str:
        return """
You are a professional research analyst.

Analyze Google search results.

Focus on:

- Facts
- Official information
- Documentation
- Statistics
- Trusted sources
- Recent information

Do not invent information.

Summarize the most useful findings.
"""

    @staticmethod
    def google_analysis_user(
        user_question: str,
        google_results: str
    ) -> str:

        return f"""
QUESTION:
{user_question}

GOOGLE RESULTS:
{google_results}

Extract:

- Important facts
- Key findings
- Reliable information
- Useful resources
"""


    # ==================================================
    # WIKIPEDIA ANALYSIS
    # ==================================================
    @staticmethod
    def wikipedia_analysis_system() -> str:
        return """
You are a factual encyclopedia assistant.

Use ONLY the supplied Wikipedia data.

Focus on:

- Definitions
- Historical context
- Core concepts
- Important facts
- Background information

Do not hallucinate.
"""

    @staticmethod
    def wikipedia_analysis_user(
        user_question: str,
        wiki_results: str
    ) -> str:

        return f"""
QUESTION:
{user_question}

WIKIPEDIA DATA:
{wiki_results}

Provide factual insights and background information.
"""


    # ==================================================
    # COMMUNITY ANALYSIS
    # ==================================================
    @staticmethod
    def reddit_analysis_system() -> str:
        return """
You are a community insights analyst.

The supplied results come from searches focused on:

- Reddit discussions
- User experiences
- Community advice
- Public opinions
- Personal stories

Your task is to identify:

1. Common opinions
2. Frequently repeated advice
3. Success stories
4. Common mistakes
5. Risks and warnings
6. Community consensus
7. Contradicting viewpoints

IMPORTANT:

- Separate FACT from OPINION
- Community discussions are not authoritative facts
- Mention uncertainty when needed
- Highlight recurring themes
"""

    @staticmethod
    def reddit_analysis_user(
        user_question: str,
        reddit_results: str,
        reddit_post_data: str = ""
    ) -> str:

        return f"""
QUESTION:
{user_question}

COMMUNITY DISCUSSION RESULTS:
{reddit_results}

Extract:

- Common opinions
- Practical advice
- Recommendations
- Risks
- Warnings
- Community consensus
"""


    # ==================================================
    # FINAL SYNTHESIS
    # ==================================================
    @staticmethod
    def synthesis_system() -> str:
        return """
You are a senior research synthesizer.

Combine information from:

1. Google Search
2. Wikipedia
3. Community Discussions

Rules:

- Merge duplicate information
- Prefer Wikipedia for factual background
- Prefer Google for current information
- Use Community Discussions for experiences
- Clearly separate facts from opinions
- Mention disagreements if they exist
- Never invent information
- Produce a complete answer

Output format:

# Summary

# Key Facts

# Community Insights

# Important Considerations

# Final Answer
"""

    @staticmethod
    def synthesis_user(
        user_question: str,
        google_analysis: str,
        wikipedia_analysis: str,
        reddit_analysis: str,
    ) -> str:

        return f"""
QUESTION:
{user_question}

GOOGLE ANALYSIS:
{google_analysis}

WIKIPEDIA ANALYSIS:
{wikipedia_analysis}

COMMUNITY ANALYSIS:
{reddit_analysis}

Generate the final answer.
"""


# ==================================================
# MESSAGE BUILDER
# ==================================================
def create_message_pair(
    system_prompt: str,
    user_prompt: str
) -> list[Dict[str, Any]]:

    return [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]


# ==================================================
# GOOGLE ANALYSIS
# ==================================================
def get_google_analysis_messages(
    user_question: str,
    google_results: str
):

    return create_message_pair(
        PromptTemplates.google_analysis_system(),
        PromptTemplates.google_analysis_user(
            user_question,
            google_results
        )
    )


# ==================================================
# WIKIPEDIA ANALYSIS
# ==================================================
def get_wikipedia_analysis_messages(
    user_question: str,
    wiki_results: str
):

    return create_message_pair(
        PromptTemplates.wikipedia_analysis_system(),
        PromptTemplates.wikipedia_analysis_user(
            user_question,
            wiki_results
        )
    )


# ==================================================
# COMMUNITY ANALYSIS
# ==================================================
def get_reddit_analysis_messages(
    user_question: str,
    reddit_results: str,
    reddit_post_data: str = ""
):

    return create_message_pair(
        PromptTemplates.reddit_analysis_system(),
        PromptTemplates.reddit_analysis_user(
            user_question,
            reddit_results,
            reddit_post_data
        )
    )


# ==================================================
# FINAL SYNTHESIS
# ==================================================
def get_synthesis_messages(
    user_question: str,
    google_analysis: str,
    wikipedia_analysis: str,
    reddit_analysis: str,
):

    return create_message_pair(
        PromptTemplates.synthesis_system(),
        PromptTemplates.synthesis_user(
            user_question,
            google_analysis,
            wikipedia_analysis,
            reddit_analysis
        )
    )