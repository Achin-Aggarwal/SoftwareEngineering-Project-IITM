from flask_restful import Resource
from flask import request , jsonify
from flask_jwt_extended import create_access_token, create_refresh_token,decode_token,jwt_required,get_jwt_identity,get_jwt,verify_jwt_in_request
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash,generate_password_hash
from . import db
from .model import User, Role,InstructorRequest,RequestStatus
from functools import wraps

# def role_required(required_role):
#     def wrapper(fn):
#         @wraps(fn)
#         def decorator(*args, **kwargs):
#             verify_jwt_in_request()  # Ensure JWT is present
#             claims = get_jwt()  # Get claims after verifying JWT
#             user_identity = get_jwt_identity()

#             print("role_required called!")
#             print("JWT Identity:", user_identity)
#             print("JWT Claims:", claims)

#             if claims.get("role") != required_role:
#                 return jsonify({"message": "Unauthorized, incorrect role"}), 403

#             return fn(*args, **kwargs)
#         return decorator
#     return wrapper

def generate_token(user_role, user_id, user_username):
    return create_access_token(identity=user_role, additional_claims={'role': user_role,'id':user_id, 'username': user_username})

def generate_refresh_token(user_id, user_role, user_username):
    return create_refresh_token(identity=user_role, additional_claims={'role': user_role,'id':user_id, 'username': user_username}, expires_delta=timedelta(days=30))

class RefreshToken(Resource):
    @jwt_required()
    def post(self):
        jwt_claims = get_jwt()
        user_id = jwt_claims.get("id")
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        return jsonify({'access_token': generate_token(user.role.name,user.id, user.username)})
    


# Login API for Admin, Student, and Instructor
class Login(Resource):
    def post(self):
        data = request.json
        login_identifier = data.get("username")
        password = data.get("password")

        user = User.query.filter((User.email == login_identifier) | (User.username == login_identifier)).first()

        if not user or not check_password_hash(user.password, password):
            return jsonify({'message': 'Invalid credentials'})

        # Check role-specific conditions
        if user.role.name == 'Instructor':
            # Ensure instructor is approved before login
            request_entry = InstructorRequest.query.filter_by(instructor_id=user.id, status=RequestStatus.APPROVED).first()
            if not request_entry:
                return jsonify({'message': 'Instructor approval pending'})

        # Update last login timestamp
        user.last_login = datetime.now()
        db.session.commit()

        # Generate tokens
        access_token = generate_token(user.role.name,user.id, user.username)
        refresh_token = generate_refresh_token(user.id, user.role.name, user.username)

        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'username': user.username,
            # 'role': user.role.name,
            'message': 'Successfully logged in.'
        })



class Signup(Resource):
    def post(self):
        data = request.json

        # Extract common fields
        name = data.get("name")
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        about = data.get("about", "")
        role_name = data.get("role")  # Role should be "Student" or "Instructor"

        username = email.split("@")[0]

        # Validate required fields
        if not all([name, email, password, role_name]):
            return jsonify({"message": "All fields are required."})

        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            return jsonify({"message": "Username already exists."})
        if User.query.filter_by(email=email).first():
            return jsonify({"message": "Email already exists."})

        # Validate role
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            return jsonify({"message": f"Role '{role_name}' not found in database."})

        # Hash password
        hashed_password = generate_password_hash(password)

        # Create user
        new_user = User(
            name=name,
            username=username,
            email=email,
            password=hashed_password,
            about=about,
            role_id=role.id,
            created_at=datetime.utcnow(),
            last_login=None
        )

        db.session.add(new_user)
        db.session.commit()

        # If Instructor, create a pending approval request
        if role_name == "Instructor":
            instructor_request = InstructorRequest(professor_id=2, instructor_id=new_user.id, status=RequestStatus.PENDING)
            db.session.add(instructor_request)
            db.session.commit()
            return jsonify({"message": "Instructor signup successful, pending approval."})

        return jsonify({"message": f"{role_name} registered successfully!"})
    


# class AdminLogin(Resource):
#     def post(self):
#         data = request.json
#         login_identifier = data.get("username")
#         password = data.get("password")
        
#         user = User.query.filter((User.email == login_identifier) | (User.username == login_identifier)).first()
        
#         if user and check_password_hash(user.password, password) and user.role.name == 'Admin':
#             user.last_login = datetime.now()
#             db.session.commit()
#             access_token = generate_token(user.id, user.role.name, user.username)
#             refresh_token = generate_refresh_token(user.id, user.role.name, user.username)
#             return jsonify({'access_token': access_token, 'refresh_token': refresh_token, 'username': user.username})
#         return jsonify({'message': 'Invalid credentials'})
    
# class OtherLogin(Resource):
#     def post(self):
#         data = request.json
#         login_identifier = data.get("username")
#         password = data.get("password")
        
#         user = User.query.filter((User.email == login_identifier) | (User.username == login_identifier)).first()
        
#         if user and check_password_hash(user.password, password) and user.role.name in ['Student'] :
#             user.last_login = datetime.now()
#             db.session.commit()
#             access_token = generate_token(user.id, user.role.name, user.username)
#             refresh_token = generate_refresh_token(user.id, user.role.name, user.username)
#             return jsonify({'access_token': access_token, 'refresh_token': refresh_token, 'username': user.username, 'message': 'Successfully logged in.'})
        
#         return jsonify({'message': 'Invalid credentials'})

# class StudentSignup(Resource):
#     def post(self):
#         data = request.json

#         # Extracting required fields
#         name = data.get("name")
#         username = data.get("username")
#         email = data.get("email")
#         password = data.get("password")

#         # Validation checks
#         if not all([name, username, email, password]):
#             return jsonify({"message": "All fields are required."})

#         # Check if username or email already exists
#         if User.query.filter_by(username=username).first():
#             return jsonify({"message": "Username already exists."})
#         if User.query.filter_by(email=email).first():
#             return jsonify({"message": "Email already exists."})

#         # Get or create Student role
#         student_role = Role.query.filter_by(name="Student").first()
#         if not student_role:
#             return jsonify({"message": "Student role not found in database."})

#         # Hash the password
#         hashed_password = generate_password_hash(password)

#         # Create a new student user
#         new_student = User(
#             name=name,
#             username=username,
#             email=email,
#             password=hashed_password,
#             role_id=student_role.id
#         )

#         # Save user to database
#         db.session.add(new_student)
#         db.session.commit()
        
#         return jsonify({ "message": "Student registered successfully!"})
    



# class InstructorSignup(Resource):
#     def post(self):
#         """ Instructor signs up (Initially in 'Pending' state) """
#         data = request.get_json()
        
#         # Check for required fields
#         required_fields = ["name", "username", "email", "password", "role_id"]
#         if not all(field in data for field in required_fields):
#             return {"message": "Missing required fields"}, 400

#         if User.query.filter_by(username=data["username"]).first():
#             return {"message": "Username already taken"}, 400
#         if User.query.filter_by(email=data["email"]).first():
#             return {"message": "Email already registered"}, 400

#         hashed_password = generate_password_hash(data["password"])

#         new_user = User(
#             name=data["name"],
#             username=data["username"],
#             email=data["email"],
#             password=hashed_password,
#             role_id=data["role_id"]  # Should be instructor role_id
#         )

#         db.session.add(new_user)
#         db.session.commit()

#         return {"message": "Instructor signup successful, pending approval"}, 201
    
    
class Logout(Resource):
    @jwt_required()
    def post(self):
        try:
            return jsonify({"message": "Logout successful"})
        except Exception as e:
            return jsonify({"error": str(e)})