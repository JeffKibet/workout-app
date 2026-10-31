from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from models import *
from schemas import (exercise_schema, exercises_schema, workout_exercise_schema, workout_schema,workouts_schema,
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

def error(message, status):
    return make_response(jsonify({'error': message}), status)


def load_json(schema):
    """Validate the request body with a schema. Returns (data, error_response)."""
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return None, error('Request body must be a JSON object.', 400)
    try:
        return schema.load(payload), None
    except ValidationError as err:
        return None, make_response(jsonify({'errors': err.messages}), 400)


def save(obj):
    """Add and commit. Returns an error response on failure, otherwise None."""
    try:
        db.session.add(obj)
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        return error(f'Database constraint violated: {exc.orig}', 409)
    return None

@app.route('/workouts', methods=['GET'])
def list_workouts():
    workouts = Workout.query.order_by(Workout.date.desc(), Workout.id).all()
    return make_response(jsonify(workouts_schema.dump(workouts)), 200)

@app.route('/workouts/<int:id>', methods=['GET'])
def show_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return error(f'Workout {id} not found.', 404)
    return make_response(jsonify(workout_schema.dump(workout)), 200)

@app.route('/workouts', methods=['POST'])
def create_workout():
    data, err = load_json(workout_schema)
    if err:
        return err
    try:
        workout = Workout(**data)
    except ValueError as exc:  # model-level validation
        return error(str(exc), 400)
    err = save(workout)
    if err:
        return err
    return make_response(jsonify(workout_schema.dump(workout)), 201)

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return error(f'Workout {id} not found.', 404)
    db.session.delete(workout)
    db.session.commit()
    return make_response('', 204)

@app.route('/exercises', methods=['GET'])
def list_exercises():
    exercises = Exercise.query.order_by(Exercise.name).all()
    return make_response(jsonify(exercises_schema.dump(exercises)), 200)

@app.route('/exercises/<int:id>', methods=['GET'])
def show_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return error(f'Exercise {id} not found.', 404)
    return make_response(jsonify(exercise_schema.dump(exercise)), 200)

@app.route('/exercises', methods=['POST'])
def create_exercise():
    data, err = load_json(exercise_schema)
    if err:
        return err
    try:
        exercise = Exercise(**data)
    except ValueError as exc:
        return error(str(exc), 400)
    err = save(exercise)
    if err:
        return err
    return make_response(jsonify(exercise_schema.dump(exercise)), 201)

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return error(f'Exercise {id} not found.', 404)
    db.session.delete(exercise)
    db.session.commit()
    return make_response('', 204)

@app.route(
    '/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises',
    methods=['POST'],
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    if not workout:
        return error(f'Workout {workout_id} not found.', 404)
    exercise = db.session.get(Exercise, exercise_id)
    if not exercise:
        return error(f'Exercise {exercise_id} not found.', 404)

    data, err = load_json(workout_exercise_schema)
    if err:
        return err
    try:
        workout_exercise = WorkoutExercise(workout=workout, exercise=exercise, **data)
    except ValueError as exc:
        db.session.rollback()
        return error(str(exc), 400)
    err = save(workout_exercise)
    if err:
        return err
    return make_response(jsonify(workout_exercise_schema.dump(workout_exercise)), 201)

if __name__ == '__main__':
    app.run(port=5555, debug=True)