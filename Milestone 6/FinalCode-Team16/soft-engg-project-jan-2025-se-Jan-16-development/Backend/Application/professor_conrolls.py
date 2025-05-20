from flask_restful import Resource
from flask import request , jsonify
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime,timedelta
from . import db
from .model import User,InstructorRequest,RequestStatus,SupplementaryMaterial



class ProfessorDetails(Resource):
    @jwt_required()
    def get(self):
        jwt_claims = get_jwt()
        professor_id = jwt_claims.get("id")
        professor = User.query.get(professor_id)
        
        if not professor:
            return {"message": "Professor not found"}, 404

        return jsonify({
            "id": professor.id,
            "name": professor.name,
            "username": professor.username,
            "email": professor.email,
            "role": professor.role.name,
            "created_at": professor.created_at,
            "last_login": professor.last_login
        })
    

class PendingInstructors(Resource):
    @jwt_required()
    def get(self):
        """ Retrieve all pending instructors """
        jwt_claims = get_jwt()
        professor_id = jwt_claims.get("id")
        professor = User.query.get(professor_id)
        
        if not professor:
            return {"message": "Professor not found"}, 404
        
        pending_requests = (
            db.session.query(
                InstructorRequest.id,
                InstructorRequest.instructor_id,
                InstructorRequest.status,
                InstructorRequest.created_at,
                User.name.label("instructor_name")  # Fetch instructor name
            )
            .join(User, InstructorRequest.instructor_id == User.id)  # Join with User table
            .filter(InstructorRequest.status == RequestStatus.PENDING)
            .all()
        )

        return jsonify([{
            "id": req.id,
            "instructor_id": req.instructor_id,
            "instructor_name": req.instructor_name,  # ✅ Now exists in query result
            "status": req.status.value,
            "created_at": req.created_at
        } for req in pending_requests])


class ApproveInstructor(Resource):
    @jwt_required()
    def put(self, request_id):
        """ Professor approves/rejects an instructor request """
        jwt_claims = get_jwt()
        professor_id = jwt_claims.get("id")
        professor = User.query.get(professor_id)

        if not professor:
            return {"message": "Professor not found"}, 404

        data = request.get_json()
        new_status = data.get("status")

        if new_status not in [RequestStatus.APPROVED.value, RequestStatus.REJECTED.value]:
            return {"message": "Invalid status, use 'Approved' or 'Rejected'"}, 400

        request_record = InstructorRequest.query.get(request_id)

        if not request_record:
            return {"message": "Instructor request not found"}, 404

        request_record.status = RequestStatus[new_status.upper()]
        db.session.commit()

        return {"message": f"Instructor request {new_status.lower()} successfully"}


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

