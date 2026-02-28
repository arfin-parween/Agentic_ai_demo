import os
import requests
import streamlit as st

st.set_page_config(page_title="Arfin AI Therapist (Demo)", page_icon="🧠")

BACKEND_URL = os.getenv("BACKEND_URL", "https://agentic-ai-demo-1.onrender.com")  # change if needed

st.title("Hi, I’m Arfin 👋")
st.caption("You can feel free to share your feelings here — I’m here to listen and support you.")

# Sidebar config
st.sidebar.header("Settings")
backend_url = st.sidebar.text_input("Backend URL", BACKEND_URL)
endpoint = st.sidebar.selectbox("Endpoint", ["/ask"], index=0)

st.sidebar.markdown("---")
st.sidebar.write("Quick tests:")
if st.sidebar.button("Check /health"):
    try:
        r = requests.get(f"{backend_url}/health", timeout=10)
        st.sidebar.success(r.text)
    except Exception as e:
        st.sidebar.error(str(e))

# Session state for chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Input box
user_msg = st.chat_input("Type your message...")

if user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.markdown(user_msg)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                url = f"{backend_url}{endpoint}"
                payload = {"message": user_msg}
                r = requests.post(url, json=payload, timeout=60)
                # Some APIs return {"detail": "..."} on error
                data = r.json() if r.headers.get("content-type", "").startswith("application/json") else {"response": r.text}

                response = data.get("response") or data.get("detail") or "No response"
                tool = data.get("tool_called", "None")
                demo_mode = data.get("demo_mode", None)

                st.markdown(response)

                # Show tool info
                meta = f"**Tool called:** `{tool}`"
                if demo_mode is not None:
                    meta += f"  |  **demo_mode:** `{demo_mode}`"
                st.caption(meta)

                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Request failed: {e}")
