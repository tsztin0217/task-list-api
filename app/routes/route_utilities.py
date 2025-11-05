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
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))

    return model


def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_model)
    db.session.commit()

    response = new_model.to_dict()

    return response, 201

def get_models_with_filters(cls, filters=None, sort_param=None):
    """Retrieve all model instances, optionally applying filters."""
    query = db.select(cls)

    if filters:
        for attribute, value in filters.items():
            query = query.where(getattr(cls, attribute) == value)

    if sort_param == "asc":
        query = query.order_by(cls.title.asc())
    elif sort_param == "desc":
        query = query.order_by(cls.title.desc())

    models = db.session.scalars(query)

    response = [model.to_dict() for model in models]

    return response