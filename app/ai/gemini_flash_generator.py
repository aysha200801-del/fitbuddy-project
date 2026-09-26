from ..config import GEMINI_TIP_MODEL
from ..schemas import UserInput
from .gemini_client import generate_text

def generate_nutrition_tip_with_flash(user: UserInput) -> str:
    prompt = f'''
Give one concise, practical nutrition or recovery tip for a FitBuddy user.
Goal: {user.goal}; age: {user.age}; weight: {user.weight} kg; intensity: {user.intensity}.
Prefer sustainable habits such as balanced meals, protein, hydration, sleep and recovery.
Do not prescribe extreme calorie restriction, supplements, or medical treatment.
Return a short heading and 2-4 sentences.
'''
    return generate_text(prompt, GEMINI_TIP_MODEL)
