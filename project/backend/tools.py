from config import (
    DEMO_MODE,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_FROM_NUMBER,
    EMERGENCY_CONTACT,
    TWILIO_ENABLE_CALL,
)
import os

DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"
USE_OPENAI_THERAPIST = os.getenv("USE_OPENAI_THERAPIST", "true").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SYSTEM_THERAPIST_PROMPT = """You are Dr. Emily Hartman, a warm and experienced clinical psychologist.
Respond with:
1) Emotional attunement
2) Gentle normalization
3) Practical guidance
4) Strengths-focused support
Always ask an open-ended question at the end.
Keep it natural; no labels or brackets.
"""
# Optional: Ollama tool (local)
try:
    import ollama
except Exception:
    ollama = None


def query_medgemma(prompt: str) -> str:
    """
    Tries Ollama first (local). If not available (Streamlit Cloud), uses OpenAI.
    """
    # 1) If we are on cloud or want OpenAI, use OpenAI directly
    if USE_OPENAI_THERAPIST and OPENAI_API_KEY:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)

            resp = client.responses.create(
                model="gpt-4o-mini",
                input=[
                    {"role": "system", "content": SYSTEM_THERAPIST_PROMPT},
                    {"role": "user", "content": prompt},
                ],
            )
            return resp.output_text.strip()
        except Exception:
            return (
                "I’m here with you. I’m having trouble generating a response right now. "
                "Can you tell me a bit more about what you’re feeling?"
            )

    # 2) Otherwise try local Ollama (works only on your laptop where Ollama is running)
    try:
        import ollama
        response = ollama.chat(
            model="alibayram/medgemma:4b",
            messages=[
                {"role": "system", "content": SYSTEM_THERAPIST_PROMPT},
                {"role": "user", "content": prompt},
            ],
            options={"num_predict": 300, "temperature": 0.7, "top_p": 0.9},
        )
        return response["message"]["content"].strip()
    except Exception:
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
    # Always safe in demo mode
    if DEMO_MODE or not TWILIO_ENABLE_CALL:
        return (
            "✅ Demo: Emergency call triggered (simulation). "
            "In real deployment, this would place a call to the configured emergency contact."
        )

    # Real call path (only when explicitly enabled)
    if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER and EMERGENCY_CONTACT):
        return (
            "⚠️ Twilio call is enabled but configuration is incomplete. "
            "Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, EMERGENCY_CONTACT."
        )

    try:
        from twilio.rest import Client

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        call = client.calls.create(
            to=EMERGENCY_CONTACT,
            from_=TWILIO_FROM_NUMBER,
            url="http://demo.twilio.com/docs/voice.xml",
        )
        return f"📞 Emergency call placed successfully. Call SID: {call.sid}"
    except Exception as e:
        return f"❌ Failed to place call via Twilio: {e}"
