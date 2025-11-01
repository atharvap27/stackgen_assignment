# import os
# import requests
# from dotenv import load_dotenv

# import re
# load_dotenv()

# USERS = {
#     "alice": "user1",
#     "bob": "user2"
# }

# # ==== GITHUB API FUNCTIONS ====

# GITHUB_API = "https://api.github.com"

# def gh_headers(token):
#     return {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}

# def list_repos(user_key):
#     username = os.getenv(f"GITHUB_USERNAME_{user_key.upper()}")
#     token = os.getenv(f"GITHUB_TOKEN_{user_key.upper()}")

#     url = f"{GITHUB_API}/users/{username}/repos"
#     r = requests.get(url, headers=gh_headers(token))
#     try:
#         data = r.json()
#     except Exception:
#         print("Error decoding JSON response")
#         return []

#     if isinstance(data, dict) and "message" in data:
#         print(f"GitHub API error: {data['message']}")
#         return []

#     return [repo["name"] for repo in data]


# def count_user_prs(user_key):
#     username = os.getenv(f"GITHUB_USERNAME_{user_key.upper()}")
#     token = os.getenv(f"GITHUB_TOKEN_{user_key.upper()}")

#     url = f"{GITHUB_API}/search/issues"
#     q = f"author:{username} type:pr state:open"
#     r = requests.get(url, headers=gh_headers(token), params={"q": q})
#     return r.json().get("total_count", 0)

# def list_repo_prs(user_key, repo):
#     username = os.getenv(f"GITHUB_USERNAME_{user_key.upper()}")
#     token = os.getenv(f"GITHUB_TOKEN_{user_key.upper()}")

#     url = f"{GITHUB_API}/repos/{username}/{repo}/pulls"
#     r = requests.get(url, headers=gh_headers(token))
#     data = r.json()

#     return [f"#{pr['number']} - {pr['title']}" for pr in data]

# # ==== LINEAR API FUNCTIONS ====

# LINEAR_API = "https://api.linear.app/graphql"

# def linear_query(api_key, email):
#     query = """
#     query ($email: String!) {
#       issues(filter: {assignee: {users: {email: {eq: $email}}}}) {
#         nodes { title state }
#       }
#     }
#     """
#     payload = {"query": query, "variables": {"email": email}}
#     headers = {"Authorization": api_key, "Content-Type": "application/json"}
#     r = requests.post(LINEAR_API, json=payload, headers=headers)
#     return r.json()["data"]["issues"]["nodes"]

# def get_linear_issues(user_key):
#     email = os.getenv(f"LINEAR_EMAIL_{user_key.upper()}")
#     api_key = os.getenv(f"LINEAR_API_KEY_{user_key.upper()}")

#     issues = linear_query(api_key, email)
#     return [f"{i['title']} ({i['state']})" for i in issues]


# # ==== ROUTER + INTERACTION ====

# def detect_user(text):
#     for u in USERS.keys():
#         if u in text.lower():
#             return USERS[u]
#     return None


# def detect_platform(text):
#     t = text.lower()

#     github_keywords = [
#         "github", "repo", "repository", "pull request", "pr", 
#         "merge request", "branches", "branch", "commits", "commit",
#         "fork", "star", "clone", "code", "source code", 
#         "file", "files", "directory", "project", "version control"
#     ]

#     linear_keywords = [
#         "linear", "issue", "issues", "task", "ticket", "bug", "story",
#         "assign", "assigned", "label", "priority", "board", 
#         "sprint", "workflow", "backlog", "in progress", "todo"
#     ]

#     # Regex for PR or issue references (#123 etc)
#     pr_pattern = r"(pr\s?#?\d+|pull\s?request\s?#?\d+)"
#     issue_pattern = r"(issue\s?#?\d+|task\s?#?\d+)"

#     # Match PR cases
#     if re.search(pr_pattern, t):
#         return "github"

#     # Match issue/task references
#     if re.search(issue_pattern, t):
#         return "linear"

