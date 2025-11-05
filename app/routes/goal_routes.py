from flask import Blueprint
from .route_utilities import validate_model, create_model
from app.models.goal import Goal
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

