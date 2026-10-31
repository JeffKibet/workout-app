# Workout Application Backend

A Flask REST API for a workout tracking app used by personal trainers. Trainers can create, view and delete workouts and reusable exercises, and add exercises to a workout with reps, sets, or duration. Built with Flask, SQLAlchemy, and Marshmallow.

## Features

- Three models: `Exercise`, `Workout`, and the `WorkoutExercise` join table (many-to-many between workouts and exercises)
- Validation at three layers: database table constraints, SQLAlchemy model validations, and Marshmallow schema validations
- Marshmallow schemas for serializing responses and validating request data
- A seed file that resets the database with starter data
- Cascading deletes: removing a workout or exercise also removes its `WorkoutExercise` rows

## Requirements

- Python 3.8.13 or higher
- [Pipenv](https://pipenv.pypa.io/)
- Git

## Installation

```bash
git clone <your-repo-url>
cd <repo-name>
pipenv install
pipenv shell
cd server
export FLASK_APP=app.py
flask db upgrade head
python seed.py
```

The migration files are included in the repo, so `flask db upgrade head` creates the tables. If you ever change a model, generate a new migration with:

```bash
flask db migrate -m "describe your change"
flask db upgrade head
```

## Running the app

From the `server/` folder:

```bash
python app.py
```

The API is served at `http://localhost:5555`.

To inspect data or try the validations by hand, open a shell with `flask shell`.

To reset the database to the starter data at any time, run `python seed.py` again.

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Show one workout with its exercises (reps, sets, duration) |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<id>` | Delete a workout and its WorkoutExercises |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Show one exercise with the workouts it appears in |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise and its WorkoutExercises |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

### Request bodies

**POST `/workouts`**
```json
{ "date": "2026-11-01", "duration_minutes": 45, "notes": "Leg day" }
```
`notes` is optional.

**POST `/exercises`**
```json
{ "name": "Lunge", "category": "strength", "equipment_needed": false }
```
`equipment_needed` defaults to `false`.

**POST `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises`**
```json
{ "reps": 12, "sets": 3 }
```
Provide at least one of `reps`, `sets`, or `duration_seconds`. `sets` must come with `reps` or `duration_seconds`.

### Example requests

```bash
curl localhost:5555/workouts

curl -X POST localhost:5555/exercises \
  -H "Content-Type: application/json" \
  -d '{"name": "Lunge", "category": "strength"}'

curl -X POST localhost:5555/workouts/1/exercises/2/workout_exercises \
  -H "Content-Type: application/json" \
  -d '{"reps": 12, "sets": 3}'

curl -X DELETE localhost:5555/workouts/1
```

### Responses and errors

| Status | Meaning |
|--------|---------|
| 200 | Successful read |
| 201 | Resource created |
| 204 | Resource deleted (empty body) |
| 400 | Validation failed (response includes the errors) |
| 404 | Workout or exercise not found |
| 409 | Database constraint violated, e.g. a duplicate exercise name |

## Validations

- **Table constraints:** exercise names are unique and non-blank; exercise categories are non-blank; workout `duration_minutes` must be greater than 0; `reps`, `sets` and `duration_seconds` on a WorkoutExercise must be positive
- **Model validations (`@validates`):** exercise name and category must be non-blank strings; workout duration must be a positive integer; reps, sets and duration must be positive integers
- **Schema validations (Marshmallow):** length and range validators on every field, strict integer types, required fields, and a `@validates_schema` rule that requires at least one of reps, sets or duration. Fields like `id` are `dump_only` and rejected if a client sends them

## Project structure

```
Pipfile
Pipfile.lock
README.md
server/
  app.py          # app configuration and routes
  models.py       # SQLAlchemy models, constraints, validations
  schemas.py      # Marshmallow schemas
  seed.py         # starter data
  migrations/     # database migration files
```

## Author

Jeff Kibet