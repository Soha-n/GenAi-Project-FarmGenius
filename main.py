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
if "general_chat_history" not in st.session_state:
    st.session_state.general_chat_history = []
if "objective_chat_history" not in st.session_state:
    st.session_state.objective_chat_history = []
if "last_objective" not in st.session_state:
    st.session_state.last_objective = "General Assistant"

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

        st.subheader("🎯 Objective")
        objective = st.selectbox(
            "Choose your farming objective:",
            [
                "General Assistant",
                "Crop Selection",
                "Soil Health",
                "Weather Guidance",
                "Pest and Disease Control",
                "Fertilizers and Irrigation",
                "Market Price Information",
            ],
        )

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
    st.title("🌾 FarmGenius - AI Farming Assistant")
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

    # Objective-aware session behavior:
    # - General Assistant keeps its own persistent history.
    # - Switching to another objective starts a fresh objective session.
    if objective != st.session_state.last_objective:
        if objective != "General Assistant":
            st.session_state.objective_chat_history = []
        st.session_state.last_objective = objective

    if objective == "General Assistant":
        active_history = st.session_state.general_chat_history
    else:
        active_history = st.session_state.objective_chat_history

    # Keep legacy key in sync for minimum downstream changes.
    st.session_state.chat_history = active_history

    # Clear only the currently active objective's chat.
    with st.sidebar:
        if st.button("🗑️ Clear Current Chat"):
            if objective == "General Assistant":
                st.session_state.general_chat_history = []
            else:
                st.session_state.objective_chat_history = []
            st.rerun()

    def process_prompt(prompt: str) -> None:
        """Run one prompt through FarmGenius and append to chat history."""
        active_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.farm_genius.get_response(
                        prompt,
                        chat_history=active_history[:-1],
                    )
                    st.markdown(response)
                    active_history.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"I apologize, but I encountered an error: {str(e)}. Please try again or rephrase your question."
                    st.error(error_msg)
                    active_history.append({"role": "assistant", "content": error_msg})
    
    # Chat interface
    st.markdown("---")

    # Display existing chat history FIRST (before forms/buttons)
    for message in active_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Objective-specific inputs
    if objective == "Crop Selection":
        st.subheader("🌱 Crop Selection")
        col1, col2 = st.columns(2)
        with col1:
            location = st.text_input("Location (e.g., Punjab, India):", key="obj_crop_loc")
            soil_type = st.selectbox("Soil Type:", ["Clay", "Sandy", "Loamy", "Silt", "Peaty", "Chalky"], key="obj_crop_soil")
        with col2:
            climate = st.selectbox("Climate:", ["Tropical", "Temperate", "Arid", "Semi-arid", "Mediterranean", "Continental"], key="obj_crop_climate")

        if st.button("Suggest Crops", key="obj_crop_btn"):
            prompt = (
                f"Suggest 3-5 suitable crops for farming in {location} with {soil_type} soil and {climate} climate. "
                "Give practical reasons and a simple first action plan. Keep your response concise and summarized."
            )
            process_prompt(prompt)

    elif objective == "Soil Health":
        st.subheader("🪨 Soil Health")
        col1, col2 = st.columns(2)
        with col1:
            soil_ph = st.slider("Soil pH Level:", 0.0, 14.0, 7.0, key="obj_soil_ph")
            n_value = st.text_input("Nitrogen Level (ppm):", key="obj_soil_n")
        with col2:
            p_value = st.text_input("Phosphorus Level (ppm):", key="obj_soil_p")
            k_value = st.text_input("Potassium Level (ppm):", key="obj_soil_k")

        if st.button("Analyze Soil", key="obj_soil_btn"):
            prompt = (
                f"Analyze this soil report: pH={soil_ph}, Nitrogen={n_value} ppm, Phosphorus={p_value} ppm, Potassium={k_value} ppm. "
                "Give a soil health diagnosis and improvement steps. Keep your response concise and summarized."
            )
            process_prompt(prompt)

    elif objective == "Weather Guidance":
        st.subheader("🌦️ Weather Guidance")
        weather_location = st.text_input("Location (e.g., New Delhi, India):", key="obj_weather_loc")
        if st.button("Get Weather Guidance", key="obj_weather_btn"):
            prompt = (
                f"Provide weather-based farming guidance for {weather_location}. "
                "Include short-term planning, irrigation advice, and crop protection suggestions. Keep your response concise and summarized."
            )
            process_prompt(prompt)

    elif objective == "Pest and Disease Control":
        st.subheader("🐛 Pest and Disease Control")
        col1, col2 = st.columns(2)
        with col1:
            pest_crop = st.text_input("Crop (e.g., Wheat, Rice):", key="obj_pest_crop")
        with col2:
            pest_issue = st.text_input("Pest/Disease (e.g., Aphids, Rust):", key="obj_pest_issue")

        if st.button("Get Control Methods", key="obj_pest_btn"):
            prompt = (
                f"For {pest_crop} affected by {pest_issue}, provide control methods. "
                "Include preventive, organic, and chemical options with safe usage guidance. Keep your response concise and summarized."
            )
            process_prompt(prompt)

    elif objective == "Fertilizers and Irrigation":
        st.subheader("💧 Fertilizers and Irrigation")
        col1, col2 = st.columns(2)
        with col1:
            fert_crop = st.text_input("Crop (e.g., Maize, Tomato):", key="obj_fert_crop")
        with col2:
            fert_soil = st.selectbox("Soil Type:", ["Clay", "Sandy", "Loamy", "Silt", "Peaty", "Chalky"], key="obj_fert_soil")

        if st.button("Get Recommendations", key="obj_fert_btn"):
            prompt = (
                f"For {fert_crop} in {fert_soil} soil, recommend fertilizer and irrigation schedule. "
                "Include timing, dosage guidance, and water-saving practices. Keep your response concise and summarized."
            )
            process_prompt(prompt)

    elif objective == "Market Price Information":
        st.subheader("📈 Market Price Information")
        market_crop = st.text_input("Crop (e.g., Wheat, Cotton):", key="obj_market_crop")
        if st.button("Get Market Info", key="obj_market_btn"):
            prompt = (
                f"Provide current market price guidance for {market_crop} in India. "
                "Include trend summary, factors affecting prices, and selling strategy tips. Keep your response concise and summarized."
            )
            process_prompt(prompt)

    # Chat input available in ALL modes for follow-up questions
    if objective == "General Assistant":
        chat_placeholder = "Ask your farming question (e.g. best crops for black soil, how to treat leaf blight...)"
    else:
        chat_placeholder = "Ask a follow-up question about the results above..."

    if prompt := st.chat_input(chat_placeholder):
        process_prompt(prompt)

if __name__ == "__main__":
    main() 