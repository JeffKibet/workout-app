from flask import Flask, jsonify, make_response
from flask_migrate import Migrate

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/workouts', methods=['GET'])
def list_workouts():
    return make_response(jsonify({'message': 'list workouts'}), 200)

@app.route('/workouts/<int:id>', methods=['GET'])
def show_workout(id):
    return make_response(jsonify({'message': f'show workout {id}'}), 200)

@app.route('/workouts', methods=['POST'])
def create_workout():
    return make_response(jsonify({'message': 'create workout'}), 201)

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    return make_response(jsonify({'message': f'delete workout {id}'}), 200)

@app.route('/exercises', methods=['GET'])
def list_exercises():
    return make_response(jsonify({'message': 'list exercises'}), 200)

@app.route('/exercises/<int:id>', methods=['GET'])
def show_exercise(id):
    return make_response(jsonify({'message': f'show exercise {id}'}), 200)

@app.route('/exercises', methods=['POST'])
def create_exercise():
    return make_response(jsonify({'message': 'create exercise'}), 201)

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    return make_response(jsonify({'message': f'delete exercise {id}'}), 200)

@app.route(
    '/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises',
    methods=['POST'],
)
def add_exercise_to_workout(workout_id, exercise_id):
    return make_response(
        jsonify({'message': f'add exercise {exercise_id} to workout {workout_id}'}), 201
    )

if __name__ == '__main__':
    app.run(port=5555, debug=True)