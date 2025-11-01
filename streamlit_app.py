import streamlit as st
import requests
import json
from typing import Optional
import html

def format_result(result):
    """Format the result for better display"""
    # If result is a dict, extract the 'raw' field
    if isinstance(result, dict):
        if 'raw' in result:
            result = result['raw']
        else:
            result = str(result)
    
    # Convert to string if needed
    result = str(result)
    
    # Escape HTML to prevent rendering issues
    result = html.escape(result)
    
    # Replace newlines with <br> for HTML rendering
    result = result.replace('\n', '<br>')
    
    return result

# Configure Streamlit page
st.set_page_config(
    page_title="StackGen AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# API endpoint
API_URL = "http://127.0.0.1:8002/api/query"

# Custom CSS for styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    
    .thoughts-container {
        background-color: #f8f9fa;
        border-left: 3px solid #d0d0d0;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    
    .thoughts-title {
        font-size: 0.9rem;
        color: #888;
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .thoughts-content {
        font-size: 0.85rem;
        color: #999;
        line-height: 1.6;
        font-family: monospace;
    }
    
    .final-response {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .response-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 1rem;
    }
    
    .response-content {
        font-size: 1.05rem;
        color: #222;
        line-height: 1.8;
        white-space: pre-wrap;
    }
    
    .metadata {
        font-size: 0.85rem;
        color: #666;
        margin-top: 0.5rem;
        padding: 0.5rem;
        background-color: #f5f5f5;
        border-radius: 4px;
    }
    
    .error-message {
        background-color: #fee;
        border-left: 3px solid #f44;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
        color: #c00;
    }
    
    .info-message {
        background-color: #e8f4f8;
        border-left: 3px solid #1f77b4;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
        color: #0066cc;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div class="main-title">🤖 StackGen AI Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask questions about GitHub repositories, Linear tasks, or explore code with AI</div>', unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar with examples
with st.sidebar:
    st.header("📚 Example Queries")
    
    st.subheader("GitHub Questions")
    st.code("List Alice's repositories", language="text")
    st.code("Show Bob's pull requests", language="text")
    st.code("What are Alice's starred repos?", language="text")
    
    st.subheader("Linear Questions")
    st.code("List Alice's issues", language="text")
    st.code("Show Bob's high priority tasks", language="text")
    st.code("What teams is Alice part of?", language="text")
    
    st.subheader("RAG Code Questions")
    st.code("What does main.py do in Ishan1819/crewai for Alice?", language="text")
    st.code("Explain the router logic in Alice's Ishan1819/crewai repo", language="text")
    
    st.divider()
    st.caption("💡 Tip: Always specify the user (Alice or Bob) in your query")

# Main chat interface
query = st.chat_input("Ask a question about GitHub, Linear, or code...")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        if message["role"] == "assistant" and "metadata" in message:
            # Display thoughts if available
            if message.get("thoughts"):
                st.markdown(f"""
                <div class="thoughts-container">
                    <div class="thoughts-title">💭 Agent Thoughts</div>
                    <div class="thoughts-content">{message["thoughts"]}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Display metadata
            metadata = message["metadata"]
            st.markdown(f"""
            <div class="metadata">
                <strong>Agent:</strong> {metadata.get('agent', 'N/A')} | 
                <strong>User:</strong> {metadata.get('user', 'N/A')}
                {f" | <strong>Repo:</strong> {metadata['repo']}" if metadata.get('repo') else ""}
            </div>
            """, unsafe_allow_html=True)

# Process new query
if query:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": query})
    
    with st.chat_message("user"):
        st.markdown(query)
    
    # Show assistant response with streaming effect
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                # Make API request
                response = requests.post(
                    API_URL,
                    json={"query": query},
                    timeout=120
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    agent = data.get("agent", "unknown")
                    user = data.get("user", "unknown")
                    repo = data.get("repo")
                    result = data.get("result", "No response")
                    
                    # Format the result properly
                    formatted_result = format_result(result)
                    
                    # Simulate thoughts/logs (in a real scenario, you'd capture actual logs)
                    thoughts = f"""
Routing query to {agent} agent...
Detected user: {user}
{f"Repository: {repo}" if repo else "No repository specified"}
Processing request...
Generating response...
                    """.strip()
                    
                    # Display thoughts
                    st.markdown(f"""
                    <div class="thoughts-container">
                        <div class="thoughts-title">💭 Agent Thoughts</div>
                        <div class="thoughts-content">{thoughts}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display final response
                    st.markdown(f"""
                    <div class="final-response">
                        <div class="response-title">📝 Final Response</div>
                        <div class="response-content">{formatted_result}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display metadata
                    st.markdown(f"""
                    <div class="metadata">
                        <strong>Agent:</strong> {agent} | 
                        <strong>User:</strong> {user}
                        {f" | <strong>Repo:</strong> {repo}" if repo else ""}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Save to session state
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result,
                        "thoughts": thoughts,
                        "metadata": {
                            "agent": agent,
                            "user": user,
                            "repo": repo
                        }
                    })
                    
                else:
                    error_msg = f"Error {response.status_code}: {response.text}"
                    st.markdown(f'<div class="error-message">❌ {error_msg}</div>', unsafe_allow_html=True)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
                    
            except requests.exceptions.ConnectionError:
                error_msg = "Cannot connect to the API server. Please make sure the FastAPI server is running on http://127.0.0.1:8001"
                st.markdown(f'<div class="error-message">❌ {error_msg}</div>', unsafe_allow_html=True)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
                
            except Exception as e:
                error_msg = f"An error occurred: {str(e)}"
                st.markdown(f'<div class="error-message">❌ {error_msg}</div>', unsafe_allow_html=True)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🔧 **Backend:** FastAPI + CrewAI")
with col2:
    st.caption("🤖 **LLM:** Gemini 2.5 Flash")
with col3:
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
