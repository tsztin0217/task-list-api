from flask import Blueprint
from .route_utilities import validate_model, create_model
from app.models.goal import Goal
from app.models.task import Task
from ..db import db
from flask import request, make_response, abort, Response
bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)

@bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)

    goals = db.session.scalars(query)

    response = [goal.to_dict() for goal in goals]

    return response

@bp.get("/<goal_id>")
def get_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    response = goal.to_dict()

    return response
    

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.post("/<goal_id>/tasks")
def create_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    # retrieve python dictionary from request body
    request_body = request.get_json()

    # get list of task ids from dictionary
    task_ids = request_body.get("task_ids", [])
    
    # associate each task with the goal
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal = goal
        task.goal_id = goal.id

    # commit the changes to the database
    db.session.commit()


    response = {
        "id": goal.id,
        "task_ids": task_ids
    }

    return response, 200