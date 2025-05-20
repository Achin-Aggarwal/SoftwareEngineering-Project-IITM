from flask_restful import Resource
from flask import request , jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime,timedelta
from . import db
from .model import User, ChatbotHistory,IssueQuery,SolveIssue,Course,CourseMaterial


class TopSupportQueries(Resource):
    @jwt_required()
    def get(self):
        # Get date 7 days ago
        last_week = datetime.utcnow() - timedelta(days=7)

        # Fetch top 5 most asked queries in the past 7 days
        queries = (
            db.session.query(ChatbotHistory.query_text, db.func.count(ChatbotHistory.id).label("count"))
            .filter(ChatbotHistory.timestamp >= last_week)
            .group_by(ChatbotHistory.query_text)
            .order_by(db.desc("count"))
            .limit(5)
            .all()
        )

        # Format response
        query_list = [{"query": q.query_text, "count": q.count} for q in queries]

        return jsonify({"top_queries": query_list})
    
class QueryDetail(Resource):
    @jwt_required()
    def get(self, query_id):
        query = IssueQuery.query.get(query_id)
        if not query:
            return jsonify({"message": "Query not found"}), 404

        student = User.query.get(query.user_id)
        student_name = student.name if student else "Unknown Student"

        return jsonify({
            "id": query.id,
            "query_text": query.details,
            "student_name": student_name,
            "timestamp": query.created_at
        })

class SolveQuery(Resource):
    @jwt_required()
    def post(self, query_id):
        admin_id = get_jwt_identity()
        admin = User.query.get(admin_id)

        if not admin or admin.role.name.lower() != "admin":
            return jsonify({"message": "Unauthorized! Only admins can solve queries."}), 403

        query = IssueQuery.query.get(query_id)
        if not query:
            return jsonify({"message": "Query not found"}), 404

        data = request.get_json()
        answer = data.get("answer")

        if not answer:
            return jsonify({"message": "Answer is required"}), 400

        try:
            solved_issue = SolveIssue(
                answer=answer,
                issue_id=query_id,
                solver_id=admin_id
            )
            db.session.add(solved_issue)
            db.session.commit()

            return jsonify({
                "message": "Query solved successfully!",
                "query_id": query_id,
                "solver_id": admin_id,
                "answer": answer,
                "timestamp": solved_issue.created_at
            }), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"message": "Error solving query", "error": str(e)}), 500
        
class AddCourse(Resource):
    @jwt_required()
    def post(self):
        admin_id = get_jwt_identity()
        admin = User.query.get(admin_id)

        if not admin or admin.role.lower() != "admin":
            return jsonify({"message": "Unauthorized! Only admins can add courses."}), 403

        data = request.get_json()
        name = data.get("name")
        description = data.get("description")

        if not name or not description:
            return jsonify({"message": "Course name and description are required."}), 400

        try:
            new_course = Course(name=name, description=description)
            db.session.add(new_course)
            db.session.commit()

            return jsonify({  "message": "Course added successfully!"}), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"message": "Error adding course", "error": str(e)}), 500
        

class EditCourse(Resource):
    @jwt_required()
    def put(self, course_id):
        admin_id = get_jwt_identity()
        admin = User.query.get(admin_id)

        if not admin or admin.role.lower() != "admin":
            return jsonify({"message": "Unauthorized! Only admins can edit courses."}), 403

        course = Course.query.get(course_id)
        if not course:
            return jsonify({"message": "Course not found."}), 404

        data = request.get_json()
        course.name = data.get("name", course.name)
        course.description = data.get("description", course.description)

        try:
            db.session.commit()
            return jsonify({   "message": "Course updated successfully!"})
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"message": "Error updating course", "error": str(e)}), 500

class AddCourseMaterial(Resource):
    @jwt_required()
    def post(self, course_id):
        admin_id = get_jwt_identity()
        admin = User.query.get(admin_id)

        if not admin or admin.role.lower() != "admin":
            return jsonify({"message": "Unauthorized! Only admins can add course materials."}), 403

        course = Course.query.get(course_id)
        if not course:
            return jsonify({"message": "Course not found."}), 404

        data = request.get_json()
        title = data.get("title")
        material_link = data.get("material_link")

        if not title or not material_link:
            return jsonify({"message": "Title and material link are required."}), 400

        try:
            new_material = CourseMaterial(title=title, material_link=material_link, course_id=course_id)
            db.session.add(new_material)
            db.session.commit()

            return jsonify({ "message": "Course material added successfully!",}), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"message": "Error adding course material", "error": str(e)}), 500
        
class EditCourseMaterial(Resource):
    @jwt_required()
    def put(self, material_id):
        admin_id = get_jwt_identity()
        admin = User.query.get(admin_id)

        if not admin or admin.role.lower() != "admin":
            return jsonify({"message": "Unauthorized! Only admins can edit course materials."}), 403

        material = CourseMaterial.query.get(material_id)
        if not material:
            return jsonify({"message": "Course material not found."}), 404

        data = request.get_json()
        material.title = data.get("title", material.title)
        material.material_link = data.get("material_link", material.material_link)

        try:
            db.session.commit()
            return jsonify({    "message": "Course material updated successfully!",})
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"message": "Error updating course material", "error": str(e)}), 500
        
