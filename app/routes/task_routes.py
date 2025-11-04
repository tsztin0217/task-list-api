from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db
from datetime import datetime
tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


def validate_task(task_id):
    """Retrieves a task by ID or aborts with 400/404."""
    try:
        task_id = int(task_id)
    except:
        response = {"message": f"Task {task_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    if not task:
        response = {"message": f"Task {task_id} not found"}
        abort(make_response(response, 404))

    return task

@tasks_bp.post("")
def create_task():
    """Create a task with the data from the request body."""
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
    except:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_task)
    db.session.commit()

    response = new_task.to_dict()

    return response, 201

@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task)

    sort_param = request.args.get("sort")
    if sort_param == "asc":
        query = query.order_by(Task.title.asc())
    elif sort_param == "desc":
        query = query.order_by(Task.title.desc())

    tasks = db.session.scalars(query)

    tasks_response = [task.to_dict() for task in tasks]

    return tasks_response

@tasks_bp.get("/<task_id>")
def get_task(task_id):
    task = validate_task(task_id)

    tasks_response = task.to_dict()

    return tasks_response

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body.get("completed_at")

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@tasks_bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = validate_task(task_id)
    task.completed_at = datetime.now()
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_task(task_id)
    task.completed_at = None
    db.session.commit() 

    return Response(status=204, mimetype="application/json")

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")