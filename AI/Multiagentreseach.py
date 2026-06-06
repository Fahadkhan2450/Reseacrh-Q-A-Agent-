from dotenv import load_dotenv
from typing import Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict

from web_operations import (
    serp_search,
    wikipedia_search,
    reddit_search_api
)

from prompts import (
    get_google_analysis_messages,
    get_wikipedia_analysis_messages,
    get_reddit_analysis_messages,
    get_synthesis_messages
)

load_dotenv()

# ==================================================
# LLM
# ==================================================
llm = init_chat_model("grok")

# ==================================================
# STATE
# ==================================================
class State(TypedDict):

    messages: Annotated[list, add_messages]

    user_question: str

    google_results: dict | None
    wikipedia_results: dict | None
    reddit_results: dict | None

    google_analysis: str | None
    wikipedia_analysis: str | None
    reddit_analysis: str | None

    final_answer: str | None


# ==================================================
# SEARCH NODES
# ==================================================
def google_search(state: State):

    print("\n🔎 Running Google Search")

    return {
        "google_results":
            serp_search(
                state["user_question"]
            ) or {}
    }


def wikipedia_search_node(state: State):

    print("\n📘 Running Wikipedia Search")

    return {
        "wikipedia_results":
            wikipedia_search(
                state["user_question"]
            ) or {}
    }


def reddit_search(state: State):

    print("\n💬 Running Community Search")

    return {
        "reddit_results":
            reddit_search_api(
                state["user_question"]
            ) or {}
    }


# ==================================================
# ANALYSIS NODES
# ==================================================
def analyze_google_results(state: State):

    response = llm.invoke(
        get_google_analysis_messages(
            state["user_question"],
            state.get("google_results", {})
        )
    )

    return {
        "google_analysis":
            response.content
    }


def analyze_wikipedia_results(state: State):

    response = llm.invoke(
        get_wikipedia_analysis_messages(
            state["user_question"],
            state.get("wikipedia_results", {})
        )
    )

    return {
        "wikipedia_analysis":
            response.content
    }


def analyze_reddit_results(state: State):

    response = llm.invoke(
        get_reddit_analysis_messages(
            state["user_question"],
            state.get("reddit_results", {}),
            ""
        )
    )

    return {
        "reddit_analysis":
            response.content
    }


# ==================================================
# SYNTHESIS
# ==================================================
def synthesize_analyses(state: State):

    print("\n🧠 Synthesizing Results")

    response = llm.invoke(
        get_synthesis_messages(
            state["user_question"],
            state.get("google_analysis", ""),
            state.get("wikipedia_analysis", ""),
            state.get("reddit_analysis", "")
        )
    )

    return {
        "final_answer":
            response.content
    }


# ==================================================
# GRAPH
# ==================================================
graph = StateGraph(State)

# Search Nodes
graph.add_node(
    "google_search",
    google_search
)

graph.add_node(
    "wikipedia_search",
    wikipedia_search_node
)

graph.add_node(
    "reddit_search",
    reddit_search
)

# Analysis Nodes
graph.add_node(
    "analyze_google_results",
    analyze_google_results
)

graph.add_node(
    "analyze_wikipedia_results",
    analyze_wikipedia_results
)

graph.add_node(
    "analyze_reddit_results",
    analyze_reddit_results
)

# Synthesis
graph.add_node(
    "synthesize_analyses",
    synthesize_analyses
)

# ==================================================
# START
# ==================================================
graph.add_edge(
    START,
    "google_search"
)

graph.add_edge(
    START,
    "wikipedia_search"
)

graph.add_edge(
    START,
    "reddit_search"
)

# ==================================================
# SEARCH -> ANALYSIS
# ==================================================
graph.add_edge(
    "google_search",
    "analyze_google_results"
)

graph.add_edge(
    "wikipedia_search",
    "analyze_wikipedia_results"
)

graph.add_edge(
    "reddit_search",
    "analyze_reddit_results"
)

# ==================================================
# ANALYSIS -> SYNTHESIS
# ==================================================
graph.add_edge(
    "analyze_google_results",
    "synthesize_analyses"
)

graph.add_edge(
    "analyze_wikipedia_results",
    "synthesize_analyses"
)

graph.add_edge(
    "analyze_reddit_results",
    "synthesize_analyses"
)

# ==================================================
# END
# ==================================================
graph.add_edge(
    "synthesize_analyses",
    END
)

# ==================================================
# COMPILE
# ==================================================
app = graph.compile()