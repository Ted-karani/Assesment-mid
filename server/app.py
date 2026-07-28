from flask import Flask, make_response
from flask_migrate import Migrate

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(WorkoutSchema(many=True).dump(workouts)), 200



@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()

    try:
        new_workout = Workout(
            date=data.get('date'),
            duration_minutes=data.get('duration_minutes'),
            notes=data.get('notes')
        )
        db.session.add(new_workout)
        db.session.commit()
        return jsonify(WorkoutSchema().dump(new_workout)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.filter_by(id=id).first()
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    return jsonify(WorkoutSchema().dump(workout)), 200

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.filter_by(id=id).first()

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    db.session.delete(workout)
    db.session.commit()
    return '', 204

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(ExerciseSchema(many=True).dump(exercises)), 200


@app.route('/exercises', methods=['POST'])
def create_exercise():
     data = request.get_json()

     try:
        new_exercise = Exercise(
            name=data.get('name'),
            category=data.get('category'),
            equipment_needed=data.get('equipment_needed')
        )
        db.session.add(new_exercise)
        db.session.commit()
        return jsonify(ExerciseSchema().dump(new_exercise)), 201
     except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.filter_by(id=id).first()

    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    return jsonify(ExerciseSchema().dump(exercise)), 200

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.filter_by(id=id).first()

    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    db.session.delete(exercise)
    db.session.commit()
    return '', 204



if __name__ == '__main__':
    app.run(port=5555, debug=True)