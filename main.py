import os
import streamlit as st
from load_documents import get_document_chunks
from vector import VectorStore
from rag_chain import FarmGenius
import time

# Set page config
st.set_page_config(
    page_title="FarmGenius - Smart Agriculture Assistant",
    page_icon="🌾",
    layout="wide"
)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "farm_genius" not in st.session_state:
    st.session_state.farm_genius = None

def initialize_farm_genius():
    """Initialize the FarmGenius system."""
    try:
        status = st.empty()
        with status.status("🌾 Initializing FarmGenius...", expanded=True) as s:
            vector_store = None

            # Try to load agriculture documents into the vector store
            try:
                st.write("📄 Loading agriculture documents...")
                chunks = get_document_chunks()
                vector_store = VectorStore()
                if not os.path.exists("chroma_db"):
                    st.write("🗄️ Creating knowledge base for the first time...")
                    vector_store.create_vector_store(chunks)
                else:
                    st.write("🗄️ Loading existing knowledge base...")
                    vector_store.load_vector_store()
                st.write(f"✅ Knowledge base ready — {len(chunks)} document chunks loaded.")
            except Exception:
                st.write("⚠️ No PDFs found — running in general knowledge mode.")

            st.write("🤖 Starting LLM...")
            farm_genius = FarmGenius(vector_store)
            s.update(label="✅ FarmGenius ready!", state="complete", expanded=False)

        # Clear the status box entirely after init
        status.empty()
        return farm_genius
    except Exception as e:
        st.error(f"Error initializing FarmGenius: {str(e)}")
        return None

def main():
    # ----------------------------------------------------------------
    # Sidebar: settings panel
    # ----------------------------------------------------------------
    with st.sidebar:
        st.header("⚙️ Settings")

        # Search provider status
        st.subheader("🔍 Web Search")
        if st.session_state.farm_genius:
            if st.session_state.farm_genius.search_source == "DuckDuckGo":
                st.success("🔍 DuckDuckGo Search active")
            else:
                st.warning("⚠️ Web search unavailable")
        else:
            st.info("Initializing...")

        st.markdown("---")
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

        st.markdown("---")
        st.caption(
            "**FarmGenius** combines:\n"
            "- 📄 Uploaded agriculture PDFs\n"
            "- 🌐 DuckDuckGo live web search\n"
            "- 🤖 Ollama LLM (llama3.2:3b)"
        )

    # ----------------------------------------------------------------
    # Main page
    # ----------------------------------------------------------------
    # Title and description
    st.title("🌾 FarmGenius")
    st.markdown("""
    Welcome to **FarmGenius**, your smart agriculture assistant for Indian farmers!
    Ask questions about crop selection, soil health, weather guidance, pest & disease control,
    fertilizers, irrigation, and market prices.
    I'll maintain context of our conversation to provide more relevant and personalized responses.
    """)

    # Topic quick-reference badges
    st.markdown(
        """
        <div style='display:flex; flex-wrap:wrap; gap:8px; margin-bottom:12px;'>
          <span style='background:#2e7d32; color:white; padding:4px 12px; border-radius:16px; font-size:13px;'>🌱 Crop Selection</span>
          <span style='background:#558b2f; color:white; padding:4px 12px; border-radius:16px; font-size:13px;'>🪨 Soil Health</span>
          <span style='background:#0277bd; color:white; padding:4px 12px; border-radius:16px; font-size:13px;'>🌦️ Weather Guidance</span>
          <span style='background:#c62828; color:white; padding:4px 12px; border-radius:16px; font-size:13px;'>🐛 Pest & Disease Control</span>
          <span style='background:#ef6c00; color:white; padding:4px 12px; border-radius:16px; font-size:13px;'>💧 Fertilizers & Irrigation</span>
          <span style='background:#6a1b9a; color:white; padding:4px 12px; border-radius:16px; font-size:13px;'>📈 Market Prices</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Initialize FarmGenius if not already initialized
    if st.session_state.farm_genius is None:
        st.session_state.farm_genius = initialize_farm_genius()
    
    if st.session_state.farm_genius is None:
        st.error("""
        Failed to initialize FarmGenius. Please ensure:
        1. Ollama is installed and running
        2. The llama3.2:3b model is pulled (run: `ollama pull llama3.2:3b`)
        3. The required agriculture PDF documents are in the data directory
        """)
        return
    
    # Chat interface
    st.markdown("---")
    
    # Display chat history with improved styling
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask your farming question (e.g. best crops for black soil, how to treat leaf blight...)"):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Pass chat history to get more contextual responses
                    response = st.session_state.farm_genius.get_response(
                        prompt,
                        chat_history=st.session_state.chat_history[:-1]  # Exclude current message
                    )
                    st.markdown(response)
                    
                    # Add assistant response to chat history
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"I apologize, but I encountered an error: {str(e)}. Please try again or rephrase your question."
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main() 