import os
from github import Github

class GitHubService:
    def __init__(self, user_id: str):
        user_key = user_id.lower().strip()  # ensure user1 / user2
        token = os.getenv(f"GITHUB_TOKEN_{user_key.upper()}")
        username = os.getenv(f"GITHUB_USERNAME_{user_key.upper()}")

        if not token or not username:
            raise ValueError(f"Missing GitHub token or username for {user_key}")

        self.client = Github(token)
        self.username = username

    def list_repos(self):
        user = self.client.get_user(self.username)
        return [repo.full_name for repo in user.get_repos()]

    def list_starred_repos(self):
        user = self.client.get_user(self.username)
        return [repo.full_name for repo in user.get_starred()]

    def list_issues(self):
        user = self.client.get_user(self.username)
        issues = user.get_issues()
        return [{"title": i.title, "repo": i.repository.name, "state": i.state} for i in issues]

    def list_branches(self, repo_name: str):
        repo = self.client.get_repo(f"{self.username}/{repo_name}")
        return [branch.name for branch in repo.get_branches()]

    def list_commits(self, repo_name: str):
        repo = self.client.get_repo(f"{self.username}/{repo_name}")
        return [{"message": c.commit.message, "sha": c.sha[:7]} for c in repo.get_commits()]

    def search_repositories(self, query: str):
        results = self.client.search_repositories(query)
        return [repo.full_name for repo in results[:10]]

    def list_prs(self):
        repos = self.list_repos()
        all_prs = []
        for repo_name in repos:
            try:
                repo = self.client.get_repo(repo_name)
                prs = repo.get_pulls(state="open")
                all_prs.extend([f"{repo_name}: {pr.title}" for pr in prs])
            except:
                pass
        return all_prs
