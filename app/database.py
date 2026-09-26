from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), unique=True, index=True, nullable=False)
    username = Column(String(120), nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    goal = Column(String(50), nullable=False)
    intensity = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Plan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), index=True, nullable=False)
    original_plan = Column(Text, nullable=False)
    updated_plan = Column(Text)
    nutrition_tip = Column(Text)
    feedback = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)

Base.metadata.create_all(bind=engine)

def save_user(data):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == data.user_id).first()
        if user:
            user.username, user.age, user.weight = data.username, data.age, data.weight
            user.goal, user.intensity = data.goal, data.intensity
        else:
            user = User(user_id=data.user_id, username=data.username, age=data.age,
                        weight=data.weight, goal=data.goal, intensity=data.intensity)
            db.add(user)
        db.commit(); db.refresh(user); return user
    finally: db.close()

def save_plan(user_id, original_plan, nutrition_tip):
    db = SessionLocal()
    try:
        plan = Plan(user_id=user_id, original_plan=original_plan, nutrition_tip=nutrition_tip)
        db.add(plan); db.commit(); db.refresh(plan); return plan
    finally: db.close()

def get_user(user_id):
    db = SessionLocal()
    try: return db.query(User).filter(User.user_id == user_id).first()
    finally: db.close()

def get_original_plan(user_id):
    db = SessionLocal()
    try:
        return db.query(Plan).filter(Plan.user_id == user_id).order_by(Plan.id.desc()).first()
    finally: db.close()

def update_plan(user_id, updated_plan, feedback):
    db = SessionLocal()
    try:
        plan = get_original_plan(user_id) if False else db.query(Plan).filter(Plan.user_id == user_id).order_by(Plan.id.desc()).first()
        if not plan: return None
        plan.updated_plan, plan.feedback, plan.updated_at = updated_plan, feedback, datetime.utcnow()
        db.commit(); db.refresh(plan); return plan
    finally: db.close()

def get_all_users_with_plans():
    db = SessionLocal()
    try:
        result = []
        for user in db.query(User).order_by(User.id.desc()).all():
            plan = db.query(Plan).filter(Plan.user_id == user.user_id).order_by(Plan.id.desc()).first()
            result.append({"user": user, "plan": plan})
        return result
    finally: db.close()

def delete_user(user_id):
    db = SessionLocal()
    try:
        db.query(Plan).filter(Plan.user_id == user_id).delete()
        user = db.query(User).filter(User.user_id == user_id).first()
        if user: db.delete(user)
        db.commit()
    finally: db.close()
