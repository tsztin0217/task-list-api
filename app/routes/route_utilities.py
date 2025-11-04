from flask import abort, make_response
from ..db import db

def validate_model(cls, model_id):
    """Retrieves a model instance by ID or aborts with 400/404."""
    try:
        model_id = int(model_id)
    except:
        response = {"message": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == model_id)
    task = db.session.scalar(query)

    if not task:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))

    return task