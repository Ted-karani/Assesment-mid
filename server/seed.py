
from app import app
from models import  db, Exercise, Workout, WorkoutExercise
import datetime


with app.app_context():
      #first i make a command to clear data like to initialise it when i run it. getting idea from canvas lab.
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    exercise1 = Exercise(name="Push Ups", category="Strength", equipment_needed=False)
    exercise2 = Exercise(name="Bench Press", category="Strength", equipment_needed=True)
    exercise3 = Exercise(name="Running", category="Cardio", equipment_needed=False)
    db.session.add_all([exercise1, exercise2, exercise3])
    db.session.commit()

    workout1 = Workout(date=datetime.date(2026, 7, 1), duration_minutes=45, notes="Morning strength session")
    workout2 = Workout(date=datetime.date(2026, 7, 3), duration_minutes=30, notes="Quick cardio run")
    db.session.add_all([workout1, workout2])
    db.session.commit()

    we1 = WorkoutExercise(workout=workout1, exercise=exercise1, reps=15, sets=3, duration_seconds=None)
    we2 = WorkoutExercise(workout=workout1, exercise=exercise2, reps=10, sets=4, duration_seconds=None)
    we3 = WorkoutExercise(workout=workout2, exercise=exercise3, reps=None, sets=None, duration_seconds=1200)
    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print("databsase seeded.")
   