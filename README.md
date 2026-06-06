# Reseacrh-Q-A-Agent-
AI-powered research agent built with LangGraph, LangChain, Groq and SerpAPI. Collects information from Google, Wikipedia, and community discussions, analyzes multiple sources, and generates structured, evidence-based research reports.


---

## Features

- **Google Search**: Retrieves fresh, relevant results using SerpAPI.  
- **Wikipedia Search**: Collects structured knowledge from Wikipedia.  
- **Community Discussions**: Integrates insights from Reddit and other forums.  
- **Multi-source Analysis**: Each source is independently analyzed by Groq-powered LLMs.  
- **Synthesis Engine**: Combines Google, Wikipedia, and community analyses into a coherent final answer.  
- **Evidence-Based Reports**: Outputs structured responses with clear reasoning and references.  
- **Graph Workflow**: Powered by LangGraph for modular, stateful execution.

---

## Tech Stack

| Component | Purpose |
|-----------|---------|
| **LangGraph** | Orchestrates the research workflow as a state graph |
| **LangChain** | Provides LLM integration and structured output handling |
| **Groq** | Accelerates inference for analysis and synthesis |
| **SerpAPI** | Fetches Google search results |
| **Wikipedia API** | Retrieves encyclopedia-style knowledge |
| **Reddit API** | Collects community discussions and comments |

---

## Project Structure

```
research-agent/
│── multisearchagent.py       # Core LangGraph workflow
│── web_operations.py         # API wrappers (Google, Wikipedia, Reddit)
│── snapshot_operations.py    # Snapshotting and state persistence
│── prompt.py                 # Prompt templates for analysis & synthesis
│── README.md                 # Documentation
│── requirements.txt          # Dependencies
```

---

## Workflow Overview

1. **Input**: User provides a research question.  
2. **Search Nodes**:  
   - Google → via SerpAPI  
   - Wikipedia → via API  
   - Reddit community discussions → via API (posts + comments)  
3. **Analysis Nodes**: Groq-powered LLM analyzes each source independently.  
4. **Synthesis Node**: Merges analyses into a final structured answer.  
5. **Output**: Evidence-based research report.

---



---

## Usage

```python
from multisearchagent import app

# Example query
state = {"user_question": "What are the health impacts of intermittent fasting?"}
result = app.invoke(state)

print(result["final_answer"])
```

---

## Example Output

**Question:** *What are the benefits of renewable energy adoption?*  

**Answer (synthesized):**
- Google: Highlights economic growth and reduced emissions.  
- Wikipedia: Provides historical context and global adoption rates.  
- Reddit: Shares personal experiences with solar panels and community debates.  

**Final Report:**  
Renewable energy adoption reduces greenhouse gas emissions, supports energy independence, and fosters innovation. Community discussions emphasize practical challenges like upfront costs but highlight long-term savings and sustainability.

---

## Environment Variables

Create a `.env` file with:

```
SERPAPI_KEY=your_serpapi_key
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_app_name
```

---


## Contributing

Pull requests are welcome! Please open an issue first to discuss major changes.

---

## License

MIT License. Free to use, modify, and distribute.
