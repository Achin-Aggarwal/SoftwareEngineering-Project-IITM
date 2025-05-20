from flask_restful import Resource
from flask import request , jsonify
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime,timedelta
from . import db
from .model import Assignment,LiveSession,User,Course
import os 
from werkzeug.utils import secure_filename


class InstructorDetails(Resource):
    @jwt_required()
    def get(self):
        jwt_claims = get_jwt()
        instructor_id = jwt_claims.get("id")
        instructor = User.query.get(instructor_id )
        
        if not instructor:
            return {"message": "Instructor not found"}, 404

        return jsonify({
            "id": instructor.id,
            "name": instructor.name,
            "username": instructor.username,
            "email": instructor.email,
            "role": instructor.role.name,
            "created_at": instructor.created_at,
            "last_login": instructor.last_login
        })

class CourseListResource(Resource):
    @jwt_required()  
    def get(self):
        courses = Course.query.all()
        course_list = [{"id": course.id, "name": course.name} for course in courses]
        return jsonify(course_list)

# File upload directory
UPLOAD_FOLDER = "uploads/assignments"
ALLOWED_EXTENSIONS = {"csv"}

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Add Assignment
class AssignmentResource(Resource):
    @jwt_required()
    def post(self):
        jwt_claims = get_jwt()
        instructor_id = jwt_claims.get("id")
        instructor = User.query.get(instructor_id )
        if not instructor:
            return {"message": "Instructor not found"}, 404

        if "file" not in request.files:
            return {"message": "No file part in request"}, 400
        
        file = request.files["file"]
        course_id = request.form.get("course_id")
        week_number = request.form.get("week_number")
        assignment_type = request.form.get("assignment_type", "Assignment")  

        # Validate required fields
        if not all([course_id, week_number, file]):
            return {"message": "Missing required fields"}, 400

        if file.filename == "":
            return {"message": "No selected file"}, 400

        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)  # Save file

                # Create new assignment entry
                assignment = Assignment(
                    course_id=int(course_id),
                    week_number=int(week_number),
                    assignment_type=assignment_type,  # Added this line
                    file=file_path,
                    created_at=datetime.utcnow()
                )
                db.session.add(assignment)
                db.session.commit()

                return {
                    "message": "Assignment added successfully",
                    "assignment_id": assignment.id,
                    "assignment_type": assignment.assignment_type,
                    "file_path": file_path
                }, 201

            except Exception as e:
                db.session.rollback()
                return {"message": f"An error occurred: {str(e)}"}, 500
        else:
            return {"message": "Invalid file type. Only CSV files are allowed."}, 400
        


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