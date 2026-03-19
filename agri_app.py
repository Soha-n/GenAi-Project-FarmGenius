import streamlit as st
from agent import agent_executor

st.set_page_config(page_title="AI Farming Assistant", page_icon="🌾", layout="wide")

st.title("🌾 AI Farming Assistant")
st.markdown("Get expert advice on farming practices using AI-powered tools.")

st.sidebar.header("🎯 Select Objective")
objective = st.sidebar.selectbox(
    "Choose your farming objective:",
    [
        "General Assistant",
        "Crop Selection",
        "Soil Health",
        "Weather Guidance",
        "Pest and Disease Control",
        "Fertilizers and Irrigation",
        "Market Price Information"
    ]
)

if objective == "General Assistant":
    st.header("💬 General Assistant")
    st.markdown("Chat with the AI assistant about farming or any topic.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is your question?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            placeholder = st.empty()
            content = ""
            for chunk in agent_executor.stream(
                {"messages": st.session_state.messages},
                stream_mode="messages",
                version="v2",
            ):
                if chunk["type"] == "messages":
                    token, metadata = chunk["data"]
                    for block in token.content_blocks:
                        if block["type"] == "text":
                            text = block["text"]
                            if not content.endswith(text):
                                content += text
                    placeholder.markdown(content)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": content})

elif objective == "Crop Selection":
    st.header("🌱 Crop Selection")
    st.markdown("Get crop recommendations based on your location and conditions.")
    col1, col2 = st.columns(2)
    with col1:
        location = st.text_input("Location (e.g., Punjab, India):", key="crop_loc")
        soil_type = st.selectbox("Soil Type:", ["Clay", "Sandy", "Loamy", "Silt", "Peaty", "Chalky"], key="crop_soil")
    with col2:
        climate = st.selectbox("Climate:", ["Tropical", "Temperate", "Arid", "Semi-arid", "Mediterranean", "Continental"], key="crop_climate")
    
    if st.button("Suggest Crops", key="crop"):
        input_str = f"{location},{soil_type},{climate}"
        placeholder = st.empty()
        content = ""
        for chunk in agent_executor.stream(
            {"messages": [{"role": "user", "content": f"Use crop_selection tool with input: {input_str}"}]},
            stream_mode="messages",
            version="v2",
        ):
            if chunk["type"] == "messages":
                token, metadata = chunk["data"]
                for block in token.content_blocks:
                    if block["type"] == "text":
                        text = block["text"]
                        if not content.endswith(text):
                            content += text
                placeholder.markdown(f"### 🌾 Recommended Crops:\n{content}")
        st.success("Crop suggestions ready!")

elif objective == "Soil Health":
    st.header("🌿 Soil Health Analysis")
    st.markdown("Analyze your soil parameters and get improvement suggestions.")
    col1, col2 = st.columns(2)
    with col1:
        pH = st.slider("Soil pH Level:", 0.0, 14.0, 7.0, key="soil_ph")
        N = st.text_input("Nitrogen Level (ppm):", key="soil_n")
    with col2:
        P = st.text_input("Phosphorus Level (ppm):", key="soil_p")
        K = st.text_input("Potassium Level (ppm):", key="soil_k")
    
    if st.button("Analyze Soil", key="soil"):
        input_str = f"{pH},{N},{P},{K}"
        placeholder = st.empty()
        content = ""
        for chunk in agent_executor.stream(
            {"messages": [{"role": "user", "content": f"Use soil_health tool with input: {input_str}"}]},
            stream_mode="messages",
            version="v2",
        ):
            if chunk["type"] == "messages":
                token, metadata = chunk["data"]
                for block in token.content_blocks:
                    if block["type"] == "text":
                        text = block["text"]
                        if not content.endswith(text):
                            content += text
                placeholder.markdown(f"### 📊 Soil Health Report:\n{content}")
        st.success("Soil analysis complete!")

elif objective == "Weather Guidance":
    st.header("🌤️ Weather Guidance")
    st.markdown("Get weather information and farming advice for your location.")
    location = st.text_input("Location (e.g., New Delhi, India):", key="weather_loc")
    
    if st.button("Get Weather Guidance", key="weather"):
        placeholder = st.empty()
        content = ""
        for chunk in agent_executor.stream(
            {"messages": [{"role": "user", "content": f"Use weather_guidance tool with input: {location}"}]},
            stream_mode="messages",
            version="v2",
        ):
            if chunk["type"] == "messages":
                token, metadata = chunk["data"]
                for block in token.content_blocks:
                    if block["type"] == "text":
                        text = block["text"]
                        if not content.endswith(text):
                            content += text
                placeholder.markdown(f"### 🌦️ Weather & Farming Guidance:\n{content}")
        st.success("Weather guidance ready!")

elif objective == "Pest and Disease Control":
    st.header("🐛 Pest & Disease Control")
    st.markdown("Get control methods for crop pests and diseases.")
    col1, col2 = st.columns(2)
    with col1:
        crop = st.text_input("Crop (e.g., Wheat, Rice):", key="pest_crop")
    with col2:
        issue = st.text_input("Pest/Disease (e.g., Aphids, Rust):", key="pest_issue")
    
    if st.button("Get Control Methods", key="pest"):
        input_str = f"{crop},{issue}"
        placeholder = st.empty()
        content = ""
        for chunk in agent_executor.stream(
            {"messages": [{"role": "user", "content": f"Use pest_disease_control tool with input: {input_str}"}]},
            stream_mode="messages",
            version="v2",
        ):
            if chunk["type"] == "messages":
                token, metadata = chunk["data"]
                for block in token.content_blocks:
                    if block["type"] == "text":
                        text = block["text"]
                        if not content.endswith(text):
                            content += text
                placeholder.markdown(f"### 🛡️ Control Methods:\n{content}")
        st.success("Control methods ready!")

elif objective == "Fertilizers and Irrigation":
    st.header("💧 Fertilizers & Irrigation")
    st.markdown("Get recommendations for fertilizers and irrigation practices.")
    col1, col2 = st.columns(2)
    with col1:
        crop = st.text_input("Crop (e.g., Maize, Tomato):", key="fert_crop")
    with col2:
        soil_type = st.selectbox("Soil Type:", ["Clay", "Sandy", "Loamy", "Silt", "Peaty", "Chalky"], key="fert_soil")
    
    if st.button("Get Recommendations", key="fert"):
        input_str = f"{crop},{soil_type}"
        placeholder = st.empty()
        content = ""
        for chunk in agent_executor.stream(
            {"messages": [{"role": "user", "content": f"Use fertilizer_irrigation tool with input: {input_str}"}]},
            stream_mode="messages",
            version="v2",
        ):
            if chunk["type"] == "messages":
                token, metadata = chunk["data"]
                for block in token.content_blocks:
                    if block["type"] == "text":
                        text = block["text"]
                        if not content.endswith(text):
                            content += text
                placeholder.markdown(f"### 🌱 Fertilizer & Irrigation Plan:\n{content}")
        st.success("Recommendations ready!")

elif objective == "Market Price Information":
    st.header("💰 Market Price Information")
    st.markdown("Get current market prices and trends for crops.")
    crop = st.text_input("Crop (e.g., Wheat, Cotton):", key="market_crop")
    
    if st.button("Get Market Info", key="market"):
        placeholder = st.empty()
        content = ""
        for chunk in agent_executor.stream(
            {"messages": [{"role": "user", "content": f"Use market_price tool with input: {crop}"}]},
            stream_mode="messages",
            version="v2",
        ):
            if chunk["type"] == "messages":
                token, metadata = chunk["data"]
                for block in token.content_blocks:
                    if block["type"] == "text":
                        text = block["text"]
                        if not content.endswith(text):
                            content += text
                placeholder.markdown(f"### 📈 Market Price Report:\n{content}")
        st.success("Market information ready!")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Instructions")
st.sidebar.markdown("""
1. Select your farming objective from the dropdown, or choose General Assistant for chat.
2. Fill in the required information or chat with the AI.
3. Click the button to get AI-powered advice, or send messages in chat mode.
4. For general queries, use the 'General Assistant' option for conversational chat.
""")
st.sidebar.markdown("### 🔑 Setup")
st.sidebar.markdown("Make sure Ollama is installed and llama3.1 model is available.")