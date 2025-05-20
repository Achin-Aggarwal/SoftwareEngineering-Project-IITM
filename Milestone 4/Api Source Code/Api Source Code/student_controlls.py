from flask_restful import Resource
from flask import request , jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from datetime import datetime
from . import db
from .model import User, Course, Assignment,CourseMaterial,UserCourse,ChatbotHistory,IssueQuery

class StudentProfile(Resource):
    @jwt_required()
    def get(self):
        student_id = get_jwt_identity()
        student = User.query.get(student_id)
        if not student:
            return jsonify({"message": "Student not found."}), 404
        return jsonify({
            "id": student.id,
            "name": student.name,
            "username": student.username,
            "email": student.email,
            "role": student.role.name,
            "last_login": student.last_login
        })

class StudentDashboard(Resource):
    @jwt_required()
    def get(self):
        student_id = get_jwt_identity()
        student = User.query.get(student_id)

        if not student:
            return jsonify({"message": "Student not found."}), 404

        # Fetch courses enrolled by the student
        enrolled_courses = UserCourse.query.filter_by(user_id=student_id).all()
        courses_data = []
        for enrollment in enrolled_courses:
            course = Course.query.get(enrollment.course_id)
            if course:
                # Fetch assignments related to this course
                assignments = Assignment.query.filter_by(course_id=course.id).all()
                assignments_data = [
                    {
                        "id": assignment.id,
                        "week_number": assignment.week_number,
                        "created_at": assignment.created_at
                    }
                    for assignment in assignments
                ]

                # Fetch course materials for this course
                materials = CourseMaterial.query.filter_by(course_id=course.id).all()
                materials_data = [
                    {
                        "id": material.id,
                        "title": material.title,
                        "file_url": material.file_url,
                        "uploaded_at": material.uploaded_at
                    }
                    for material in materials
                ]

                courses_data.append({
                    "id": course.id,
                    "name": course.name,
                    "description": course.description,
                    "created_at": course.created_at,
                    "assignments": assignments_data,
                    "materials": materials_data
                })

        # Fetch student's chatbot history
        chatbot_history = ChatbotHistory.query.filter_by(user_id=student_id).all()
        chatbot_data = [
            {
                "query": chat.query,
                "response": chat.response,
                "timestamp": chat.timestamp
            }
            for chat in chatbot_history
        ]

        # Fetch student's queries
        issue_queries = IssueQuery.query.filter_by(user_id=student_id).all()
        queries_data = [
            {
                "id": query.id,
                "details": query.details,
                "created_at": query.created_at
            }
            for query in issue_queries
        ]

        return jsonify({
            
            "courses": courses_data,
            "chatbot_history": chatbot_data,
            "queries": queries_data
        })
    
