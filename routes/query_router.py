from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import Any, Dict, Optional

# ---- Import your agent runners here ----
from agents.github_agent import run_github_agent
from agents.linear_agent import run_linear_agent
from router_logic.llm_router import route_to_agent   # Your LLM routing function
from tools.github_rag import github_repo_qa_direct  # Import RAG function (not the tool)

router = APIRouter()

# Add this mapping at the top of query_router.py
USER_MAP = {
    "alice": "user1",
    "bob": "user2"
}
# Request body schema
class QueryRequest(BaseModel):
    query: str

# Response model (optional)
class QueryResponse(BaseModel):
    agent: str
    user: str
    repo: Optional[str] = None
    result: Any


@router.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    """
    Accepts user query, routes to correct agent via LLM, returns agent result.
    """
    query = request.query

    # 🔥 Call the LLM router (it returns agent + user + repo)
    routing_decision: Dict[str, str] = route_to_agent(query)
    agent = routing_decision.get("agent")
    user = routing_decision.get("user")
    repo = routing_decision.get("repo")
    
    # Check if query is unrelated to GitHub or Linear
    if agent == "none":
        return QueryResponse(
            agent=agent,
            user=user,
            repo=repo,
            result="I cannot answer this question."
        )
    
    # Check if user is ambiguous (unknown) for GitHub/Linear queries
    if user == "unknown" and agent in ["github", "github_rag", "linear"]:
        return QueryResponse(
            agent=agent,
            user=user,
            repo=repo,
            result="Please specify which user (Alice or Bob) you're asking about."
        )
    
    user_key = USER_MAP.get(user, user)  # defaults to original if not found

    if agent == "github":
        result = run_github_agent(query, user_key)
        # Extract raw text from CrewAI result
        if isinstance(result, dict) and 'raw' in result:
            result = result['raw']
        elif hasattr(result, 'raw'):
            result = result.raw
    elif agent == "github_rag" and repo:
        # RAG-based repo Q&A - use the direct function
        result = github_repo_qa_direct(user_key, repo, query)
    elif agent == "linear":
        result = run_linear_agent(query, user_key)
        # Extract raw text from CrewAI result
        if isinstance(result, dict) and 'raw' in result:
            result = result['raw']
        elif hasattr(result, 'raw'):
            result = result.raw
    else:
        result = "I cannot answer this question."

    return QueryResponse(
        agent=agent,
        user=user,
        repo=repo,
        result=result
    )
