from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from marshmallow import Schema, fields, validates, ValidationError
db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise')
    workouts = association_proxy('workout_exercises', 'workout')

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Exercise must have a name.')
        return name

    def __repr__(self):
        return f'<Exercise {self.id}, {self.name}, {self.category}>'

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout')
    exercises = association_proxy('workout_exercises', 'exercise')

    def __repr__(self):
        return f'<Workout {self.id}, {self.date}, {self.duration_minutes} min>'    

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    def __repr__(self):
        return f'<WorkoutExercise {self.id}, reps={self.reps}, sets={self.sets}>'    

class WorkoutExerciseSchema(Schema):
    id = fields.Integer()
    reps = fields.Integer()
    sets = fields.Integer()
    duration_seconds = fields.Integer()
    workout = fields.Nested(lambda: WorkoutSchema(exclude=("workout_exercises",)))
    exercise = fields.Nested(lambda: ExerciseSchema(exclude=("workout_exercises",)))

    @validates('reps')
    def validate_reps(self, value):
        if value is not None and value < 0:
            raise ValidationError('Reps cannot be negative.')


class WorkoutSchema(Schema):
    id = fields.Integer()
    date = fields.Date()
    duration_minutes = fields.Integer()
    notes = fields.String()
    workout_exercises = fields.Nested(lambda: WorkoutExerciseSchema(exclude=("workout",)), many=True)


class ExerciseSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    category = fields.String()
    equipment_needed = fields.Boolean()
    workout_exercises = fields.Nested(lambda: WorkoutExerciseSchema(exclude=("exercise",)), many=True)    