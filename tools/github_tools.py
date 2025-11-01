from crewai.tools import tool
from services.github_services import GitHubService

@tool("github_list_repos")
def github_list_repos(user: str) -> str:
    """Lists all GitHub repositories for the given user."""
    gh = GitHubService(user.lower())
    repos = gh.list_repos()
    return f"📂 Repositories for {user}:\n" + "\n".join(repos)

@tool("github_list_prs")
def github_list_prs(user: str) -> str:
    """Lists open pull requests for the given user."""
    gh = GitHubService(user.lower())
    prs = gh.list_prs()
    if not prs:
        return f"No open PRs found for {user}."
    formatted = "\n".join([f"{pr['title']} ({pr['repo']} #{pr['number']})" for pr in prs])
    return f"🔀 Open PRs for {user}:\n{formatted}"

@tool("github_list_starred")
def github_list_starred(user: str) -> str:
    """Lists starred GitHub repositories for the given user."""
    gh = GitHubService(user.lower())
    stars = gh.list_starred_repos()
    return f"⭐ Starred repos for {user}:\n" + "\n".join(stars)

@tool("github_list_issues")
def github_list_issues(user: str) -> str:
    """Lists GitHub issues for the given user."""
    gh = GitHubService(user.lower())
    issues = gh.list_issues()
    return f"🐛 Issues for {user}:\n" + "\n".join([f"{i['title']} ({i['repo']})" for i in issues])

@tool("github_list_branches")
def github_list_branches(user: str, repo_name: str) -> str:
    """Lists branches in the specified GitHub repository for the given user."""
    gh = GitHubService(user.lower())
    branches = gh.list_branches(repo_name)
    return f"🌿 Branches in {repo_name} for {user}:\n" + "\n".join(branches)

@tool("github_list_commits")
def github_list_commits(user: str, repo_name: str) -> str:
    """Lists recent commits in the specified GitHub repository for the given user."""
    gh = GitHubService(user.lower())
    commits = gh.list_commits(repo_name)
    return f"📦 Commits in {repo_name}:\n" + "\n".join([f"{c['sha']} - {c['message']}" for c in commits[:10]])

@tool("github_search_repos")
def github_search_repos(query: str) -> str:
    """Searches GitHub repositories globally using the given query."""
    gh = GitHubService("user1")  # search global
    repos = gh.search_repositories(query)
    return f"🔍 Search results for '{query}':\n" + "\n".join(repos)
