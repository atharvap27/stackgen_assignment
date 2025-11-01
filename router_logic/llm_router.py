import os
import json
import google.generativeai as genai

# -------------------- Configure Gemini --------------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# -------------------- LLM Call Wrapper --------------------
def call_llm(system_prompt: str, user_query: str) -> dict:
    """
    Calls Gemini for routing and returns parsed JSON dict.
    """

    model = genai.GenerativeModel("gemini-2.5-flash")

    try:
        # Combine system and user prompt as a single user message
        prompt = system_prompt.strip() + "\n" + user_query.strip()
        response = model.generate_content(prompt)

        text = response.text.strip()
        
        # Remove markdown code blocks if present
        if text.startswith("```"):
            text = text.split("```")[-2].strip()
        
        # Remove "json" prefix if present (sometimes Gemini adds this)
        if text.lower().startswith("json"):
            text = text[4:].strip()
        
        # Try to extract JSON object if there's extra text
        if not text.startswith("{"):
            # Find the first { and last }
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end > start:
                text = text[start:end]
        
        # parse JSON safely
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            print("⚠️ Gemini returned non-JSON:", text)
            print(f"   Parse error: {e}")
            return {"agent": "none", "user": "unknown", "repo": None}

    except Exception as e:
        print("❌ Gemini error:", e)
        return {"agent": "none", "user": "unknown", "repo": None}


# -------------------- Router Logic --------------------
def route_to_agent(query: str):
    """
    Sends query to Gemini and returns routing decision
    """

    system_prompt = """
You are a strict routing engine for a multi-agent system.

### AGENT ROUTING RULES ###
- If query asks about code/files/implementation inside a specific repository → agent = "github_rag" AND extract repo name
- If query mentions GitHub terms (repo, PR, pull request, stars, commits, branches) → agent = "github"
- If query mentions Linear terms (issue, task, ticket, sprint, project, team) → agent = "linear"
- Otherwise → agent = "none"

### USER IDENTIFICATION RULES ###
- If "Alice" or "alice" in query → user = "alice"
- If "Bob" or "bob" in query → user = "bob"
- If the query is about GitHub/Linear but no user is mentioned → user = "unknown"
- For unrelated queries → user = "unknown"

### REPO EXTRACTION RULES ###
- If query is about code/files inside a repo, extract the repository name in format "owner/repo"
- Examples: "Ishan1819/crewai", "facebook/react", "microsoft/vscode"
- If no specific repo mentioned → repo = null

### OUTPUT ONLY THIS JSON (VERY STRICT) ###
{
  "agent": "github" | "github_rag" | "linear" | "none",
  "user": "alice" | "bob" | "unknown",
  "repo": "owner/repo" | null
}

No explanation. No markdown. Only JSON.
"""

    result = call_llm(system_prompt, query)

    # Force safe keys
    return {
        "agent": result.get("agent", "none"),
        "user": result.get("user", "unknown"),
        "repo": result.get("repo", None)
    }