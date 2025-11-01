# StackGen# StackGen - AI-Powered Multi-Agent Development Assistant# StackGen - Multi-Agent GitHub & Linear Assistant with RAG

**A multi-agent AI system that routes queries to specialized agents for GitHub, Linear, and code analysis.**[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)A sophisticated multi-agent system that routes queries to specialized agents for GitHub, Linear, and code analysis using RAG (Retrieval-Augmented Generation).

StackGen uses LLM-based routing (Google Gemini) to intelligently direct user queries to the right agent. It supports multi-user credentials (Alice → User1, Bob → User2) and includes a RAG pipeline for deep code analysis using ChromaDB. The system has a FastAPI backend and a ChatGPT-style Streamlit UI.[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)

**How it works:**[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)## Features

1. User submits a query via Streamlit UI (port 8501)

2. FastAPI backend (port 8002) receives the query[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

3. LLM Router analyzes the query and determines which agent to use (GitHub/Linear/RAG)

4. The appropriate agent executes using CrewAI tools### 🤖 Multi-Agent System

5. Response is formatted and returned to the user

StackGen is an intelligent multi-agent system that provides seamless access to GitHub repositories, Linear project management, and AI-powered code analysis through a conversational interface. Built with CrewAI, it routes queries to specialized agents and uses RAG (Retrieval-Augmented Generation) for deep code understanding.

---

- **GitHub Agent**: Handles repository listings, PRs, issues, stars, branches, commits

## Setup & Run

## 🌟 Features- **Linear Agent**: Manages tasks, issues, projects, teams, priorities

### Prerequisites

- Python 3.11+- **RAG Agent**: Answers code-related questions by analyzing repository contents

- API Keys: Google Gemini, GitHub Personal Access Token, Linear API Key

### 🤖 Multi-Agent Architecture

### Installation

- **GitHub Agent**: Repository management, PRs, issues, stars, branches, commits### 🧠 Smart Routing

```bash

# Clone repository- **Linear Agent**: Task management, issues, projects, teams, priorities

git clone <repository-url>

cd stackgen- **RAG Agent**: Deep code analysis and understanding using vector embeddings- Uses Gemini LLM to intelligently route queries to the appropriate agent



# Install dependencies- Automatically detects user (Alice/Bob) from query

pip install -r requirements.txt

### 🧠 Intelligent Routing- Extracts repository names for code analysis queries

# Configure environment

cp .env.example .env- LLM-powered query routing using Gemini 2.5 Flash

```

- Automatic user detection (Alice/Bob)### 🔍 RAG-Powered Code Q&A

Edit `.env` with your credentials:

````env- Repository name extraction for code analysis

GEMINI_API_KEY=your_gemini_api_key

GITHUB_TOKEN_USER1=ghp_your_github_token- Smart handling of ambiguous queries- Indexes entire repositories using vector embeddings

LINEAR_API_KEY_USER1=lin_api_your_linear_key

GITHUB_TOKEN_USER2=ghp_optional_second_user- Retrieves relevant code snippets for context

LINEAR_API_KEY_USER2=lin_api_optional_second_user

```### 🔍 RAG-Powered Code Q&A- Provides detailed answers with file references and code examples



### Run- Indexes entire repositories using ChromaDB



```bash- Semantic search with sentence transformers## Architecture

# Terminal 1: Start FastAPI backend

python main.py- Context-aware code analysis



# Terminal 2: Start Streamlit UI- File references and code snippets in responses```

streamlit run streamlit_app.py

```stackgen/



Open http://localhost:8501 in your browser.### 💬 Interactive UI├── agents/



### Docker (Optional)- ChatGPT-style Streamlit interface│ ├── github_agent.py # GitHub operations agent



```bash- Agent thoughts visualization│ └── linear_agent.py # Linear operations agent

docker build -t stackgen .

docker run -d -p 8001:8001 -p 8501:8501 --env-file .env stackgen- Formatted responses with metadata├── tools/

````

- Chat history and conversation context│ ├── github_tools.py # GitHub CrewAI tools

---

│ ├── linear_tools.py # Linear CrewAI tools

## Usage Examples

## 📋 Table of Contents│ └── github_rag.py # RAG-based repo Q&A tool

**GitHub:** `"Alice, show me all open issues in Ishan1819/crewai"`

├── services/

**Linear:** `"Bob, create a new Linear issue with title 'Bug fix'"`

- [Quick Start](#-quick-start)│ ├── github_services.py # GitHub API wrapper

**RAG Code Analysis:** `"Alice, analyze the code in Ishan1819/crewai and explain main.py"`

- [Installation](#-installation)│ └── linear_services.py # Linear API wrapper

---

- [Configuration](#-configuration)├── router_logic/

## Dependencies

- [Usage](#-usage)│ └── llm_router.py # LLM-based routing logic

See `requirements.txt` for full list. Key packages:

- `fastapi` - Web framework- [API Documentation](#-api-documentation)├── routes/

- `streamlit` - UI

- `crewai` - Multi-agent orchestration- [Docker Deployment](#-docker-deployment)│ └── query_router.py # FastAPI query endpoint

- `google-generativeai` - Gemini LLM

- `PyGithub` - GitHub API- [Architecture](#-architecture)├── main.py # FastAPI application entry point

- `chromadb` - Vector database for RAG

- `sentence-transformers` - Embeddings- [Examples](#-examples)├── litellm_wrapper.py # LiteLLM wrapper for CrewAI

---- [Troubleshooting](#-troubleshooting)└── .env # Environment variables

## Assumptions & Limitations- [Contributing](#-contributing)```

**Assumptions:**- [License](#-license)

- Users are named "Alice" or "Bob" (mapped to user1/user2 credentials)

- Queries explicitly mention user name ("Alice, show me...")## Setup

- GitHub repositories use `owner/repo` format

- API keys have appropriate permissions## 🚀 Quick Start

**Limitations:**### 1. Install Dependencies

- Single LLM provider (Google Gemini 2.5 Flash)

- In-memory ChromaDB (resets on restart)### Prerequisites

- No authentication/authorization layer

- Limited to GitHub and Linear platforms- Python 3.11 or higher```bash

- RAG indexing downloads entire repos (slow for large repos)

- No caching for API responses- GitHub Personal Access Token

- Requires both services running simultaneously

- pip install -r requirements.txt

**Known Issues:**

- ChromaDB vectors not persisted between sessions- Linear API Key```

- Streamlit API URL hardcoded to port 8002 (should be 8001)

- No retry logic for failed API calls- Google Gemini API Key

- Large repository analysis can timeout

### 2. Configure Environment Variables

---

### 1. Clone the Repository

For detailed architecture and technical documentation, see `ARCHITECTURE.md`.

```bashCreate a `.env` file with the following:

git clone https://github.com/Ishan1819/crewai.git

cd crewai```env

````# Alice GitHub

GITHUB_USERNAME_USER1=your_username

### 2. Install DependenciesGITHUB_TOKEN_USER1=your_github_token

```bash

pip install -r requirements.txt# Bob GitHub

```GITHUB_USERNAME_USER2=other_username

GITHUB_TOKEN_USER2=other_github_token

### 3. Configure Environment

Create a `.env` file:# Alice Linear

```envLINEAR_EMAIL_USER1=alice@example.com

# Alice (User1)LINEAR_API_KEY_USER1=your_linear_key

GITHUB_USERNAME_USER1=your_username

GITHUB_TOKEN_USER1=ghp_xxxxx# Bob Linear

LINEAR_EMAIL_USER1=alice@example.comLINEAR_EMAIL_USER2=bob@example.com

LINEAR_API_KEY_USER1=lin_api_xxxxxLINEAR_API_KEY_USER2=other_linear_key



# Bob (User2)# Gemini Key

GITHUB_USERNAME_USER2=other_usernameGEMINI_API_KEY=your_gemini_api_key

GITHUB_TOKEN_USER2=ghp_xxxxx```

LINEAR_EMAIL_USER2=bob@example.com

LINEAR_API_KEY_USER2=lin_api_xxxxx### 3. Run the Server



# Gemini```bash

GEMINI_API_KEY=AIzaSyxxxxxpython main.py

````

### 4. Run the ApplicationServer will start at `http://127.0.0.1:8002`

**Terminal 1 - Backend:**## Usage

```bash

python main.py### API Endpoint

```

**POST** `/api/query`

**Terminal 2 - Frontend:**

```````bash**Request:**

streamlit run streamlit_app.py

``````json

{

Visit `http://localhost:8501` to access the UI.  "query": "What does the main.py file do in Ishan1819/crewai for alice?"

}

## 💻 Installation```



### Using pip**Response:**

```bash

# Create virtual environment```json

python -m venv venv{

  "agent": "github_rag",

# Activate virtual environment  "user": "alice",

# Windows  "repo": "Ishan1819/crewai",

venv\Scripts\activate  "result": "📚 Answer for repo 'Ishan1819/crewai':\n[Detailed answer with code snippets]"

# Linux/Mac}

source venv/bin/activate```



# Install dependencies### Example Queries

pip install -r requirements.txt

```#### GitHub Queries



### Using conda```

```bash- "Show alice's repositories"

# Create conda environment- "List bob's pull requests"

conda create -n stackgen python=3.11- "What are alice's starred repos?"

- "Show branches in repo xyz for bob"

# Activate environment```

conda activate stackgen

#### Linear Queries

# Install dependencies

pip install -r requirements.txt```

```- "List alice's issues"

- "Show bob's high priority tasks"

## ⚙️ Configuration- "What teams is alice part of?"

- "Show in-progress issues for bob"

### Environment Variables```



| Variable | Description | Example |#### RAG Code Queries

|----------|-------------|---------|

| `GITHUB_USERNAME_USER1` | Alice's GitHub username | `alice_dev` |```

| `GITHUB_TOKEN_USER1` | Alice's GitHub PAT | `ghp_xxxxx` |- "What does the main.py file do in Ishan1819/crewai for alice?"

| `LINEAR_EMAIL_USER1` | Alice's Linear email | `alice@company.com` |- "Explain the authentication logic in alice's repo owner/repo"

| `LINEAR_API_KEY_USER1` | Alice's Linear API key | `lin_api_xxxxx` |- "How does the router work in bob's Ishan1819/crewai repository?"

| `GEMINI_API_KEY` | Google Gemini API key | `AIzaSyxxxxx` |- "Show me the GitHub agent implementation in alice's crewai repo"

```````

### User Mapping

- **Alice** → `USER1` credentials
- **Bob** → `USER2` credentials

The system uses Gemini LLM to analyze queries and route them:

## 📖 Usage

1. **github_rag**: Questions about code/files in a specific repository

### GitHub Queries2. **github**: General GitHub operations (repos, PRs, issues, etc.)

````3. **linear**: Linear project management (tasks, issues, teams)

✅ "List Alice's repositories"4. **none**: Unrecognized queries

✅ "Show Bob's pull requests"

✅ "What are Alice's starred repos?"## User Mapping

✅ "List branches in repo xyz for Bob"

✅ "Show commits in repo abc for Alice"- `alice` → `USER1` environment variables

```- `bob` → `USER2` environment variables



### Linear Queries## Testing

````

✅ "List Alice's issues"Run the test script to verify the integration:

✅ "Show Bob's high priority tasks"

✅ "What are Alice's in-progress tasks?"```bash

✅ "Which teams is Bob part of?"python test_rag.py

✅ "Show Alice's projects"```

````

## RAG System Details

### RAG Code Analysis

```### Supported File Types

✅ "What does main.py do in Ishan1819/crewai for Alice?"

✅ "Explain the router logic in Bob's facebook/react repo"Python, JavaScript, TypeScript, Java, C++, C, C#, Ruby, Go, Rust, PHP, HTML, CSS, JSON, XML, YAML, Markdown, Shell scripts, SQL, and more.

✅ "How is authentication implemented in Alice's repo owner/name?"

✅ "Show me the API endpoints in Bob's fastapi/fastapi repo"### Vector Database

````

- **ChromaDB**: In-memory vector storage

### Edge Cases- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)

```- **Chunk Size**: 1000 characters with 200 character overlap

⚠️ "List all repositories" → "Please specify which user (Alice or Bob)"

⚠️ "What's the weather today?" → "I cannot answer this question."### Process Flow

```

1. Extract repository contents via GitHub API

## 📚 API Documentation2. Filter text-based files (ignoring binaries)

3. Chunk large files for better context

### POST `/api/query`4. Generate embeddings using sentence-transformers

5. Store in ChromaDB with metadata

**Request:**6. Query with semantic search

````json7. Retrieve top-k relevant chunks

{8. Send context + question to Gemini

  "query": "List Alice's repositories"9. Return detailed answer

}

```## Dependencies



**Response:**- **FastAPI**: Web framework

```json- **CrewAI**: Multi-agent orchestration

{- **PyGithub**: GitHub API client

  "agent": "github",- **google-generativeai**: Gemini LLM

  "user": "alice",- **chromadb**: Vector database

  "repo": null,- **sentence-transformers**: Text embeddings

  "result": "📂 Repositories for alice:\nrepo1\nrepo2\n..."- **litellm**: LLM wrapper for CrewAI

}

```## API Documentation



### Interactive API DocsOnce the server is running, visit:

- **Swagger UI**: http://127.0.0.1:8001/docs

- **ReDoc**: http://127.0.0.1:8001/redoc- **Swagger UI**: http://127.0.0.1:8001/docs

- **ReDoc**: http://127.0.0.1:8001/redoc

## 🐳 Docker Deployment

## Notes

### Build Image

```bash- First query to a repository will be slower due to indexing

docker build -t stackgen:latest .- Subsequent queries to the same repo are faster (embeddings cached)

```- Maximum file size: 500KB per file

- The system respects GitHub rate limits

### Run Container- Make sure to use valid API tokens

```bash

docker run -d \## Error Handling

  --name stackgen \

  -p 8001:8001 \The system handles:

  -p 8501:8501 \

  --env-file .env \- Missing API tokens

  stackgen:latest- Invalid repository names

```- API rate limits

- Network errors

### Access Application- Malformed queries

- **Streamlit UI**: http://localhost:8501

- **FastAPI Backend**: http://localhost:8001## Security

- **API Docs**: http://localhost:8001/docs

⚠️ **Important**: Never commit your `.env` file to version control!

### Docker Compose

```yamlAdd `.env` to `.gitignore`:

version: '3.8'

````

services:.env

stackgen:**pycache**/

    build: .*.pyc

    ports:```

      - "8001:8001"

      - "8501:8501"## License

    env_file:

      - .env[Your License Here]

    restart: unless-stopped

````## Contributing



Run with:[Your Contributing Guidelines Here]

```bash
docker-compose up -d
````

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                    │
│                  (streamlit_app.py)                      │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP POST /api/query
                     ↓
┌─────────────────────────────────────────────────────────┐
│                   FastAPI Backend                        │
│                     (main.py)                            │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│                 LLM Router (Gemini)                      │
│              (router_logic/llm_router.py)                │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Analyzes query → Returns:                        │   │
│  │ - agent: github | github_rag | linear | none     │   │
│  │ - user: alice | bob | unknown                    │   │
│  │ - repo: owner/repo | null                        │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
┌──────────────┐ ┌──────────┐ ┌──────────┐
│ GitHub Agent │ │RAG Agent │ │Linear Ag.│
│ (CrewAI)     │ │(ChromaDB)│ │(CrewAI)  │
└──────┬───────┘ └────┬─────┘ └────┬─────┘
       │              │            │
       ↓              ↓            ↓
┌──────────────┐ ┌──────────┐ ┌──────────┐
│ GitHub API   │ │ Gemini + │ │Linear API│
│              │ │Vector DB │ │          │
└──────────────┘ └──────────┘ └──────────┘
```

For detailed architecture, see [ARCHITECTURE.md](ARCHITECTURE.md)

## 💡 Examples

### Example 1: GitHub Repository Listing

**Query:** "List Alice's repositories"

**Agent Thoughts:**

```
Routing query to github agent...
Detected user: alice
No repository specified
Processing request...
Generating response...
```

**Response:**

```
📂 Repositories for alice:
alice/project1
alice/project2
alice/awesome-lib
```

### Example 2: RAG Code Analysis

**Query:** "What does main.py do in Ishan1819/crewai for Alice?"

**Agent Thoughts:**

```
Routing query to github_rag agent...
Detected user: alice
Repository: Ishan1819/crewai
Extracting repository contents...
Indexing 45 files...
Processing request...
Generating response...
```

**Response:**

```
📚 Answer for repo 'Ishan1819/crewai':
The main.py file is the entry point for the FastAPI application. It:

1. Initializes the FastAPI app with CORS middleware
2. Includes the query router under /api prefix
3. Starts the Uvicorn server on port 8001

Key code from main.py:
- Line 15-20: CORS configuration
- Line 25: Router inclusion
- Line 30: Server startup

The file serves as the backend API server...
```

### Example 3: Linear Task Management

**Query:** "Show Bob's high priority tasks"

**Response:**

```
📝 Issues for bob:
Fix authentication bug - Priority 8 - In Progress
Implement new API endpoint - Priority 9 - Todo
Database migration - Priority 7 - In Review
```

## 🔧 Troubleshooting

### "Cannot connect to the API server"

**Solution:** Ensure FastAPI backend is running:

```bash
python main.py
```

### "Missing GitHub token for user X"

**Solution:** Check your `.env` file has the correct variables:

```env
GITHUB_TOKEN_USER1=ghp_xxxxx
```

### "Please specify which user"

**Solution:** Always mention "Alice" or "Bob" in your query:

```
❌ "List repositories"
✅ "List Alice's repositories"
```

### Slow RAG responses

**Solution:**

- First query to a repo takes 10-60 seconds (indexing)
- Subsequent queries are faster (cached)
- Large repos may timeout - increase timeout if needed

### Gemini API errors

**Solution:**

- Verify your `GEMINI_API_KEY` is valid
- Check rate limits on your Gemini API account
- Ensure you have credits/quota available

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linter
flake8

# Format code
black .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) for multi-agent orchestration
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [Streamlit](https://streamlit.io/) for the interactive UI
- [Google Gemini](https://ai.google.dev/) for LLM capabilities
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [PyGithub](https://github.com/PyGithub/PyGithub) for GitHub API integration

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Ishan1819/crewai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Ishan1819/crewai/discussions)
- **Email**: support@stackgen.dev

## 🗺️ Roadmap

- [ ] Support for more users (beyond Alice and Bob)
- [ ] GitLab and Bitbucket integration
- [ ] Jira integration
- [ ] Slack/Discord bot interface
- [ ] Advanced RAG with multi-repo analysis
- [ ] Code generation capabilities
- [ ] PR review automation
- [ ] Custom agent creation

---

**Made with ❤️ by the StackGen Team**
