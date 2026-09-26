from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from .schemas import UserInput
from .database import (
    save_user,
    save_plan,
    get_user,
    get_original_plan,
    update_plan,
    get_all_users_with_plans,
    delete_user,
)

from .ai.gemini_generator import generate_workout_gemini
from .ai.gemini_flash_generator import generate_nutrition_tip_with_flash
from .ai.updated_plan import update_workout_plan

router = APIRouter()


def ctx(request, **data):
    return {"request": request, **data}


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return request.app.state.templates.TemplateResponse(
        request=request,
        name="index.html",
        context=ctx(request),
    )


@router.post("/generate-workout", response_class=HTMLResponse)
async def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):
    try:
        data = UserInput(
            username=username,
            user_id=user_id,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )

        user = save_user(data)

        workout = generate_workout_gemini(data)
        tip = generate_nutrition_tip_with_flash(data)

        save_plan(data.user_id, workout, tip)

        return request.app.state.templates.TemplateResponse(
            request=request,
            name="result.html",
            context=ctx(
                request,
                user=user,
                workout_plan=workout,
                nutrition_tip=tip,
                updated=False,
                message=None,
            ),
        )

    except Exception as exc:
        return request.app.state.templates.TemplateResponse(
            request=request,
            name="error.html",
            context=ctx(request, message=str(exc)),
            status_code=500,
        )


@router.post("/submit-feedback", response_class=HTMLResponse)
async def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
):
    try:
        user = get_user(user_id)
        plan = get_original_plan(user_id)

        if not user or not plan:
            raise ValueError("No saved plan was found for this User ID.")

        updated = update_workout_plan(
            user,
            plan.original_plan,
            feedback,
        )

        update_plan(user_id, updated, feedback)

        return request.app.state.templates.TemplateResponse(
            request=request,
            name="result.html",
            context=ctx(
                request,
                user=user,
                workout_plan=updated,
                nutrition_tip=plan.nutrition_tip,
                updated=True,
                message="Your workout plan has been updated using your feedback.",
            ),
        )

    except Exception as exc:
        return request.app.state.templates.TemplateResponse(
            request=request,
            name="error.html",
            context=ctx(request, message=str(exc)),
            status_code=400,
        )


@router.get("/view-all-users", response_class=HTMLResponse)
async def view_all_users(request: Request):
    return request.app.state.templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context=ctx(
            request,
            rows=get_all_users_with_plans(),
        ),
    )


@router.post("/delete-user/{user_id}")
async def remove_user(user_id: str):
    delete_user(user_id)
    return RedirectResponse(
        "/view-all-users",
        status_code=303,
    )