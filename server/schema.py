from marshmallow import (Schema, ValidationError, fields, pre_load, validate, validates, validates_schema,
)


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    equipment_needed = fields.Bool(load_default=False)

    workout_exercises = fields.Nested(
        "WorkoutExerciseSchema", many=True, exclude=("exercise",), dump_only=True
    )

    @pre_load
    def strip_strings(self, data, **kwargs):
        data = dict(data)
        for key in ("name", "category"):
            if isinstance(data.get(key), str):
                data[key] = data[key].strip()
        return data

    @validates("name")
    def validate_name_not_blank(self, value):
        if not value.strip():
            raise ValidationError("Name cannot be blank.")


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(
        required=True, strict=True, validate=validate.Range(min=1, max=1440)
    )
    notes = fields.Str(allow_none=True, validate=validate.Length(max=1000))

    # Response only: the exercises in this workout, with reps/sets/duration
    workout_exercises = fields.Nested(
        "WorkoutExerciseSchema", many=True, exclude=("workout",), dump_only=True
    )


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(strict=True, allow_none=True, validate=validate.Range(min=1))
    sets = fields.Int(strict=True, allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(
        strict=True, allow_none=True, validate=validate.Range(min=1)
    )

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

    @validates_schema
    def validate_metrics(self, data, **kwargs):
        reps, sets, duration = (data.get(k) for k in ("reps", "sets", "duration_seconds"))
        if reps is None and sets is None and duration is None:
            raise ValidationError(
                "Provide at least one of reps, sets, or duration_seconds.",
                field_name="_schema",
            )
        if sets is not None and reps is None and duration is None:
            raise ValidationError(
                "sets requires reps or duration_seconds.", field_name="sets"
            )


# this instances are reusable
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True, exclude=("workout_exercises",))
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True, exclude=("workout_exercises",))
workout_exercise_schema = WorkoutExerciseSchema()