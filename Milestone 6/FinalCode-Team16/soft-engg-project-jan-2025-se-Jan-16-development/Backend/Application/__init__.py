from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager,get_jwt_identity
from flask_cors import CORS




app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config["SECRET_KEY"] = "Anish_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 


db = SQLAlchemy(app) 
# db = SQLAlchemy()
api = Api(app)
jwt = JWTManager(app)
from . import model




with app.app_context():
    db.create_all()

from .auth import Login ,RefreshToken,Signup,Logout
api.add_resource(Login, '/login')
api.add_resource(RefreshToken, '/token_refresh')

api.add_resource(Signup, '/signup')

api.add_resource(Logout, '/logout')


from .student_controlls import StudentProfile,StudentDashboard,CourseDetails,RunCode,SubmitCode,UpdateScore

api.add_resource(StudentProfile,'/student_profile')
api.add_resource(StudentDashboard,'/student_dashboard')
api.add_resource(CourseDetails, "/course/<int:course_id>")
api.add_resource(RunCode, "/run_code")
api.add_resource(SubmitCode, "/submit_code")
api.add_resource(UpdateScore, "/submit_score")

from .admin_controlls import TopSupportQueries ,AddCourse,EditCourse,AddCourseMaterial,EditCourseMaterial,AssignCourse,AdminDetails,GetAllCourses,GetAllStudents,UserResource,StatsResource
api.add_resource(UserResource, '/students')
api.add_resource(AdminDetails, "/admin_details")
api.add_resource(GetAllCourses, "/admin_courses")
api.add_resource(GetAllStudents, "/admin_students")
api.add_resource(TopSupportQueries,'/topquery')
# api.add_resource(QueryDetail, '/query_detail/<int:query_id>')
# api.add_resource(SolveQuery, '/solve_query/<int:query_id>')
api.add_resource(AssignCourse, '/assign-course/<int:course_id>/<int:student_id>')
api.add_resource(StatsResource, '/api/stats')

# Course Management Endpoints
api.add_resource(AddCourse, '/add_course')
api.add_resource(EditCourse, '/edit_course/<int:course_id>')
api.add_resource(AddCourseMaterial, '/add_course/<int:course_id>/material')
api.add_resource(EditCourseMaterial, '/edit_course/material/<int:material_id>')

from .professor_conrolls import PendingInstructors,ApproveInstructor,LessonResource,ProfessorDetails
api.add_resource(ProfessorDetails, "/professor_details")
api.add_resource(PendingInstructors,'/pending_instructor')
api.add_resource(ApproveInstructor,'/approve_instructor/<int:request_id>')
api.add_resource(LessonResource,'/add_suplementary')


from .instructor_controlls import AssignmentResource,LiveSessionResource,InstructorDetails,CourseListResource
api.add_resource(InstructorDetails, "/instructor_details")
api.add_resource(AssignmentResource,'/add_assigments')
api.add_resource(LiveSessionResource,'/add_livesession')
api.add_resource(CourseListResource, '/courses')

from .rag_chat import ChatbotAPI,ProgramingChatbotAPI
api.add_resource(ChatbotAPI, "/chat")
api.add_resource(ProgramingChatbotAPI, "/pchat")


from .admin_rag import Data,Students,Courses,StudentPlan,CoursePlan,Visualizations,SummaryReport,BulkStudentPlans,BulkCoursePlans,FileDownload,VisualizationDownload
api.add_resource(Data, '/api/data')
api.add_resource(Students, '/api/students')
api.add_resource(Courses, '/api/courses')
api.add_resource(StudentPlan, '/api/student/<string:student_id>/academic-plan')
api.add_resource(CoursePlan, '/api/course/<string:course_name>/improvement-plan')
api.add_resource(Visualizations, '/api/visualizations')
api.add_resource(SummaryReport, '/api/summary-report')
api.add_resource(BulkStudentPlans, '/api/bulk/student-plans')
api.add_resource(BulkCoursePlans, '/api/bulk/course-plans')
api.add_resource(FileDownload, '/api/files/<path:filename>')
api.add_resource(VisualizationDownload, '/api/visualizations/<path:filename>')

from .inst_rag import WeeklyAnalysis,StrugglingTopics
api.add_resource(WeeklyAnalysis, "/api/weekly-analysis")
api.add_resource(StrugglingTopics, '/api/struggling-topics')


# print("Registered routes:")
# for rule in app.url_map.iter_rules():
#     print(rule)