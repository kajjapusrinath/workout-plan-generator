# Workout Plan Generator

A single-page Streamlit app that creates personalized weekly workout plans using the Groq API.

## Features
- Structured fitness goal, experience, days/week, equipment, and optional limitations.
- Typed Python function with prompt design and Groq API integration.
- Input validation and friendly error messages.
- Markdown plan output, session persistence, and download.

## Setup
1. Install Python 3.10 or newer.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\activate
   # macOS/Linux: source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and replace the placeholder with your Groq API key.
5. Run:
   ```bash
   streamlit run app.py
   ```

Get an API key from https://console.groq.com/. Never commit `.env` or publish your API key.

## Testing checklist
- Generate a plan for each fitness goal and experience level.
- Check 1-day and 7-day schedules.
- Confirm no-equipment plans contain bodyweight exercises only.
- Enter a limitation and confirm the response includes a safety disclaimer.
- Test without a key and with an invalid key; the app should show a friendly error.
- Confirm an empty response does not crash the app.

## Safety
Plans provide general fitness information and are not medical advice. Users with injuries or medical concerns should consult an appropriate qualified professional.
