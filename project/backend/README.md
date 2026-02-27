# SafeSpace AI Therapist Demo (FastAPI + React + Streamlit optional)

## 1) Backend (FastAPI)
### Run (uv)
cd backend
uv sync
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

Open Swagger:
http://localhost:8000/docs

### Demo emergency call (safe)
If DEMO_MODE=true, emergency call triggers only if message contains:
CALL_DEMO_NOW

## 2) Frontend (React)
cd frontend
npm install
npm run dev

Open:
http://localhost:5173

## 3) Environment variables
Copy:
backend/.env.example -> backend/.env

Set:
OPENAI_API_KEY=...
DEMO_MODE=true
DEMO_CALL_PHRASE=CALL_DEMO_NOW

(Optional Twilio for demo call)
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
TWILIO_FROM_NUMBER=...
EMERGENCY_CONTACT=...

## 4) Streamlit demo (optional)
You can run a simple Streamlit UI that calls the backend.

cd streamlit_app
pip install -r requirements.txt
streamlit run app.py