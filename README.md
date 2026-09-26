# FitBuddy

This version follows the video-style structure:

app/
- main.py
- config.py
- database.py
- schemas.py
- routes.py
- ai/
  - gemini_client.py
  - gemini_generator.py
  - gemini_flash_generator.py
  - updated_plan.py

templates/
static/
.env.example
requirements.txt

## Windows setup

py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload

Open http://127.0.0.1:8000
API docs: http://127.0.0.1:8000/docs
Admin: http://127.0.0.1:8000/view-all-users

If GEMINI_API_KEY is empty, the app runs in demo mode so you can test the UI and database first.
