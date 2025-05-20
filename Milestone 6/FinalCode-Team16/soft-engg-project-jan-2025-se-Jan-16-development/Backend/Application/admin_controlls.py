from flask_restful import Resource
from flask import request , jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity,get_jwt
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime,timedelta
from . import db
from sqlalchemy import func

from .model import User,IssueQuery,Course,CourseMaterial,UserCourse,Role,LiveSession,SupplementaryMaterial,Assignment

class StatsResource(Resource):
    def get(self):
        # Get role IDs
        student_role = db.session.query(Role.id).filter_by(name='Student').scalar()
        professor_role = db.session.query(Role.id).filter_by(name='Professor').scalar()
        instructor_role = db.session.query(Role.id).filter_by(name='Instructor').scalar()
        
        # Count users by role
        num_students = db.session.query(User).filter_by(role_id=student_role).count() if student_role else 0
        num_professors = db.session.query(User).filter_by(role_id=professor_role).count() if professor_role else 0
        num_instructors = db.session.query(User).filter_by(role_id=instructor_role).count() if instructor_role else 0
        
        # Count courses and related materials
        num_courses = db.session.query(Course).count()
        num_course_materials = db.session.query(CourseMaterial).count()
        num_live_sessions = db.session.query(LiveSession).count()
        num_supplementary_materials = db.session.query(SupplementaryMaterial).count()
        num_assignments = db.session.query(Assignment).count()
        num_queries = db.session.query(IssueQuery).count()
        
        stats = {
            "students": num_students,
            "professors": num_professors,
            "instructors": num_instructors,
            "courses": num_courses,
            "course_materials": num_course_materials,
            "live_sessions": num_live_sessions,
            "supplementary_materials": num_supplementary_materials,
            "assignments": num_assignments,
            "queries": num_queries
        }
        return jsonify(stats)
    

class AdminDetails(Resource):
    @jwt_required()
    def get(self):
        jwt_claims = get_jwt()
        admin_id = jwt_claims.get("id")
        admin = User.query.get(admin_id)

        if not admin or admin.role.name.lower() != "admin":
            return jsonify({"message": "Unauthorized! Only admins can access this."}), 403

        return jsonify({
            "id": admin.id,
            "name": admin.name,
            "username": admin.username,
            "email": admin.email,
            "role": admin.role.name,
            "created_at": admin.created_at,
            "last_login": admin.last_login
        })

class GetAllCourses(Resource):
    @jwt_required()
    def get(self):
        courses = Course.query.all()
        course_list = [{
            "id": course.id,
            "name": course.name,
            "description": course.description,
            "created_at": course.created_at,
            "total_materials": len(course.materials),
            "total_assignments": len(course.assignments),
            "total_students": len(course.enrolled_users)
        } for course in courses]

        return jsonify({"courses": course_list})
    
class GetAllStudents(Resource):
    @jwt_required()
    def get(self):
        jwt_claims = get_jwt()
        admin_id = jwt_claims.get("id")
        admin = User.query.get(admin_id)

        if not admin or admin.role.name.lower() != "admin":
            return jsonify({"message": "Unauthorized! Only admins can access this."}), 403

        students = User.query.filter(User.role.has(name="Student")).all()
        student_list = [{
            "id": student.id,
            "name": student.name,
            "username": student.username,
            "email": student.email,
            "created_at": student.created_at,
            "total_courses": len(student.courses)
        } for student in students]

        return jsonify({"students": student_list})

class UserResource(Resource):
    def get(self):
        students = (
            db.session.query(User.id, User.name)
            .join(Role)
            .filter(Role.name == "Student")
            .all()
        )
        
        return jsonify([{"id": user.id, "name": user.name} for user in students])


# class TopSupportQueries(Resource):
#     @jwt_required()
#     def get(self):
#         # Get date 7 days ago
#         last_week = datetime.utcnow() - timedelta(days=7)

#         # Fetch top 5 most asked queries in the past 7 days
#         queries = (
#             db.session.query(ChatbotHistory.query, db.func.count(ChatbotHistory.id).label("count"))
#             .filter(ChatbotHistory.timestamp >= last_week)
#             .group_by(ChatbotHistory.query)
#             .order_by(db.desc("count"))
#             .limit(5)
#             .all()
#         )

#         # Format response
#         query_list = [{"query": q.query, "count": q.count} for q in queries]

#         return jsonify({"top_queries": query_list})

class TopSupportQueries(Resource):
    @jwt_required()
    def get(self):
        last_week = datetime.now() - timedelta(days=7)

        # Fetch top 5 most frequent queries in the last 7 days
        top_queries = db.session.query(
            IssueQuery.details,
            func.count(IssueQuery.details).label("count")
        ).filter(
            IssueQuery.created_at >= last_week
        ).group_by(
            IssueQuery.details
        ).order_by(
            db.desc("count")
        ).limit(5).all()

        if not top_queries:
            return jsonify({"message": "No queries found"}), 404

        return jsonify([
            {
                "query_text": query.details,
                "count": query.count
            }
            for query in top_queries
        ])

    
# class QueryDetail(Resource):
#     @jwt_required()
#     def get(self, query_id):
#         query = IssueQuery.query.get(query_id)
#         if not query:
#             return jsonify({"message": "Query not found"}), 404

