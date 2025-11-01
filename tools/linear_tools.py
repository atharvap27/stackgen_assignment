from crewai.tools import tool
from services.linear_services import LinearService

@tool("linear_list_issues")
def linear_list_issues(user: str) -> str:
    """List all issues assigned to the Linear user."""
    client = LinearService(user.lower())
    data = client.list_issues()

    issues = data.get("data", {}).get("issues", {}).get("nodes", [])
    if not issues:
        return f"No issues found for {user}"

    formatted = "\n".join([f"{i['title']} - {i['state']['name']}" for i in issues])
    return f"📝 Issues for {user}:\n{formatted}"

@tool("linear_in_progress")
def linear_in_progress(user: str) -> str:
    """List all in-progress issues for the Linear user."""
    client = LinearService(user.lower())
    data = client.list_in_progress()
    return str(data)

@tool("linear_high_priority")
def linear_high_priority(user: str) -> str:
    """List all high priority issues for the Linear user."""
    client = LinearService(user.lower())
    data = client.list_high_priority()
    return str(data)

@tool("linear_teams")
def linear_teams(user: str) -> str:
    """List all teams for the Linear user."""
    client = LinearService(user.lower())
    return str(client.list_teams())

@tool("linear_projects")
def linear_projects(user: str) -> str:
    """List all projects for the Linear user."""
    client = LinearService(user.lower())
    return str(client.list_projects())

@tool("linear_create_issue")
def linear_create_issue(user: str, title: str, desc: str) -> str:
    """Create a new issue for the Linear user with the given title and description."""
    client = LinearService(user.lower())
    data = client.create_issue(title, desc)
    return f"✅ Issue created: {data}"