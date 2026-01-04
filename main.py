import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="MindMate", page_icon="🧠")
st.title("🧠 MindMate")
st.write("I am your student assistant. Paste your API key on the left to start!")

# 2. Sidebar for API Key
api_key = st.sidebar.text_input("Paste your API Key here:", type="password")

# 3. Logic
if api_key:
    try:
        genai.configure(api_key=api_key)

        # Using the model we found works for you
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
            # System instruction
            st.session_state.messages.append({
                "role": "user", 
                "parts": ["Act as a compassionate student mental health assistant. Be empathetic, short, and helpful."]
            })
            st.session_state.messages.append({
                "role": "model", 
                "parts": ["Understood. I am here to listen and help."]
            })

        # Show old messages
        for message in st.session_state.messages[2:]:
            with st.chat_message(message["role"]):
                st.markdown(message["parts"][0])

        # Chat Input
        if prompt := st.chat_input("Tell me what is stressing you out..."):
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "parts": [prompt]})

            # Get Answer
            response = model.generate_content(prompt)

            with st.chat_message("model"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "model", "parts": [response.text]})

    except Exception as e:
        st.error(f"Error: {e}")