#         student = User.query.get(query.user_id)
#         student_name = student.name if student else "Unknown Student"

#         return jsonify({
#             "id": query.id,
#             "query_text": query.details,
#             "student_name": student_name,
#             "timestamp": query.created_at
#         })

# class SolveQuery(Resource):
#     @jwt_required()
#     def post(self, query_id):
#         jwt_claims = get_jwt()  
#         admin_id = jwt_claims.get("id") 
        
#         admin = User.query.get(admin_id)

#         if not admin or admin.role.name.lower() != "admin":
#             return jsonify({"message": "Unauthorized! Only admins can solve queries."}), 403

#         query = IssueQuery.query.get(query_id)
#         if not query:
#             return jsonify({"message": "Query not found"}), 404

#         data = request.get_json()
#         answer = data.get("answer")

#         if not answer:
#             return jsonify({"message": "Answer is required"}), 400

#         try:
#             solved_issue = SolveIssue(
#                 answer=answer,
#                 issue_id=query_id,
#                 solver_id=admin_id
#             )
#             db.session.add(solved_issue)
#             db.session.commit()

#             return jsonify({
#                 "message": "Query solved successfully!",
#                 "query_id": query_id,
#                 "solver_id": admin_id,
#                 "answer": answer,
#                 "timestamp": solved_issue.created_at
#             }), 201
#         except SQLAlchemyError as e:
#             db.session.rollback()
#             return jsonify({"message": "Error solving query", "error": str(e)}), 500
  
class AddCourse(Resource):
    @jwt_required()
    def post(self):
        jwt_claims = get_jwt()  
        admin_id = jwt_claims.get("id")
        admin = User.query.get(admin_id) 
        if not admin or admin.role.name.lower() != "admin":
            return jsonify({"message": "Unauthorized! Only admins can edit courses."}), 403
        
        data = request.get_json(silent=True)

        if not data:
            return {"message": "Invalid JSON data"}, 400

        name = data.get("name")
        description = data.get("description")

        if not isinstance(name, str) or not isinstance(description, str) or not name.strip() or not description.strip():
            return {"message": "Course name and description must be non-empty strings."}, 400

        try:
            new_course = Course(name=name.strip(), description=description.strip())
            db.session.add(new_course)
            db.session.commit()

            return {"message": "Course added successfully!"}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Error adding course", "error": str(e)}, 500


class EditCourse(Resource):
    @jwt_required()
    def put(self, course_id):
        jwt_claims = get_jwt()  
        admin_id = jwt_claims.get("id")
        admin = User.query.get(admin_id) 
        if not admin or admin.role.name.lower() != "admin":
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
        jwt_claims = get_jwt()  
        admin_id = jwt_claims.get("id")
        admin = User.query.get(admin_id) 
        if not admin or admin.role.name.lower() != "admin":
            return jsonify({"message": "Unauthorized! Only admins can edit courses."}), 403

        course = Course.query.get(course_id)
        if not course:
            return {"message": "Course not found."}

        data = request.get_json()
        week_number = data.get("week_number")
        title = data.get("title")
        material_link = data.get("material_link")

        if not title or not material_link:
            return {"message": "Title and material link are required."}

        try:
            new_material = CourseMaterial(week_number=week_number,title=title, video_link=material_link, course_id=course_id)
            db.session.add(new_material)
            db.session.commit()

            return { "message": "Course material added successfully!"}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Error adding course material"}
        
class EditCourseMaterial(Resource):
    @jwt_required()
    def put(self, material_id):
        jwt_claims = get_jwt()  
        admin_id = jwt_claims.get("id")
        admin = User.query.get(admin_id) 
        if not admin or admin.role.name.lower() != "admin":
            return jsonify({"message": "Unauthorized! Only admins can edit courses."}), 403

        material = CourseMaterial.query.get(material_id)
        if not material:
            return jsonify({"message": "Course material not found."}), 404

        data = request.get_json()
        # print(data)
        material.title = data.get("title", material.title)
        material.video_link = data.get("link", material.video_link)
       

        try:
            db.session.commit()
            return jsonify({    "message": "Course material updated successfully!",})
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"message": "Error updating course material", "error": str(e)}), 500
        
class AssignCourse(Resource):
    @jwt_required()
    def post(self, course_id, student_id):
        jwt_claims = get_jwt()  
        admin_id = jwt_claims.get("id")
        admin = User.query.get(admin_id) 
        if not admin or admin.role.name.lower() != "admin":
            return {"message": "Unauthorized! Only admins can edit courses."}, 403

        course = Course.query.get(course_id)
        student = User.query.get(student_id)

        if not course:
            return jsonify({"message": "Course not found."}), 404

        if not student:
            return jsonify({"message": "Student not found."}), 404

        existing_enrollment = UserCourse.query.filter_by(user_id=student_id, course_id=course_id).first()
        if existing_enrollment:
            return {"message": "Student is already enrolled in this course."}, 400

        try:
            # Create a new enrollment record
            enrollment = UserCourse(user_id=student_id, course_id=course_id)
            db.session.add(enrollment)
            db.session.commit()
            return {"message": "Course assigned successfully!"}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Error assigning course", "error": str(e)}, 500