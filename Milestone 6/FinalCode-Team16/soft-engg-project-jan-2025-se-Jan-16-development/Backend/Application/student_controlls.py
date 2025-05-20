from flask_restful import Resource
from flask import request , jsonify
from flask_jwt_extended import jwt_required, get_jwt
import os
import pandas as pd
from datetime import datetime
from . import db
import subprocess
from .model import User, Course, Assignment,CourseMaterial,UserCourse,ChatbotHistory,IssueQuery,LiveSession,SupplementaryMaterial,UserAssignmentScore

# class StudentProfile(Resource):
#     @jwt_required()
#     def get(self):
#         jwt_claims = get_jwt()
#         student_id = jwt_claims.get("id")
#         student = User.query.get(student_id)
        
#         if not student:
#             return jsonify({"message": "Student not found."}), 404
#         return jsonify({
#             "id": student.id,
#             "name": student.name,
#             "username": student.username,
#             "email": student.email,
#             "role": student.role.name,
#             "last_login": student.last_login
#         })

class StudentProfile(Resource):
    @jwt_required()
    def get(self):
        jwt_claims = get_jwt()
        student_id = jwt_claims.get("id")
        student = User.query.get(student_id)
        
        if not student:
            return jsonify({"message": "Student not found."}), 404
        
        # Fetch enrolled courses with assignment scores
        courses_data = []
        for user_course in student.courses:
            course = user_course.course
            assignments = []
            
            for assignment in course.assignments:
                score_entry = UserAssignmentScore.query.filter_by(
                    user_id=student.id, assignment_id=assignment.id
                ).first()
                score = score_entry.score if score_entry else None
                
                assignments.append({
                    "week_number": assignment.week_number,
                    "assignment_type": assignment.assignment_type,
                    "score": score
                })
            
            courses_data.append({
                "course_name": course.name,
                "assignments": assignments
            })
        
        return jsonify({
            "id": student.id,
            "name": student.name,
            "username": student.username,
            "email": student.email,
            "role": student.role.name,
            "last_login": student.last_login,
            "courses": courses_data
        })


class StudentDashboard(Resource):
    @jwt_required()
    def get(self):
        jwt_claims = get_jwt()
        student_id = jwt_claims.get("id")
        student = User.query.get(student_id)

        if not student:
            return jsonify({"message": "Student not found."}), 404

        # Fetch courses enrolled by the student
        enrolled_courses = UserCourse.query.filter_by(user_id=student_id).all()
        courses_data = []

        for enrollment in enrolled_courses:
            course = Course.query.get(enrollment.course_id)
            if course:
                # Fetch assignments for the course
                assignments = Assignment.query.filter_by(course_id=course.id).all()
                assignments_data = [
                    {
                        "id": assignment.id,
                        "week_number": assignment.week_number,
                        "created_at": assignment.created_at
                    }
                    for assignment in assignments
                ]

                # Fetch course materials for the course
                materials = CourseMaterial.query.filter_by(course_id=course.id).all()
                materials_data = [
                    {
                        "id": material.id,
                        "title": material.title,
                        "video_link": material.video_link,
                        "week_number": material.week_number,
                        "created_at": material.created_at
                    }
                    for material in materials
                ]

                # Fetch live sessions for the course
                live_sessions = LiveSession.query.filter_by(course_id=course.id).all()
                live_sessions_data = [
                    {
                        "id": session.id,
                        "yt_link": session.yt_link,
                        "description": session.description,
                        "created_at": session.created_at
                    }
                    for session in live_sessions
                ]

                # Fetch supplementary materials for the course
                supplementary_materials = SupplementaryMaterial.query.filter_by(course_id=course.id).all()
                supplementary_materials_data = [
                    {
                        "id": material.id,
                        "material_type": material.material_type,
                        "content": material.content,
                        "created_at": material.created_at
                    }
                    for material in supplementary_materials
                ]

                # Add course details with all related data
                courses_data.append({
                    "id": course.id,
                    "name": course.name,
                    "description": course.description,
                    "created_at": course.created_at,
                    "assignments": assignments_data,
                    "materials": materials_data,
                    "live_sessions": live_sessions_data,
                    "supplementary_materials": supplementary_materials_data
                })
        return jsonify({ 'courses_data': courses_data})
    

