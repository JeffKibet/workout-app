from marshmallow import Schema, fields


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(load_default=False)

    # Response only: the workouts this exercise appears in
    workout_exercises = fields.Nested(
        "WorkoutExerciseSchema", many=True, exclude=("exercise",), dump_only=True
    )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str(allow_none=True)

    workout_exercises = fields.Nested(
        "WorkoutExerciseSchema", many=True, exclude=("workout",), dump_only=True
    )


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)

    exercise = fields.Nested(
        "ExerciseSchema",
        only=("id", "name", "category", "equipment_needed"),
        dump_only=True,
    )
    workout = fields.Nested(
        "WorkoutSchema",
        only=("id", "date", "duration_minutes", "notes"),
        dump_only=True,
    )

# this instances are reusable
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True, exclude=("workout_exercises",))
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True, exclude=("workout_exercises",))
workout_exercise_schema = WorkoutExerciseSchema()