import streamlit as st
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.mem0 import Mem0Tools
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")


# Configuration for Gemini embedding and LLM
config = {
    "embedder": {
        "provider": "gemini",
        "config": {
            "model": "models/text-embedding-004",
        }
    },
    "llm": {
        "provider": "gemini",
        "config": {
            "model": "gemini-flash-latest",
            "temperature": 0.3,
            "max_tokens": 1000,
        }
    },
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "test",
            "path": "db",
        }
    }
}


@st.cache_resource
def create_agent():
    """Create and cache the agent to avoid reinitializing on each interaction"""
    agent = Agent(
        model=Gemini(id="gemini-flash-latest", api_key=api_key),
        tools=[Mem0Tools(user_id="finance_dept_001", config=config)],
        instructions=[
            "You are a practical corporate finance assistant for a mid-sized technology company",
            "Update the memory as per the instruction of user",
            "Use all available tools that are required to get the job done",
            "Use your memory to recall information as per the query of user",
        ]
    )
    return agent


def main():
    st.set_page_config(page_title="Corporate Finance Assistant", layout="wide")
    st.title("💼 Corporate Finance Assistant")
    st.markdown("An AI-powered assistant with memory for corporate finance queries and budget management.")
    
    # Initialize agent
    agent = create_agent()
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    user_input = st.chat_input("Ask your finance assistant...")
    
    if user_input:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = agent.run(user_input)
                    st.markdown(response.content)
                    st.session_state.messages.append({"role": "assistant", "content": response.content})
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    # Sidebar with utility options
    with st.sidebar:
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()


if __name__ == "__main__":
    main()
