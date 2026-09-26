from ..config import GEMINI_WORKOUT_MODEL
from ..schemas import UserInput
from .gemini_client import generate_text


def generate_workout_gemini(user: UserInput) -> str:

    prompt = f"""
You are FitBuddy, an AI fitness-plan assistant.

Create a practical 7-day workout plan for:

Name: {user.username}
Age: {user.age}
Weight: {user.weight} kg
Goal: {user.goal}
Intensity: {user.intensity}

Give exactly 7 days.

Each day should have:
- Focus
- Warm-up
- Exercises with sets/reps or duration
- Rest guidance
- Cooldown/recovery

Match the requested intensity.

Avoid medical diagnosis, dangerous exercise, extreme dieting,
or unsafe rapid weight loss.

Return only the plan.
"""

    return generate_text(prompt, GEMINI_WORKOUT_MODEL)