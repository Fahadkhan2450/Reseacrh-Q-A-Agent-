import os
import requests

from dotenv import load_dotenv
from urllib.parse import quote_plus
from functools import lru_cache

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


# ==================================================
# SAFE REQUEST
# ==================================================
def safe_get(
    url,
    params=None,
    headers=None,
    timeout=15
):

    default_headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json,text/plain,*/*",
    }

    if headers:
        default_headers.update(headers)

    try:

        response = requests.get(
            url,
            params=params,
            headers=default_headers,
            timeout=timeout
        )

        response.raise_for_status()

        try:
            return response.json()

        except Exception:
            return None

    except Exception as e:

        print(f"Request Error: {e}")
        return None


# ==================================================
# GOOGLE SEARCH
# ==================================================
@lru_cache(maxsize=128)
def serp_search(
    query: str,
    engine="google"
):

    if not SERPAPI_API_KEY:

        print("❌ Missing SERPAPI_API_KEY")
        return {}

    print(f"\n🔎 Google Search: {query}")

    data = safe_get(
        "https://serpapi.com/search.json",
        params={
            "q": query,
            "engine": engine,
            "api_key": SERPAPI_API_KEY
        }
    )

    if not data:
        return {}

    organic = data.get("organic_results", [])

    results = []

    for item in organic[:10]:

        results.append({
            "title": item.get("title"),
            "snippet": item.get("snippet"),
            "link": item.get("link"),
            "source": item.get("source"),
            "position": item.get("position")
        })

    return {
        "organic": results,
        "total_results": len(results)
    }


# ==================================================
# WIKIPEDIA SEARCH
# ==================================================
@lru_cache(maxsize=128)
def wikipedia_search(query: str):

    print(f"\n📘 Wikipedia Search: {query}")

    search_data = safe_get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "origin": "*"
        }
    )

    if not search_data:
        return {}

    results = (
        search_data
        .get("query", {})
        .get("search", [])
    )

    if not results:
        return {}

    page = results[0]

    return {
        "title": page.get("title"),
        "snippet": page.get("snippet", ""),
        "pageid": page.get("pageid")
    }


# ==================================================
# COMMUNITY INSIGHTS SEARCH
# (Google + Reddit + Quora + Forums)
# ==================================================
def reddit_search_api(query: str):

    print(
        f"\n💬 Community Search: {query}"
    )

    community_query = (
        f"{query} "
        "reddit OR quora OR forum "
        "experience advice discussion opinion"
    )

    data = safe_get(
        "https://serpapi.com/search.json",
        params={
            "engine": "google",
            "q": community_query,
            "api_key": SERPAPI_API_KEY
        }
    )

    if not data:
        return {
            "parsed_posts": [],
            "total": 0
        }

    organic = data.get(
        "organic_results",
        []
    )

    posts = []

    for item in organic[:15]:

        posts.append({

            "title":
                item.get("title"),

            "snippet":
                item.get("snippet"),

            "url":
                item.get("link"),

            "source":
                item.get("source"),

            "position":
                item.get("position")
        })

    return {

        "parsed_posts":
            posts,

        "total":
            len(posts)
    }


# ==================================================
# DUMMY FUNCTION
# (keeps existing graph code working)
# ==================================================
def reddit_post_retrieval(urls):

    return {
        "posts": [],
        "total_posts": 0
    }