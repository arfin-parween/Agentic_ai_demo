import os

# Optional: Ollama tool (local)
try:
    import ollama
except Exception:
    ollama = None

SYSTEM_THERAPIST_PROMPT = """You are Dr. Emily Hartman, a warm and experienced clinical psychologist.
Respond with:
1) Emotional attunement
2) Gentle normalization
3) Practical guidance
4) Strengths-focused support
Always ask an open-ended question at the end.
Keep it natural; no labels or brackets.
"""

def query_medgemma(prompt: str) -> str:
    """
    If USE_OPENAI_THERAPIST=true and OPENAI_API_KEY is set -> use OpenAI.
    Else try Ollama locally (only works on your laptop).
    """
    use_openai = os.getenv("USE_OPENAI_THERAPIST", "true").lower() == "true"
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()

    # --- OpenAI path (best for Streamlit Cloud + Render) ---
    if use_openai and openai_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)

            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_THERAPIST_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )
            return completion.choices[0].message.content.strip()

        except Exception as e:
            print("🔥 OpenAI therapist error:", repr(e))
            return (
                "I’m here with you. I’m having trouble generating a response right now. "
                "Can you tell me a bit more about what you’re feeling?"
            )

    # --- Ollama path (local laptop only) ---
    if ollama is not None:
        try:
            response = ollama.chat(
                model="alibayram/medgemma:4b",
                messages=[
                    {"role": "system", "content": SYSTEM_THERAPIST_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                options={"num_predict": 300, "temperature": 0.7, "top_p": 0.9},
            )
            return response["message"]["content"].strip()
        except Exception as e:
            print("🔥 Ollama therapist error:", repr(e))

    return (
        "I’m here with you. Something went wrong on my side, but your feelings still matter. "
        "Can you tell me a little more about what you’re experiencing right now?"
    )


def call_emergency() -> str:
    """
    Demo-safe emergency call tool.
    - Default: SIMULATES call (no real call)
    - If TWILIO_ENABLE_CALL=true and Twilio creds exist: places a real call
    """
    demo_mode = os.getenv("DEMO_MODE", "true").lower() == "true"
    twilio_enable_call = os.getenv("TWILIO_ENABLE_CALL", "false").lower() == "true"

    twilio_sid = os.getenv("TWILIO_ACCOUNT_SID", "").strip()
    twilio_token = os.getenv("TWILIO_AUTH_TOKEN", "").strip()
    twilio_from = os.getenv("TWILIO_FROM_NUMBER", "").strip()
    emergency_to = os.getenv("EMERGENCY_CONTACT", "").strip()

    # Always safe in demo mode
    if demo_mode or not twilio_enable_call:
        return (
            "✅ Demo: Emergency call triggered (simulation). "
            "In real deployment, this would place a call to the configured emergency contact."
        )

    # Real call path (only when explicitly enabled)
    if not (twilio_sid and twilio_token and twilio_from and emergency_to):
        return (
            "⚠️ Twilio call is enabled but configuration is incomplete. "
            "Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, EMERGENCY_CONTACT."
        )

    try:
        from twilio.rest import Client
        client = Client(twilio_sid, twilio_token)

        call = client.calls.create(
            to=emergency_to,
            from_=twilio_from,
            url="http://demo.twilio.com/docs/voice.xml",
        )
        return f"📞 Emergency call placed successfully. Call SID: {call.sid}"
    except Exception as e:
        return f"❌ Failed to place call via Twilio: {e}"
