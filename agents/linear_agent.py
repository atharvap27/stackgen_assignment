from crewai import Agent, Task, Crew
from tools.linear_tools import (
    linear_list_issues,
    linear_in_progress,
    linear_high_priority,
    linear_teams,
    linear_projects,
    linear_create_issue
)
from litellm_wrapper import LiteLLMWrapper

gemini_llm = LiteLLMWrapper(model="gemini/gemini-2.5-flash")

def run_linear_agent(query: str, user_key: str):
    user_key = user_key.lower()

    linear_ai = Agent(
        role="Linear Assistant",
        goal="Fetch project/task/issue data from Linear based on user query.",
        backstory="Expert in Linear project management, tasks, states, and priorities.",
        tools=[
            linear_list_issues,
            linear_in_progress,
            linear_high_priority,
            linear_teams,
            linear_projects,
            linear_create_issue
        ],
        verbose=False,
        llm=gemini_llm
    )

    linear_task = Task(
        description=f"""
User query: "{query}"
Internal user key: {user_key}

⚠️ ALWAYS call Linear tools using "{user_key}"
""",
        agent=linear_ai,
        expected_output="Just the Linear result, one line per item.",
        input={"query": query, "user": user_key}
    )

    crew = Crew(
        agents=[linear_ai],
        tasks=[linear_task],
        process="sequential",
        verbose=True
    )

    return crew.kickoff()
