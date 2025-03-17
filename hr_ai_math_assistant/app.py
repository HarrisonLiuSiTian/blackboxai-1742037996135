import streamlit as st
import asyncio
from dotenv import load_dotenv
import os
from agent_handler import AssistantAgent
from config import AppConfig, EnvConfig
import openai

# Load environment variables
load_dotenv()

# Configure OpenAI API
openai.api_key = EnvConfig.OPENAI_API_KEY

def initialize_session_state():
    """Initialize session state variables."""
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'current_domain' not in st.session_state:
        st.session_state.current_domain = AppConfig.DEFAULT_DOMAIN
    if 'agent' not in st.session_state:
        st.session_state.agent = AssistantAgent(AppConfig.DEFAULT_DOMAIN)

def display_conversation_history():
    """Display the conversation history in the UI."""
    for conv in st.session_state.conversation_history:
        st.text_area("You:", conv["user_message"], height=100, disabled=True)
        st.text_area("Assistant:", conv["response"], height=200, disabled=True)
        st.markdown("---")

async def main():
    # Initialize session state
    initialize_session_state()
    
    # Page configuration
    st.set_page_config(
        page_title=AppConfig.APP_NAME,
        page_icon="🤖",
        layout="wide"
    )
    
    # Title and description
    st.title(f"🤖 {AppConfig.APP_NAME}")
    st.markdown(AppConfig.DESCRIPTION)

    # Sidebar
    with st.sidebar:
        st.markdown("### Settings")
        
        # Domain selection
        new_domain = st.selectbox(
            "Select Domain",
            AppConfig.SUPPORTED_DOMAINS,
            index=AppConfig.SUPPORTED_DOMAINS.index(st.session_state.current_domain)
        )
        
        # Update agent if domain changes
        if new_domain != st.session_state.current_domain:
            st.session_state.current_domain = new_domain
            st.session_state.agent = AssistantAgent(new_domain)
            st.session_state.conversation_history = []
            st.experimental_rerun()
        
        # Display domain capabilities
        st.markdown("### Domain Capabilities")
        for capability in st.session_state.agent.get_domain_capabilities():
            st.markdown(f"- {capability}")
        
        # Clear conversation button
        if st.button("Clear Conversation"):
            st.session_state.conversation_history = []
            st.session_state.agent.clear_conversation_history()
            st.experimental_rerun()

    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Ask Your Question")
        user_query = st.text_area(
            "Enter your question:",
            height=100,
            max_chars=AppConfig.MAX_QUERY_LENGTH,
            help=f"Maximum {AppConfig.MAX_QUERY_LENGTH} characters"
        )
        
        if st.button("Get Answer", key="submit"):
            if not user_query:
                st.warning("Please enter a question.")
            else:
                with st.spinner("Thinking..."):
                    response = await st.session_state.agent.get_response(user_query)
                    
                    if response["status"] == "success":
                        st.session_state.conversation_history.append({
                            "user_message": user_query,
                            "response": response["response"],
                            "metadata": response["metadata"]
                        })
                        
                        # Display the latest response
                        st.markdown("### Response:")
                        st.markdown(response["response"])
                        
                        # Display metadata in an expander
                        with st.expander("Response Metadata"):
                            st.json(response["metadata"])
                    else:
                        st.error(response["response"])
    
    with col2:
        st.markdown("### Conversation History")
        display_conversation_history()

if __name__ == "__main__":
    asyncio.run(main())
