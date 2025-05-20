from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
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


from .student_controlls import StudentProfile,StudentDashboard

api.add_resource(StudentProfile,'/student_profile')
api.add_resource(StudentDashboard,'/student_dashboard')

from .admin_controlls import TopSupportQueries ,QueryDetail,SolveQuery,AddCourse,EditCourse,AddCourseMaterial,EditCourseMaterial

api.add_resource(TopSupportQueries,'/topquery')
api.add_resource(QueryDetail, '/query_detail/<int:query_id>')
api.add_resource(SolveQuery, '/solve_query/<int:query_id>')

# Course Management Endpoints
api.add_resource(AddCourse, '/add_course')
api.add_resource(EditCourse, '/edit_course/<int:course_id>')
api.add_resource(AddCourseMaterial, '/add_course/<int:course_id>/material')
api.add_resource(EditCourseMaterial, '/edit_course/material/<int:material_id>')

from .professor_conrolls import PendingInstructors,ApproveInstructor,SolvedIssues,PendingIssues

api.add_resource(PendingInstructors,'/pensing_instructor')
api.add_resource(ApproveInstructor,'/approve_instructor')
api.add_resource(SolvedIssues, "/solved_issues")
api.add_resource(PendingIssues, "/pending_issues")

from .instructor_controlls import LessonResource,AssignmentResource,LiveSessionResource

api.add_resource(LessonResource,'/add_suplementary')
api.add_resource(AssignmentResource,'/add_assigments')
api.add_resource(LiveSessionResource,'/add_livesession')

from .rag_chat import ChatbotAPI
api.add_resource(ChatbotAPI, "/chat")




# print("Registered routes:")
# for rule in app.url_map.iter_rules():
#     print(rule)