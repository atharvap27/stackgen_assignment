# StackGen Architecture - In-Depth Documentation

## Table of Contents

1. [System Overview](#system-overview)
2. [High-Level Architecture](#high-level-architecture)
3. [Component Deep Dive](#component-deep-dive)
4. [Data Flow](#data-flow)
5. [Agent System](#agent-system)
6. [RAG Pipeline](#rag-pipeline)
7. [API Layer](#api-layer)
8. [Security](#security)
9. [Performance Optimization](#performance-optimization)
10. [Deployment Architecture](#deployment-architecture)

---

## System Overview

StackGen is a microservices-based multi-agent system designed to provide intelligent access to developer tools (GitHub, Linear) and code understanding (RAG). The system uses LLM-powered routing to direct queries to specialized agents that handle specific domains.

### Key Design Principles

1. **Separation of Concerns**: Each agent handles a specific domain
2. **Intelligent Routing**: LLM-based query understanding and routing
3. **Scalability**: Microservices architecture allows independent scaling
4. **Extensibility**: Easy to add new agents and tools
5. **User Experience**: Chat-like interface with transparent agent reasoning

---

## High-Level Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                         User Interface                          │
│                      (Streamlit Frontend)                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Chat Input Box                                         │  │
│  │  • Message History                                        │  │
│  │  • Agent Thoughts Display                                 │  │
│  │  • Formatted Response                                     │  │
│  │  • Metadata (Agent, User, Repo)                          │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬────────────────────────────────────┘
                            │
                     HTTP POST /api/query
                            │
┌───────────────────────────▼────────────────────────────────────┐
│                      API Gateway                                │
│                     (FastAPI Backend)                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Request Validation                                     │  │
│  │  • CORS Handling                                          │  │
│  │  • Session Management                                     │  │
│  │  • Error Handling                                         │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬────────────────────────────────────┘
                            │
                            ↓
┌────────────────────────────────────────────────────────────────┐
│                      Router Layer                               │
│                   (LLM-Based Intelligence)                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Gemini 2.5 Flash LLM                                     │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  System Prompt:                                     │  │  │
│  │  │  • Agent routing rules                              │  │  │
│  │  │  • User identification rules                        │  │  │
│  │  │  • Repository extraction rules                      │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │                                                            │  │
│  │  Output: {agent, user, repo}                             │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ↓               ↓               ↓
┌───────────────────┐ ┌────────────┐ ┌────────────────┐
│   GitHub Agent    │ │ RAG Agent  │ │  Linear Agent  │
│    (CrewAI)       │ │ (Custom)   │ │   (CrewAI)     │
├───────────────────┤ ├────────────┤ ├────────────────┤
│ Tools:            │ │ Pipeline:  │ │ Tools:         │
│ • list_repos      │ │ • Extract  │ │ • list_issues  │
│ • list_prs        │ │ • Chunk    │ │ • in_progress  │
│ • list_issues     │ │ • Embed    │ │ • high_priority│
│ • list_starred    │ │ • Store    │ │ • teams        │
│ • list_branches   │ │ • Query    │ │ • projects     │
│ • list_commits    │ │ • Generate │ │ • create_issue │
│ • search_repos    │ │            │ │                │
└────────┬──────────┘ └─────┬──────┘ └────────┬───────┘
         │                  │                  │
         ↓                  ↓                  ↓
┌────────────────┐  ┌───────────────┐  ┌─────────────┐
│  GitHub API    │  │  ChromaDB     │  │  Linear API │
│  (REST)        │  │  (Vector DB)  │  │  (GraphQL)  │
│                │  │  +            │  │             │
│  PyGithub      │  │  Gemini Pro   │  │  requests   │
│  Wrapper       │  │  Latest       │  │  library    │
└────────────────┘  └───────────────┘  └─────────────┘
```

---

## Component Deep Dive

### 1. Frontend Layer (Streamlit)

**File**: `streamlit_app.py`

**Responsibilities**:

- User interface rendering
- Chat message management
- API communication
- Response formatting
- Session state management

**Key Components**:

```python
# Session State Management
st.session_state.messages = [
    {
        "role": "user",
        "content": "query text"
    },
    {
        "role": "assistant",
        "content": "response",
        "thoughts": "agent reasoning",
        "metadata": {
            "agent": "github",
            "user": "alice",
            "repo": null
        }
    }
]

# Response Formatting
def format_result(result):
    # Extract raw text from CrewAI response
    # Escape HTML
    # Format newlines
    return formatted_text
```

**Styling**:

- Custom CSS for ChatGPT-like appearance
- Light grey, small font for agent thoughts
- Large, clear font for final responses
- Metadata badges for agent/user/repo info

### 2. API Gateway (FastAPI)

**File**: `main.py`

**Responsibilities**:

- HTTP request/response handling
- CORS configuration
- Middleware management
- Route registration
- Error handling

**Configuration**:

```python
app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session Middleware
app.add_middleware(
    SessionMiddleware,
    secret_key="supersecret-key"
)

# Router Registration
app.include_router(router, prefix="/api")
```

**Endpoints**:

- `POST /api/query`: Main query endpoint
- `GET /docs`: Swagger UI documentation
- `GET /redoc`: ReDoc documentation

### 3. Query Router

**File**: `routes/query_router.py`

**Responsibilities**:

- Request validation
- LLM router invocation
- User mapping (alice → user1, bob → user2)
- Agent dispatch
- Response formatting
- Error handling for edge cases

**Flow**:

```python
async def handle_query(request: QueryRequest):
    # 1. Get routing decision from LLM
    routing = route_to_agent(request.query)

    # 2. Validate routing
    if routing["agent"] == "none":
        return "I cannot answer this question."

    if routing["user"] == "unknown":
        return "Please specify which user..."

    # 3. Map user to credentials
    user_key = USER_MAP.get(routing["user"])

    # 4. Dispatch to agent
    if routing["agent"] == "github":
        result = run_github_agent(query, user_key)
    elif routing["agent"] == "github_rag":
        result = github_repo_qa_direct(user_key, repo, query)
    elif routing["agent"] == "linear":
        result = run_linear_agent(query, user_key)

    # 5. Extract and format result
    if isinstance(result, dict) and 'raw' in result:
        result = result['raw']

    return result
```

### 4. LLM Router

**File**: `router_logic/llm_router.py`

**Responsibilities**:

- Query analysis using Gemini LLM
- Agent selection
- User identification
- Repository name extraction
- JSON parsing and error handling

**System Prompt**:

```
You are a strict routing engine for a multi-agent system.

AGENT ROUTING RULES:
- Code/files in repo → github_rag + extract repo
- GitHub terms (repo, PR, stars) → github
- Linear terms (issue, task, team) → linear
- Otherwise → none

USER IDENTIFICATION:
- "Alice"/"alice" → user = "alice"
- "Bob"/"bob" → user = "bob"
- Otherwise → user = "unknown"

REPO EXTRACTION:
- Format: "owner/repo"
- Examples: "facebook/react", "Ishan1819/crewai"

OUTPUT: JSON only
{
  "agent": "github|github_rag|linear|none",
  "user": "alice|bob|unknown",
  "repo": "owner/repo|null"
}
```

**JSON Parsing**:

````python
def call_llm(system_prompt, user_query):
    response = model.generate_content(prompt)
    text = response.text.strip()

    # Handle markdown code blocks
    if text.startswith("```"):
        text = text.split("```")[-2].strip()

    # Handle "json" prefix
    if text.lower().startswith("json"):
        text = text[4:].strip()

    # Extract JSON object
    if not text.startswith("{"):
        start = text.find("{")
        end = text.rfind("}") + 1
        text = text[start:end]

    return json.loads(text)
````

---

## Agent System

### GitHub Agent (CrewAI)

**File**: `agents/github_agent.py`

**Architecture**:

```python
github_ai = Agent(
    role="GitHub Assistant",
    goal="Fetch GitHub data based on user query",
    backstory="Expert in GitHub API...",
    tools=[
        github_list_repos,
        github_list_prs,
        github_list_issues,
        github_list_starred,
        github_list_branches,
        github_list_commits,
        github_search_repos
    ],
    llm=gemini_llm,
    verbose=False
)

github_task = Task(
    description=f"User query: {query}, User key: {user_key}",
    agent=github_ai,
    expected_output="GitHub result, one line per item"
)

crew = Crew(
    agents=[github_ai],
    tasks=[github_task],
    process="sequential"
)

return crew.kickoff()
```

**Tools** (`tools/github_tools.py`):

Each tool is decorated with `@tool` for CrewAI integration:

```python
@tool("github_list_repos")
def github_list_repos(user: str) -> str:
    """Lists all GitHub repositories for the given user."""
    gh = GitHubService(user.lower())
    repos = gh.list_repos()
    return f"📂 Repositories for {user}:\n" + "\n".join(repos)
```

**Service Layer** (`services/github_services.py`):

```python
class GitHubService:
    def __init__(self, user_id: str):
        token = os.getenv(f"GITHUB_TOKEN_{user_id.upper()}")
        self.client = Github(token)
        self.username = os.getenv(f"GITHUB_USERNAME_{user_id.upper()}")

    def list_repos(self):
        user = self.client.get_user(self.username)
        return [repo.name for repo in user.get_repos()]
```

### Linear Agent (CrewAI)

**File**: `agents/linear_agent.py`

**Architecture**: Similar to GitHub agent

**Service Layer** (`services/linear_services.py`):

```python
class LinearService:
    BASE_URL = "https://api.linear.app/graphql"

    def __init__(self, user_id: str):
        self.api_key = os.getenv(f"LINEAR_API_KEY_{user_id.upper()}")

    def query(self, query_string):
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
        data = {"query": query_string}
        r = requests.post(self.BASE_URL, json=data, headers=headers)
        return r.json()

    def list_issues(self):
        query = """
        query {
          issues(filter: {
            assignee: { displayName: { eq: "..." } }
          }) {
            nodes { id title state { name } priority }
          }
        }
        """
        return self.query(query)
```

---

## RAG Pipeline

**File**: `tools/github_rag.py`

### Architecture

```
┌─────────────────────────────────────────────────────┐
│            RAG Pipeline Components                   │
├─────────────────────────────────────────────────────┤
│                                                      │
│  1. Repository Extraction (GitHub API)              │
│     ├── Get all files from repo                     │
│     ├── Filter by file type (py, js, md, etc.)      │
│     └── Decode base64 content                       │
│                                                      │
│  2. Chunking Strategy                               │
│     ├── Chunk size: 1000 characters                 │
│     ├── Overlap: 200 characters                     │
│     ├── Smart splitting at newlines                 │
│     └── Add file path header to each chunk          │
│                                                      │
│  3. Embedding Generation                            │
│     ├── Model: sentence-transformers/all-MiniLM-L6-v2│
│     ├── Dimension: 384                              │
│     └── Batch processing with progress bar          │
│                                                      │
│  4. Vector Storage (ChromaDB)                       │
│     ├── Collection: "repo"                          │
│     ├── Distance: Cosine similarity                 │
│     └── Metadata: {file_path, chunk_index}          │
│                                                      │
│  5. Query Processing                                │
│     ├── Embed query with same model                 │
│     ├── Retrieve top-k chunks (k=5)                 │
│     └── Rank by relevance                           │
│                                                      │
│  6. Answer Generation (Gemini)                      │
│     ├── Context: Retrieved code chunks              │
│     ├── Question: User query                        │
│     └── Response: Code analysis with references     │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Implementation Details

**1. Repository Extraction**:

```python
def extract_repo(self, repo_name: str):
    repo = self.github.get_repo(repo_name)
    docs, metas, ids = [], [], []
    contents = repo.get_contents("")

    text_exts = {'py','js','ts','java','cpp','md',...}

    while contents:
        fc = contents.pop(0)
        if fc.type == "dir":
            contents.extend(repo.get_contents(fc.path))
        elif fc.size < 500000 and is_text_file(fc):
            content = base64.b64decode(fc.content).decode('utf-8')
            chunks = self._chunk(content, fc.path)

            for i, chunk in enumerate(chunks):
                docs.append(chunk)
                metas.append({'file_path': fc.path, 'chunk': i})
                ids.append(f"f{file_id}_c{i}")
```

**2. Chunking Strategy**:

```python
def _chunk(self, text, path, size=1000, overlap=200):
    header = f"File: {path}\n\n"
    if len(text) <= size:
        return [header + text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        if end < len(text):
            # Find nearest newline
            nl = text.rfind('\n', start, end)
            if nl > start + size // 2:
                end = nl
        chunks.append(header + text[start:end])
        start = end - overlap if end < len(text) else end
    return chunks
```

**3. Embedding & Storage**:

```python
embeddings = self.embedder.encode(docs, show_progress_bar=True).tolist()
self.collection.add(
    documents=docs,
    embeddings=embeddings,
    metadatas=metas,
    ids=ids
)
```

**4. Query & Answer**:

```python
def ask(self, question, n=5):
    # Embed query
    qemb = self.embedder.encode([question])[0].tolist()

    # Retrieve chunks
    results = self.collection.query(
        query_embeddings=[qemb],
        n_results=n
    )

    # Build context
    context = "\n".join([
        f"--- {m['file_path']} ---\n{d}\n"
        for d, m in zip(results['documents'][0], results['metadatas'][0])
    ])

    # Generate answer
    prompt = f"""
    Analyze GitHub repo: {self.repo_name}

    Context:
    {context}

    Question: {question}

    Provide concise answer with file references and code snippets.
    """

    return self.model.generate_content(prompt).text
```

### Performance Characteristics

| Metric                  | Value            | Notes            |
| ----------------------- | ---------------- | ---------------- |
| Embedding Speed         | ~1000 chunks/sec | CPU-dependent    |
| Index Time (small repo) | 10-30 sec        | < 100 files      |
| Index Time (large repo) | 30-120 sec       | 100-1000 files   |
| Query Latency           | 2-5 sec          | After indexing   |
| Memory Usage            | ~200MB           | Per indexed repo |
| Max File Size           | 500KB            | Configurable     |

---

## Data Flow

### Complete Request Flow

```
1. User Input (Streamlit)
   └─> "List Alice's repositories"

2. HTTP POST to Backend
   └─> POST /api/query
       Body: {"query": "List Alice's repositories"}

3. Request Validation
   └─> QueryRequest model validates input

4. LLM Router
   ├─> System prompt + user query
   ├─> Gemini analyzes query
   └─> Returns: {
         "agent": "github",
         "user": "alice",
         "repo": null
       }

5. Validation Checks
   ├─> agent == "none"? → "I cannot answer this question."
   └─> user == "unknown"? → "Please specify which user..."

6. User Mapping
   └─> "alice" → "user1"

7. Agent Dispatch
   └─> run_github_agent(query, "user1")
       ├─> Creates CrewAI Agent with GitHub tools
       ├─> Agent selects appropriate tool (github_list_repos)
       ├─> Tool calls GitHubService("user1")
       ├─> GitHubService gets repos from GitHub API
       └─> Returns formatted result

8. Response Formatting
   ├─> Extract 'raw' field from CrewAI response
   └─> Return clean text

9. HTTP Response
   └─> {
         "agent": "github",
         "user": "alice",
         "repo": null,
         "result": "📂 Repositories for alice:\nrepo1\nrepo2..."
       }

10. Streamlit Display
    ├─> Show agent thoughts (light grey)
    ├─> Show final response (large, clear)
    └─> Show metadata (agent/user/repo)
```

---

## Security

### Authentication & Authorization

**Environment Variables**:

- Stored in `.env` file (gitignored)
- Loaded at runtime via `python-dotenv`
- Never exposed to frontend

**User Isolation**:

```python
USER_MAP = {
    "alice": "user1",
    "bob": "user2"
}

# Each user has separate credentials
GITHUB_TOKEN_USER1=...
GITHUB_TOKEN_USER2=...
```

**API Security**:

- GitHub Personal Access Tokens with scoped permissions
- Linear API keys with team access control
- Gemini API key with rate limiting

### Data Privacy

**No Data Storage**:

- ChromaDB is in-memory (cleared on restart)
- No logging of user queries or responses
- No persistent session storage

**CORS Configuration**:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Best Practices

1. **.env Security**:

   - Never commit `.env` file
   - Use `.env.example` for template
   - Rotate tokens regularly

2. **Docker Secrets**:

   - Use Docker secrets for production
   - Mount secrets as files, not environment variables

3. **Network Security**:
   - Use HTTPS in production
   - Implement rate limiting
   - Add authentication middleware

---

## Performance Optimization

### Caching Strategy

**1. RAG Cache** (In-Memory):

```python
# ChromaDB collection persists until server restart
# Subsequent queries to same repo are faster
```

**2. GitHub API Cache**:

```python
# Consider adding Redis cache for GitHub responses
# Cache key: f"{user}:{endpoint}:{params}"
# TTL: 5 minutes
```

**3. LLM Response Cache**:

```python
# Cache routing decisions for identical queries
# Cache key: hash(query)
# TTL: 1 hour
```

### Concurrent Processing

**Asyncio for API Calls**:

```python
# FastAPI natively supports async
async def handle_query(request: QueryRequest):
    # Async HTTP calls to GitHub/Linear
    # Parallel embedding generation
    # Non-blocking LLM calls
```

### Resource Limits

**Memory Management**:

```python
# Limit ChromaDB collection size
MAX_CHUNKS_PER_REPO = 10000

# Limit concurrent requests
MAX_WORKERS = 10

# Limit file size for RAG
MAX_FILE_SIZE = 500_000  # 500KB
```

---

## Deployment Architecture

### Docker Deployment

**Multi-Stage Build**:

```dockerfile
# Stage 1: Dependencies
FROM python:3.11-slim AS builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Application
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app
CMD ["bash", "start.sh"]
```

**Docker Compose**:

```yaml
version: "3.8"
services:
  stackgen:
    build: .
    ports:
      - "8001:8001" # FastAPI
      - "8501:8501" # Streamlit
    env_file: .env
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/docs"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Kubernetes Deployment

**Deployment YAML**:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: stackgen
spec:
  replicas: 3
  selector:
    matchLabels:
      app: stackgen
  template:
    metadata:
      labels:
        app: stackgen
    spec:
      containers:
        - name: stackgen
          image: stackgen:latest
          ports:
            - containerPort: 8001
            - containerPort: 8501
          envFrom:
            - secretRef:
                name: stackgen-secrets
          resources:
            limits:
              memory: "2Gi"
              cpu: "1000m"
            requests:
              memory: "1Gi"
              cpu: "500m"
```

### Monitoring & Observability

**Logging**:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

**Metrics** (Prometheus):

```python
from prometheus_client import Counter, Histogram

query_counter = Counter('queries_total', 'Total queries', ['agent'])
query_duration = Histogram('query_duration_seconds', 'Query duration')

@query_duration.time()
def handle_query(request):
    result = process_query(request)
    query_counter.labels(agent=result['agent']).inc()
    return result
```

**Health Checks**:

```python
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "github": check_github_connection(),
            "linear": check_linear_connection(),
            "gemini": check_gemini_connection()
        }
    }
```

---

## Future Enhancements

### Planned Features

1. **Multi-User Support**:

   - Dynamic user registration
   - User authentication (JWT)
   - Per-user rate limiting

2. **Advanced RAG**:

   - Multi-repo analysis
   - Cross-repo code search
   - Code diff analysis
   - Pull request review

3. **Agent Extensions**:

   - Jira agent
   - Slack agent
   - GitLab agent
   - Custom agent framework

4. **Performance**:

   - Redis caching layer
   - Background job queue (Celery)
   - Async agent execution
   - Response streaming

5. **Observability**:
   - Distributed tracing (Jaeger)
   - Application metrics (Prometheus)
   - Log aggregation (ELK stack)
   - Error tracking (Sentry)

---

**Document Version**: 1.0  
**Last Updated**: November 1, 2025  
**Maintained By**: StackGen Team
