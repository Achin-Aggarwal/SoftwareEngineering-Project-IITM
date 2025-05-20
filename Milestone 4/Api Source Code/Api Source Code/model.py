from . import db
from datetime import datetime
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum

# Role
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    users = db.relationship('User', backref='role', lazy=True, cascade="all, delete")

# User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    about = db.Column(db.Text, nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    last_login = db.Column(db.DateTime(timezone=True), nullable=True)

    courses = db.relationship('UserCourse', backref='user', lazy=True, cascade="all, delete")
    queries = db.relationship('IssueQuery', backref='user', lazy=True)
    solutions = db.relationship('SolveIssue', backref='solver', lazy=True)
    chatbot_history = db.relationship('ChatbotHistory', backref='user', lazy=True, cascade="all, delete")
    instructor_requests_sent = db.relationship('InstructorRequest', foreign_keys='InstructorRequest.professor_id', backref='professor', lazy=True, cascade="all, delete")
    instructor_requests_received = db.relationship('InstructorRequest', foreign_keys='InstructorRequest.instructor_id', backref='instructor', lazy=True, cascade="all, delete")
    assignments = db.relationship('UserAssignment', backref='user', lazy=True, cascade="all, delete")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.username}>"

# Enum for InstructorRequest Status
class RequestStatus(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"

# Instructor Request
class InstructorRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    status = db.Column(db.Enum(RequestStatus), default=RequestStatus.PENDING, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

# Course
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    materials = db.relationship('CourseMaterial', backref='course', lazy=True, cascade="all, delete")
    assignments = db.relationship('Assignment', backref='course', lazy=True, cascade="all, delete")
    enrolled_users = db.relationship('UserCourse', backref='course', lazy=True, cascade="all, delete")
    live_sessions = db.relationship('LiveSession', backref='course', lazy=True, cascade="all, delete")
    supplementary_materials = db.relationship('SupplementaryMaterial', backref='course', lazy=True, cascade="all, delete")

# Course Material
class CourseMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week_number = db.Column(db.Integer, nullable=False)
    video_link = db.Column(db.String(500), nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

# Assignment
class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week_number = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    users = db.relationship('UserAssignment', backref='assignment', lazy=True, cascade="all, delete")

# UserCourse
class UserCourse(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete="CASCADE"), primary_key=True)
    enrolled_at = db.Column(db.DateTime(timezone=True), default=func.now())

# UserAssignment
class UserAssignment(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id', ondelete="CASCADE"), primary_key=True)
    submitted_at = db.Column(db.DateTime(timezone=True), default=func.now())

class LiveSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete="CASCADE"), nullable=False)
    yt_link = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

#Supplementary Material 
class SupplementaryMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete="CASCADE"), nullable=False)
    material_type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

# Chatbot History
class ChatbotHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    query = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())

class IssueQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    details = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())


class SolveIssue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text, nullable=False)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue_query.id'), nullable=False)
    solver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

# Instructor Deletion Log
class InstructorDeletionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.Integer, nullable=False)
    deleted_by_admin_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="SET NULL"), nullable=True)
    deleted_at = db.Column(db.DateTime(timezone=True), default=func.now())
