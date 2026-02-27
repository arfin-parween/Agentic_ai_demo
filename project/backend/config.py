import os
from dotenv import load_dotenv

# Load backend/.env if present
load_dotenv()

def _get_bool(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "y", "on")

# Modes
DEMO_MODE = _get_bool("DEMO_MODE", False)  # if true: don't call OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

# Twilio config
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "").strip()
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "").strip()
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", "").strip()
EMERGENCY_CONTACT = os.getenv("EMERGENCY_CONTACT", "").strip()

# Safety: by default we DO NOT place real calls
TWILIO_ENABLE_CALL = _get_bool("TWILIO_ENABLE_CALL", False)