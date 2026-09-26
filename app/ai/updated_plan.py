from ..config import GEMINI_WORKOUT_MODEL
from .gemini_client import generate_text

def update_workout_plan(user, original_plan: str, feedback: str) -> str:
    prompt = f'''
Update this FitBuddy 7-day workout plan based on user feedback.

User: {user.username}, age {user.age}, weight {user.weight} kg,
goal {user.goal}, intensity {user.intensity}

Original plan:
{original_plan}

Feedback:
{feedback}

Return a revised 7-day plan. Apply the feedback while keeping it practical and safe.
Include warm-up, main work, rest and cooldown/recovery. No medical diagnosis, dangerous
exercise, extreme dieting, or unsafe rapid weight loss.
'''
    return generate_text(prompt, GEMINI_WORKOUT_MODEL)
