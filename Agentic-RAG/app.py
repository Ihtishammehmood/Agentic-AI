import streamlit as st
from utils import save_uploaded_files, initialize_agent


def main():
    st.set_page_config(page_title="Agentic RAG", page_icon='🛢')
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "agent" not in st.session_state or st.session_state.agent is None:
        with st.spinner("Initializing agent..."):
            st.session_state.agent = initialize_agent()
            st.session_state.documents_loaded = False

    with st.sidebar:
        st.header("Document Management")
        uploaded_files = st.file_uploader(
            "Upload PDF/DOC files (optional)",
            type=["pdf", "doc", "docx"],
            accept_multiple_files=True
        )
        if uploaded_files:
            save_uploaded_files(uploaded_files)
            with st.spinner("Processing documents..."):
                st.session_state.agent.knowledge.load(recreate=False)
                st.session_state.documents_loaded = True
            st.success(f"Processed {len(uploaded_files)} documents!")

        st.markdown("---")
        st.markdown("### Features")
        st.markdown("- Chat with SQL database")
        st.markdown("- Upload documents for document-based Q&A")
        st.markdown("- Use calculator, web search, and financial tools")
        st.markdown("---")
        st.markdown('Github: [Source Code](https://github.com/Ihtishammehmood/Agentic-AI.git)')
        st.markdown('Made with ❤️ by [Ihtisham M.](https://www.linkedin.com/in/ihtishammehmood/)')    
    st.title("Agentic RAG: AI Assistant")
    if st.session_state.get("documents_loaded", False):
        st.write('Agentic RAG is now ready with your documents and database access!')
    else:
        st.write('Agent is ready to answer  queries. Upload documents for additional capabilities.')

    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"`User:` {message['content']}")
        else:
            st.markdown(f"`Agent:` {message['content']}")
    if prompt := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.markdown(f"`User:` {prompt}")

        response_placeholder = st.empty()
        full_response = ""
        for chunk in st.session_state.agent.run(prompt, stream=True):
            if chunk:
                content_chunk = chunk.content
                full_response += content_chunk
                response_placeholder.markdown(f"`Agent:` {full_response}▌")
        response_placeholder.markdown(f"`Agent:` {full_response}")
        st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()