#     # Keyword matching
#     if any(word in t for word in github_keywords):
#         return "github"
#     if any(word in t for word in linear_keywords):
#         return "linear"

#     return None


# def interact():
#     print("Ask anything (type exit to quit)\n")

#     while True:
#         q = input("You: ").strip()
#         if q == "exit":
#             break

#         # detect user
#         user = detect_user(q)
#         if not user:
#             user_input = input("Which user? (Alice/Bob): ").lower()
#             user = USERS.get(user_input)
#             if not user:
#                 print("Invalid user")
#                 continue

#         # detect platform
#         platform = detect_platform(q)
#         if not platform:
#             print("I can answer only GitHub or Linear queries")
#             continue

#         # route
#         if platform == "github":
#             if "repo" in q and "pr" in q:
#                 repo = q.split("repo")[-1].strip().split()[0]
#                 print(list_repo_prs(user, repo))
#             elif "repo" in q:
#                 print(list_repos(user))
#             elif "pr" in q:
#                 print(count_user_prs(user))
#             else:
#                 print("GitHub: not understood")

#         elif platform == "linear":
#             print(get_linear_issues(user))

# if __name__ == "__main__":
#     interact()




# # import os
# # import json
# # import requests
# # from dotenv import load_dotenv
# # import google.generativeai as genai

# # load_dotenv()

# # # ================== USER MAPPING ==================

# # USERS = {
# #     "alice": "user1",
# #     "bob": "user2"
# # }

# # # ================== GEMINI CONFIG ==================

# # genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# # model = genai.GenerativeModel("gemini-2.0-flash")

# # def llm_route(query):
# #     prompt = f"""
# # You are an AI router for developer queries.

# # Platforms:
# # - "github" = repos, PRs, commits, code files
# # - "linear" = issues, tasks, tickets, bugs

# # Routing rules:
# # - The word "issue" ALWAYS means Linear unless a repo name is mentioned.
# # - If query contains "PR", "pull request", "repo", "code" → GitHub
# # - Extract user (alice/bob) if found else null
# # - Extract repo if found else null
# # - Only return JSON, no text

# # Return JSON keys:
# # - platform
# # - intent (list_repos, count_prs, list_repo_prs, list_linear_issues)
# # - user
# # - repo

# # User query: "{query}"
# # """

# #     res = model.generate_content(prompt)
# #     try:
# #         out = res.text.replace("```json","").replace("```","").strip()
# #         return json.loads(out)
# #     except:
# #         return None


# # # ================== GITHUB API ==================

# # GITHUB_API = "https://api.github.com"

# # def gh_headers(token):
# #     return {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}

# # def list_repos(user_key):
# #     username = os.getenv(f"GITHUB_USERNAME_{user_key.upper()}")
# #     token = os.getenv(f"GITHUB_TOKEN_{user_key.upper()}")

# #     r = requests.get(f"{GITHUB_API}/users/{username}/repos", headers=gh_headers(token))
# #     data = r.json()

# #     if isinstance(data, dict) and "message" in data:
# #         return f"GitHub error: {data['message']}"
# #     return [repo["name"] for repo in data]

# # def count_user_prs(user_key):
# #     username = os.getenv(f"GITHUB_USERNAME_{user_key.upper()}")
# #     token = os.getenv(f"GITHUB_TOKEN_{user_key.upper()}")

# #     url = f"{GITHUB_API}/search/issues"
# #     q = f"author:{username} type:pr state:open"
# #     r = requests.get(url, headers=gh_headers(token), params={"q": q})
# #     return r.json().get("total_count", 0)

# # def list_repo_prs(user_key, repo):
# #     username = os.getenv(f"GITHUB_USERNAME_{user_key.upper()}")
# #     token = os.getenv(f"GITHUB_TOKEN_{user_key.upper()}")

# #     r = requests.get(f"{GITHUB_API}/repos/{username}/{repo}/pulls", headers=gh_headers(token))
# #     data = r.json()