class CourseDetails(Resource):
    @jwt_required()
    def get(self, course_id):
        # Fetch course by ID
        course = Course.query.get(course_id)

        if not course:
            return {"message": "Course not found."}, 404

        # Fetch assignments for the course
        # assignments = Assignment.query.filter_by(course_id=course.id).all()
        assignments_data = []

        assignments = Assignment.query.filter_by(course_id=course.id, assignment_type='Assignment').all()
        for assignment in assignments:
            file_path = assignment.file

            if not file_path or not os.path.exists(file_path):
                return {"message": "File not found"}, 404

            try:
                df = pd.read_csv(file_path)

                # Ensure CSV contains necessary columns
                required_columns = {"Question", "Option A", "Option B", "Option C", "Option D", "Answer"}
                if not required_columns.issubset(df.columns):
                    return {"message": "CSV file is missing required columns"}, 400

                # Convert CSV data into structured questions
                questions = [
                    {
                        "text": row["Question"],
                        "options": [
                            {"text": row["Option A"]},
                            {"text": row["Option B"]},
                            {"text": row["Option C"]},
                            {"text": row["Option D"]}
                        ],
                        "correctAnswer": row["Answer"]
                    }
                    for _, row in df.iterrows()
                ]

                # Append structured assignment data
                assignments_data.append({
                    "id":assignment.id,
                    "name": assignment.assignment_type,
                    "weekNumber": assignment.week_number,
                    "questions": questions
                })

            except Exception as e:
                return {"message": f"An error occurred: {str(e)}"}, 500
            
        programming_assignments_data = []

        programming_assignments = Assignment.query.filter_by(course_id=course.id, assignment_type='Programing Assignment').all()
        
        # print(f"Found {len(programming_assignments)} programming assignments")
        for assignment in programming_assignments:
            file_path = assignment.file

            if not file_path or not os.path.exists(file_path):
                # print(file_path)
                return {"message": "File not found"}, 404

            try:
                df = pd.read_csv(file_path)
                # print(f"Processing: {file_path}")
                # print(df.head())

                # Ensure CSV contains necessary columns
                required_columns = {"Task Number", "Problem Statement", "Example Input", "Expected Output"}
                if not required_columns.issubset(df.columns):
                    return {"message": "CSV file is missing required columns"}, 400

                # Convert CSV data into structured programming assignments
                tasks = [
                    {
                        "problemStatement": row["Problem Statement"],
                        "exampleInput": row["Example Input"],
                        "expectedOutput": row["Expected Output"]
                    }
                    for _, row in df.iterrows()
                ]

                programming_assignments_data.append({
                    "id":assignment.id,
                    "name": assignment.assignment_type,
                    "weekNumber": assignment.week_number,
                    "tasks": tasks
                })

            except Exception as e:
                return {"message": f"An error occurred: {str(e)}"}, 500

        # Fetch course materials for the course
        materials = CourseMaterial.query.filter_by(course_id=course.id).all()
        materials_data = [
            {
                "id": material.id,
                "title": material.title,
                "video_link": material.video_link,
                "week_number": material.week_number,
                "created_at": material.created_at
            }
            for material in materials
        ]

        # Fetch live sessions for the course
        live_sessions = LiveSession.query.filter_by(course_id=course.id).all()
        live_sessions_data = [
            {
                "id": session.id,
                "yt_link": session.yt_link,
                "description": session.description,
                "created_at": session.created_at
            }
            for session in live_sessions
        ]

        # Fetch supplementary materials for the course
        supplementary_materials = SupplementaryMaterial.query.filter_by(course_id=course.id).all()
        supplementary_materials_data = [
            {
                "id": material.id,
                "material_type": material.material_type,
                "content": material.content,
                "created_at": material.created_at
            }
            for material in supplementary_materials
        ]

        # Construct response with course details
        course_data = {
            "id": course.id,
            "name": course.name,
            "description": course.description,
            "created_at": course.created_at,
            "assignments": assignments_data,
            "programming_assignments_data": programming_assignments_data,
            "materials": materials_data,
            "live_sessions": live_sessions_data,
            "supplementary_materials": supplementary_materials_data
        }

        return jsonify({"course_data": course_data})

