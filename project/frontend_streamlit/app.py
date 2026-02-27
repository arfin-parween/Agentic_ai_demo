import os
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="SafeSpace AI Therapist Demo", page_icon="🧠", layout="centered")

st.title("🧠 SafeSpace AI Therapist (Demo)")
st.caption("FastAPI backend + Tool-calling (Therapist / Nearby therapists / Emergency call)")

with st.sidebar:
    st.subheader("Backend")
    st.write(f"Using: `{BACKEND_URL}`")
    if st.button("Ping /health"):
        try:
            r = requests.get(f"{BACKEND_URL}/health", timeout=10)
            st.success(r.json())
        except Exception as e:
            st.error(str(e))

st.divider()

if "chat" not in st.session_state:
    st.session_state.chat = []

for role, content in st.session_state.chat:
    with st.chat_message(role):
        st.markdown(content)

user_msg = st.chat_input("Type your message...")

if user_msg:
    st.session_state.chat.append(("user", user_msg))
    with st.chat_message("user"):
        st.markdown(user_msg)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                payload = {"message": user_msg}
                r = requests.post(f"{BACKEND_URL}/ask", json=payload, timeout=60)

                # If your backend returns 200 with JSON
                data = r.json()

                response = data.get("response") or data.get("detail") or "No response"
                tool = data.get("tool_called", "None")
                demo = data.get("demo_mode", None)

                st.markdown(response)
                st.caption(f"Tool called: `{tool}`" + (f" | demo_mode: `{demo}`" if demo is not None else ""))

                st.session_state.chat.append(("assistant", response))

            except Exception as e:
                st.error(f"Frontend error: {e}")