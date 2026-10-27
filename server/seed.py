from datetime import date

from app import app
from models import *

with app.app_context():
    print("Clearing tables...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Seeding exercises...")
    squat = Exercise(name="Squat", category="strength", equipment_needed=True)
    pushup = Exercise(name="Push-up", category="strength", equipment_needed=False)
    plank = Exercise(name="Plank", category="core", equipment_needed=False)
    run = Exercise(name="Treadmill Run", category="cardio", equipment_needed=True)
    db.session.add_all([squat, pushup, plank, run])

    print("Seeding workouts...")
    w1 = Workout(date=date(2026, 10, 20), duration_minutes=45, notes="Leg day")
    w2 = Workout(date=date(2026, 10, 22), duration_minutes=30, notes="Quick full-body session")
    w3 = Workout(date=date(2026, 10, 24), duration_minutes=60, notes=None)
    db.session.add_all([w1, w2, w3])
    db.session.commit()

    print("Linking exercises to workouts...")
    db.session.add_all([
        WorkoutExercise(workout=w1, exercise=squat, reps=10, sets=4),
        WorkoutExercise(workout=w1, exercise=plank, duration_seconds=60, sets=3),
        WorkoutExercise(workout=w2, exercise=pushup, reps=15, sets=3),
        WorkoutExercise(workout=w2, exercise=plank, duration_seconds=45),
        WorkoutExercise(workout=w3, exercise=run, duration_seconds=1800),
        WorkoutExercise(workout=w3, exercise=squat, reps=8, sets=5),
    ])
    db.session.commit()
    print("Done seeding.")