# #     if isinstance(data, dict) and "message" in data:
# #         return f"Error: {data['message']}"
    
# #     if not data:
# #         return "No PRs found."
    
# #     return [f"#{pr['number']} - {pr['title']}" for pr in data]

# # # ================== LINEAR API ==================

# # LINEAR_API = "https://api.linear.app/graphql"

# # def linear_query(api_key, email):
# #     query = """
# #     query ($email: String!) {
# #       users(filter: {email: {eq: $email}}) {
# #         nodes {
# #           id
# #         }
# #       }
# #     }
# #     """

# #     headers = {"Authorization": api_key, "Content-Type": "application/json"}
# #     r = requests.post(LINEAR_API, json={"query": query, "variables": {"email": email}}, headers=headers)
# #     data = r.json()

# #     try:
# #         user_id = data["data"]["users"]["nodes"][0]["id"]
# #     except:
# #         print("⚠️ Linear user not found for:", email)
# #         return []

# #     issues_query = """
# #     query ($userId: String!) {
# #       issues(filter: {assignee: {id: {eq: $userId}}}) {
# #         nodes { 
# #           title 
# #           state { name }
# #         }
# #       }
# #     }
# #     """

# #     payload = {"query": issues_query, "variables": {"userId": user_id}}
# #     r2 = requests.post(LINEAR_API, json=payload, headers=headers)

# #     try:
# #         return r2.json()["data"]["issues"]["nodes"]
# #     except:
# #         print("⚠️ Failed fetching issues:", r2.text)
# #         return []



# # def get_linear_issues(user_key):
# #     email = os.getenv(f"LINEAR_EMAIL_{user_key.upper()}")
# #     api_key = os.getenv(f"LINEAR_API_KEY_{user_key.upper()}")

# #     issues = linear_query(api_key, email)
# #     if not issues:
# #         return ["No issues found or API error"]
    
# #     return [f"{i['title']} ({i['state']})" for i in issues]


# # # ================== MAIN CHAT LOOP ==================

# # def interact():
# #     print("\n🤖 Ask me anything about GitHub repos/PRs or Linear tasks!")
# #     print("Type **exit** to quit.\n")

# #     while True:
# #         q = input("You: ").strip()
# #         if q.lower() == "exit":
# #             break

# #         route = llm_route(q)
# #         if not route:
# #             print("⚠️ Could not understand. Try again.")
# #             continue

# #         platform = route["platform"]
# #         intent = route["intent"]
# #         user = route.get("user")
# #         repo = route.get("repo")

# #         # Ask user if missing
# #         if not user:
# #             user_input = input("Which user? (Alice/Bob): ").lower()
# #             user = USERS.get(user_input)
# #             if not user:
# #                 print("❌ Invalid user")
# #                 continue

# #         if platform == "github":
# #             if intent == "list_repos":
# #                 print("📁 Repos:", list_repos(user))

# #             elif intent == "count_prs":
# #                 print("🔢 PR Count:", count_user_prs(user))

# #             elif intent == "list_repo_prs":
# #                 if not repo:
# #                     repo = input("Repo name: ")
# #                 print("📌 PRs:", list_repo_prs(user, repo))

# #             else:
# #                 print("❓ Unsupported GitHub action")

# #         elif platform == "linear":
# #             print("📝 Issues:", get_linear_issues(user))

# #         else:
# #             print("❓ Unknown platform")


# # if __name__ == "__main__":
# #     interact()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.staticfiles import StaticFiles
import os
from routes.query_router import router  # importing your APIRouter instance
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# Secret key for signing cookies (keep it secret!)
app.add_middleware(SessionMiddleware, secret_key="supersecret-key")
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root path
# @app.get("/")
# def root():
#     return {"message": "Welcome to ShopBuddyAI! Use the /api/query or /api/products endpoints."}

# Include all APIs under /api
app.include_router(router, prefix="/api")
# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8002, reload=True)