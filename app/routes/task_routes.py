from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db
from datetime import datetime
import requests
import os
from .route_utilities import validate_model, create_model, get_models_with_filters

path = "https://slack.com/api/chat.postMessage"
token = os.environ.get("SLACK_API_TOKEN")


bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")



@bp.post("")
def create_task():
    """Create a task with the data from the request body."""
    request_body = request.get_json()
    return create_model(Task, request_body)

@bp.get("")
def get_all_tasks():
    return get_models_with_filters(Task, 
                                   sort_param=request.args.get("sort"))

@bp.get("/<task_id>")
def get_task(task_id):
    task = validate_model(Task, task_id)

    response = task.to_dict()

    return response

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body.get("completed_at")

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()
    db.session.commit()

    query_params = {
        "channel": "#test-slack-api",
        "text": f"Someone just completed the task {task.title}"
    }

    headers = {"Authorization": f"Bearer {token}"}

    requests.post(path, json=query_params, headers=headers)

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit() 

    return Response(status=204, mimetype="application/json")

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")