class RunCode(Resource):
    def post(self):
        try:
            data = request.get_json()

            user_code = data.get("code", "").strip()
            test_cases = data.get("test_cases", [])

            # Validate test_cases format
            if not isinstance(test_cases, list):
                return jsonify({"error": "test_cases should be a list", "code": 400})
            
            if not all(isinstance(tc, dict) for tc in test_cases):
                return jsonify({"error": "Each test case should be a dictionary", "code": 400})
            
            if not all("input" in tc and "expected_output" in tc for tc in test_cases):
                return jsonify({"error": "Each test case must have 'input' and 'expected_output'", "code": 400})

            if not user_code:
                return jsonify({"error": "Missing code", "code": 400})

            temp_code_path = "temp_code.py"

            # Extract function name (assuming the user defines a function)
            function_name = user_code.split("(")[0].replace("def", "").strip()

            # Generate test case execution code
            test_code = "\n".join(
                [f'print({function_name}({tc["input"].strip()}))' for tc in test_cases]
            )

            full_code = f"{user_code}\n\n{test_code}"

            # Write user code + test cases to temp file
            with open(temp_code_path, "w") as f:
                f.write(full_code)

            # Execute the script
            process = subprocess.Popen(
                ["python3", temp_code_path],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            out, err = process.communicate(timeout=5)

            actual_outputs = out.strip().split("\n") if out.strip() else []
            errors = err.strip()

            # Match outputs with expected outputs
            test_results = []
            for i, test_case in enumerate(test_cases):
                expected_output = test_case.get("expected_output", "").strip()
                # print(expected_output)
                actual_output = actual_outputs[i] if i < len(actual_outputs) else ""

                test_results.append({
                    "input": test_case["input"],
                    "expected_output": expected_output,
                    "actual_output": actual_output,
                    "passed": actual_output == expected_output
                })

            # Cleanup: Remove temp file
            os.remove(temp_code_path)

            return jsonify({"test_results": test_results, "errors": errors, "code": 200})

        except KeyError as e:
            return jsonify({"error": f"Missing key: {str(e)}", "code": 400})
        except subprocess.TimeoutExpired:
            return jsonify({"error": "Execution timed out", "code": 500})
        except Exception as e:
            return jsonify({"error": str(e), "code": 500})
        

class SubmitCode(Resource):
    @jwt_required()
    def post(self):
        jwt_claims = get_jwt()
        user_id = jwt_claims.get("id")
        try:
            data = request.get_json()

            user_code = data.get("code", "").strip()
            test_cases = data.get("test_cases", [])
            assignment_id = data.get("assignment_id")

            # Validate input data
            if not isinstance(test_cases, list):
                return jsonify({"error": "test_cases should be a list", "code": 400})
            
            if not all(isinstance(tc, dict) for tc in test_cases):
                return jsonify({"error": "Each test case should be a dictionary", "code": 400})
            
            if not all("input" in tc and "expected_output" in tc for tc in test_cases):
                return jsonify({"error": "Each test case must have 'input' and 'expected_output'", "code": 400})

            if not user_code:
                return jsonify({"error": "Missing code", "code": 400})

            if not user_id or not assignment_id:
                return jsonify({"error": "Missing user_id or assignment_id", "code": 400})

            temp_code_path = "temp_code.py"

            # Extract function name (assuming the user defines a function)
            function_name = user_code.split("(")[0].replace("def", "").strip()

            # Generate test case execution code
            test_code = "\n".join(
                [f'print({function_name}({tc["input"].strip()}))' for tc in test_cases]
            )

            full_code = f"{user_code}\n\n{test_code}"

            # Write user code + test cases to temp file
            with open(temp_code_path, "w") as f:
                f.write(full_code)

            # Execute the script
            process = subprocess.Popen(
                ["python3", temp_code_path],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            out, err = process.communicate(timeout=5)

            actual_outputs = out.strip().split("\n") if out.strip() else []
            errors = err.strip()

            # Match outputs with expected outputs
            test_results = []
            all_passed = True
            for i, test_case in enumerate(test_cases):
                expected_output = test_case.get("expected_output", "").strip()
                actual_output = actual_outputs[i] if i < len(actual_outputs) else ""

                passed = actual_output == expected_output
                if not passed:
                    all_passed = False  # At least one test case failed

                test_results.append({
                    "input": test_case["input"],
                    "expected_output": expected_output,
                    "actual_output": actual_output,
                    "passed": passed
                })

            # Cleanup: Remove temp file
            os.remove(temp_code_path)

            # ✅ Update score if all test cases passed
            if all_passed:
                score_entry = UserAssignmentScore.query.filter_by(
                    user_id=user_id, assignment_id=assignment_id
                ).first()

                if score_entry:
                    score_entry.score = 10  # Update score to 10
                    score_entry.graded_at = datetime.utcnow()
                else:
                    new_score = UserAssignmentScore(
                        user_id=user_id,
                        assignment_id=assignment_id,
                        score=10
                    )
                    db.session.add(new_score)

                db.session.commit()

            return jsonify({
                "test_results": test_results,
                "errors": errors,
                "code": 200
            })

        except KeyError as e:
            return jsonify({"error": f"Missing key: {str(e)}", "code": 400})
        except subprocess.TimeoutExpired:
            return jsonify({"error": "Execution timed out", "code": 500})
        except Exception as e:
            return jsonify({"error": str(e), "code": 500})
        
class UpdateScore(Resource):
    @jwt_required() 
    def post(self):
        jwt_claims = get_jwt()
        user_id = jwt_claims.get("id")
        try:
            data = request.get_json()
            assignment_id = data.get("assignment_id")
            score = data.get("score")

            if not assignment_id or score is None:
                return jsonify({"error": "Missing assignment_id or score", "code": 400})

            # Check if the user already has a score for this assignment
            existing_score = UserAssignmentScore.query.filter_by(user_id=user_id, assignment_id=assignment_id).first()

            if existing_score:
                existing_score.score = score  # Update score
                existing_score.graded_at = datetime.utcnow()
            else:
                new_score = UserAssignmentScore(user_id=user_id, assignment_id=assignment_id, score=score)
                db.session.add(new_score)

            db.session.commit()

            return jsonify({"success": True, "message": "Score updated successfully", "code": 200})

        except Exception as e:
            return jsonify({"error": str(e), "code": 500})