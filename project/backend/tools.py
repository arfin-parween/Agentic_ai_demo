from config import (
    DEMO_MODE,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_FROM_NUMBER,
    EMERGENCY_CONTACT,
    TWILIO_ENABLE_CALL,
)

# Optional: Ollama tool (local)
try:
    import ollama
except Exception:
    ollama = None


def query_medgemma(prompt: str) -> str:
    """
    If Ollama is available -> call local medgemma.
    Else -> demo response (no crash).
    """
    system_prompt = (
        "You are Dr. Emily Hartman, a warm and experienced clinical psychologist.\n"
        "Respond with emotional attunement, gentle normalization, practical guidance,\n"
        "and strengths-focused support. Ask open-ended questions.\n"
        "Do not use brackets or labels."
    )

    # If Ollama isn't installed/running, do a safe fallback (especially for demo)
    if ollama is None:
        return (
            "I hear you. It sounds like you’ve been carrying a lot lately. "
            "Many people feel overwhelmed when multiple things pile up at once. "
            "What’s been the hardest part for you recently?"
        )

    try:
        resp = ollama.chat(
            model="alibayram/medgemma:4b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            options={"num_predict": 250, "temperature": 0.7, "top_p": 0.9},
        )
        return resp["message"]["content"].strip()
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