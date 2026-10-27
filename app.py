import os
from typing import Final

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

FITNESS_GOALS: Final[list[str]] = [
    "Build muscle", "Lose fat", "General fitness", "Improve endurance"
]
EXPERIENCE_LEVELS: Final[list[str]] = ["Beginner", "Intermediate", "Advanced"]
EQUIPMENT_OPTIONS: Final[list[str]] = [
    "No equipment", "Home dumbbells", "Full gym"
]


def generate_workout_plan(
    fitness_goal: str,
    experience_level: str,
    days_per_week: int,
    equipment: str,
    limitations: str = "",
) -> str:
    """Generate a constraint-aware weekly workout plan using the Groq API."""
    if fitness_goal not in FITNESS_GOALS:
        raise ValueError("Please select a valid fitness goal.")
    if experience_level not in EXPERIENCE_LEVELS:
        raise ValueError("Please select a valid experience level.")
    if not 1 <= days_per_week <= 7:
        raise ValueError("Days per week must be between 1 and 7.")
    if equipment not in EQUIPMENT_OPTIONS:
        raise ValueError("Please select a valid equipment option.")

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Groq API key not found. Add GROQ_API_KEY to your .env file."
        )

    injury_note = (
        "\nThe user reported limitations/injuries. Avoid movements that may "
        "aggravate the stated limitation, do not diagnose or make medical "
        "claims, and include a brief safety disclaimer recommending a qualified "
        "health professional for injury-specific advice."
        if limitations.strip() else ""
    )

    prompt = f"""
Create a practical, personalized weekly workout plan using these details:
- Fitness goal: {fitness_goal}
- Experience level: {experience_level}
- Available training days: {days_per_week} per week (exactly this many workout days)
- Equipment: {equipment}
- Injuries or limitations: {limitations.strip() or "None reported"}

Requirements:
1. Use only exercises compatible with the equipment listed. No equipment means
   bodyweight exercises only.
2. Match volume and difficulty to the experience level and goal.
3. Clearly label each training day (Day 1, Day 2, etc.) and include rest/recovery
   guidance for non-training days.
4. For each exercise, list sets, reps or duration, and a short form cue.
5. Include a brief warm-up and cool-down, plus a concise progression tip.
6. Do not promise results or make medical claims.
7. Keep the response readable with Markdown headings and bullet points.
{injury_note}
"""

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful fitness-programming assistant. "
                        "Follow all user constraints exactly. Never invent "
                        "equipment the user does not have. Return a safe, "
                        "structured, actionable Markdown plan."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=2200,
        )
        content = response.choices[0].message.content
        if not content or not content.strip():
            raise ValueError("The AI returned an empty response. Please try again.")
        return content.strip()
    except ValueError:
        raise

    except Exception as exc:
        print(f"GROQ API ERROR: {type(exc).__name__}: {exc}")
    raise RuntimeError(
        "Unable to generate workout plan. Check the VS Code terminal for details."
    ) from exc


st.set_page_config(page_title="Workout Plan Generator", page_icon="💪", layout="centered")
st.title("Workout Plan Generator")
st.write("Create a weekly workout plan tailored to your goal, schedule, and equipment.")

with st.form("workout_form"):
    fitness_goal = st.selectbox("Fitness goal", FITNESS_GOALS)
    experience_level = st.selectbox("Experience level", EXPERIENCE_LEVELS)
    days_per_week = st.slider("Days available per week", min_value=1, max_value=7, value=3)
    equipment = st.selectbox("Equipment access", EQUIPMENT_OPTIONS)
    limitations = st.text_area(
        "Injuries or limitations (optional)",
        placeholder="e.g., avoid jumping, limited overhead movement",
        help="Share only what is relevant to exercise selection.",
    )
    submitted = st.form_submit_button("Generate Plan", type="primary", use_container_width=True)

if submitted:
    with st.spinner("Building your personalized plan..."):
        try:
            plan = generate_workout_plan(
                fitness_goal, experience_level, days_per_week, equipment, limitations
            )
            st.session_state["last_plan"] = plan
        except (ValueError, RuntimeError) as exc:
            st.error(str(exc))
        except Exception:
            st.error("Something unexpected happened. Please review your inputs and try again.")

if st.session_state.get("last_plan"):
    st.subheader("Your Weekly Plan")
    st.markdown(st.session_state["last_plan"])
    st.download_button(
        "Download plan (.md)",
        data=st.session_state["last_plan"],
        file_name="weekly_workout_plan.md",
        mime="text/markdown",
    )
    if limitations.strip():
        st.caption(
            "Safety note: This plan is general information, not medical advice. "
            "Consult a qualified healthcare professional about injury-specific exercise."
        )
