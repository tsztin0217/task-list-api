from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db
tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# To do:
# make helper functions:
# 1: retrieve a model instance by id
# 2: handle the creation of new instances of a model from a dictionary, return expected response

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    title = request_body["title"]
    description = request_body["description"]
    completed_at = request_body.get("completed_at")

    new_task = Task(title=title, description=description, completed_at=completed_at)

    db.session.add(new_task)
    db.session.commit()

    response = new_task.return_dict()

    return response, 201

@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task).order_by(Task.id)

    tasks = db.session.scalars(query)

    tasks_response = [task.return_dict() for task in tasks]

    return tasks_response

@tasks_bp.get("/<task_id>")
def get_task(task_id):
    query = db.select(Task).where(Task.id == task_id)

    task = db.session.scalar(query)

    tasks_response = task.return_dict()

    return tasks_response

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    request_body = request.get_json()
    title = request_body["title"]
    description = request_body["description"]
    completed_at = request_body.get("completed_at")

    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    task.title = title
    task.description = description
    task.completed_at = completed_at

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    query = db.Select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")