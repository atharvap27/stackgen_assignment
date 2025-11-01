from crewai import Agent, Task, Crew
from tools.github_rag import github_repo_qa
from tools.github_tools import (
    github_list_repos,
    github_list_prs,
    github_list_issues,
    github_list_starred,
    github_list_branches,
    github_list_commits,
    github_search_repos
)
from litellm_wrapper import LiteLLMWrapper

gemini_llm = LiteLLMWrapper(model="gemini/gemini-2.5-flash")

def run_github_agent(query: str, user_key: str):
    user_key = user_key.lower()  # normalize

    github_ai = Agent(
        role="GitHub Assistant",
        goal="Fetch GitHub data based on user query.",
        backstory="Expert in GitHub API, repositories, pull requests, issues, branches, commits, and stars.",
        tools=[
            github_list_repos,
            github_list_prs,
            github_list_issues,
            github_list_starred,
            github_list_branches,
            github_list_commits,
            github_search_repos,
            
        ],
        verbose=False,
        llm=gemini_llm
    )

    github_task = Task(
        description=f"""
User query: "{query}"
Internal user key: {user_key}

⚠️ IMPORTANT ⚠️  
ALWAYS call GitHub tools using this user key: "{user_key}"

Example:
Action: github_list_repos
Action Input: {{"user": "{user_key}"}}
""",
        agent=github_ai,
        expected_output="Just the GitHub result, one line per item.",
        input={"query": query, "user": user_key}
    )

    crew = Crew(
        agents=[github_ai],
        tasks=[github_task],
        process="sequential",
        verbose=True
    )

    return crew.kickoff()



def run_github_rag(query: str, user_key: str):
    user_key = user_key.lower()  # normalize

    github_rag_ai = Agent(
        role="GitHub Assistant",
        goal="Fetch GitHub repo data based on user query.",
        backstory="Expert in extracting code and files from GitHub repositories using RAG.",
        tools=[
            github_repo_qa
        ],
        verbose=False,
        llm=gemini_llm
    )

    github_rag_task = Task(
        description=f"""
User query: "{query}"
Internal user key: {user_key}   
⚠️ IMPORTANT ⚠️ 
ALWAYS call GitHub RAG tool using this user key: "{user_key}"
Example:
Action: github_repo_qa
Action Input: {{"user": "{user_key}", "repo_name": "owner/repo"}}
""",
        agent=github_rag_ai,
        expected_output="Just the GitHub RAG result, concise answer with file references and code snippets.",
        input={"query": query, "user": user_key}
    )

    crew = Crew(
        agents=[github_rag_ai],
        tasks=[github_rag_task],
        process="sequential",
        verbose=True
    )

    return crew.kickoff()
