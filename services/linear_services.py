import os
import requests

class LinearService:
    BASE_URL = "https://api.linear.app/graphql"

    def __init__(self, user_id: str):
        user_key = user_id.lower().strip()  # user1 / user2
        self.api_key = os.getenv(f"LINEAR_API_KEY_{user_key.upper()}")
        self.email   = os.getenv(f"LINEAR_EMAIL_{user_key.upper()}")

        if not self.api_key or not self.email:
            raise ValueError(f"Missing Linear credentials for {user_key}")

    def query(self, query_string):
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
        data = {"query": query_string}
        r = requests.post(self.BASE_URL, json=data, headers=headers)
        return r.json()

    def list_in_progress(self):
        query = f"""
        query {{
          issues(filter: {{
            assignee: {{ email: {{ eq: "{self.email}" }} }},
            state: {{ name: {{ eq: "In Progress" }} }}
          }}) {{
            nodes {{ id title state {{ name }} }}
          }}
        }}
        """
        return self.query(query)

    def list_high_priority(self):
        query = f"""
        query {{
          issues(filter: {{
            assignee: {{ email: {{ eq: "{self.email}" }} }},
            priority: {{ gte: 7 }}
          }}) {{
            nodes {{ title priority state {{ name }} }}
          }}
        }}
        """
        return self.query(query)

    def list_teams(self):
        return self.query("""{ teams { nodes { id name }}}""")

    def list_projects(self):
        return self.query("""{ projects { nodes { id name state }}}""")

    def list_issues(self):
        query = f"""
        query {{
          issues(filter: {{
            assignee: {{ email: {{ eq: "{self.email}" }} }}
          }}) {{
            nodes {{ id title state {{ name }} }}
          }}
        }}
        """
        return self.query(query)

    def create_issue(self, title: str, desc: str):
        mutation = f"""
        mutation {{
          issueCreate(input: {{
            title: "{title}",
            description: "{desc}"
          }}) {{
            issue {{ id title }}
          }}
        }}
        """
        return self.query(mutation)
