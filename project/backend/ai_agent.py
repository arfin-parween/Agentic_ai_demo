import os
import re
from typing import Tuple, Optional

from tools import query_medgemma, call_emergency

# ----------------------------
# Config via environment
# ----------------------------
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# ----------------------------
# Tools (plain python functions)
# ----------------------------
def ask_mental_health_specialist(query: str) -> str:
    """Therapeutic response using local MedGemma via Ollama (or any local model)."""
    return query_medgemma(query)

def emergency_call_tool() -> str:
    """Demo-safe emergency call (Twilio real call only if DEMO_MODE=false)."""
    return call_emergency()

def find_nearby_therapists_by_location(location: str) -> str:
    """Demo list of therapists near location (placeholder)."""
    return (
        f"Here are some therapists near {location}:\n"
        "- MindCare Counseling Center - +1 (555) 222-3333\n"
        "- Dr. Ayesha Kapoor - +1 (555) 123-4567\n"
        "- Dr. James Patel - +1 (555) 987-6543"
    )

SYSTEM_PROMPT = """
You are an AI engine supporting mental health conversations with warmth and vigilance.
If the user asks for therapists near a location, return therapist suggestions.
If the user expresses self-harm intent or suicide ideation, escalate urgently.
Otherwise provide supportive therapeutic guidance.
""".strip()

# ----------------------------
# Deterministic Router (for demo reliability)
# ----------------------------
SELF_HARM_PATTERNS = [
    r"\bkill myself\b",
    r"\bsuicide\b",
    r"\bend my life\b",
    r"\bwant to die\b",
    r"\bself harm\b",
    r"\bhurt myself\b",
    r"\bcut myself\b",
]

THERAPIST_PATTERNS = [
    r"\btherapist\b",
    r"\bcounsel(or|ing)\b",
    r"\bpsychologist\b",
    r"\bpsychiatrist\b",
    r"\bnear me\b",
    r"\bnear\b",
    r"\bin\s+[A-Za-z ]{2,}\b",
]

def _looks_like_self_harm(text: str) -> bool:
    t = text.lower()
    return any(re.search(p, t) for p in SELF_HARM_PATTERNS)

def _extract_location(text: str) -> Optional[str]:
    """
    Very simple extractor for demo:
    - "near Bangalore", "in Hyderabad", "near me in Mumbai"
    If not found, returns None.
    """
    t = text.strip()
    m = re.search(r"(?:near|in)\s+([A-Za-z ]{2,})", t, flags=re.IGNORECASE)
    if m:
        return m.group(1).strip().strip(".")
    return None

def _looks_like_find_therapist(text: str) -> bool:
    t = text.lower()
    # must include therapist-ish keyword OR "near <location>"
    return any(re.search(p, t) for p in THERAPIST_PATTERNS) and (
        "therap" in t or "counsel" in t or "psycholog" in t or "psychiat" in t or "near" in t
    )

def run_agent(message: str) -> Tuple[str, str, bool]:
    """
    Returns: (tool_called, response, demo_mode)
    """
    # 1) Emergency routing
    if _looks_like_self_harm(message):
        return "emergency_call_tool", emergency_call_tool(), DEMO_MODE

    # 2) Therapist lookup routing
    if _looks_like_find_therapist(message):
        loc = _extract_location(message) or "your area"
        return "find_nearby_therapists_by_location", find_nearby_therapists_by_location(loc), DEMO_MODE

    # 3) Default: therapist response
    return "ask_mental_health_specialist", ask_mental_health_specialist(message), DEMO_MODE