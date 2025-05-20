from flask_restful import Resource
from flask import request , jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime,timedelta
from . import db
from .model import SupplementaryMaterial,Assignment,LiveSession



# Add Lesson (Supplementary Material)
class LessonResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        required_fields = ["course_id", "material_type", "content"]
        if not all(field in data for field in required_fields):
            return {"message": "Missing required fields"}, 400

        lesson = SupplementaryMaterial(
            course_id=data["course_id"],
            material_type=data["material_type"],
            content=data["content"]
        )
        db.session.add(lesson)
        db.session.commit()
        return {"message": "Lesson added successfully"}, 201
    
# Add Assignment
class AssignmentResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        required_fields = ["course_id", "week_number", "assignment_link", "description"]
        if not all(field in data for field in required_fields):
            return {"message": "Missing required fields"}, 400

        assignment = Assignment(
            course_id=data["course_id"],
            week_number=data["week_number"],
            assignment_link=data["assignment_link"],
            description=data["description"]
        )
        db.session.add(assignment)
        db.session.commit()
        return {"message": "Assignment added successfully"}, 201

# Add Live Session
class LiveSessionResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        required_fields = ["course_id", "yt_link", "description"]
        if not all(field in data for field in required_fields):
            return {"message": "Missing required fields"}, 400

        session = LiveSession(
            course_id=data["course_id"],
            yt_link=data["yt_link"],
            description=data["description"]
        )
        db.session.add(session)
        db.session.commit()
        return {"message": "Live session added successfully"}, 201