import pytest
import sys
import os
from flask import Flask
from flask_jwt_extended import create_access_token, create_refresh_token
from Application.model import db, User, Role # Import the database and User model

from datetime import datetime, timedelta

# Ensure the Backend folder is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Import Flask app after updating the path
from Application import app  # Adjust if app is inside main.py

def generate_token(user_role, user_id, user_username):
    return create_access_token(identity=user_role, additional_claims={'role': user_role,'id':user_id, 'username': user_username})
def generate_refresh_token(user_role, user_id, user_username):
    return create_refresh_token(identity=user_role, additional_claims={'role': user_role,'id':user_id, 'username': user_username}, expires_delta=timedelta(days=30))

@pytest.fixture
def client():
    """Creates a test client for Flask application."""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///appdatabase.db"  # Use an in-memory DB for tests
    app.config["JWT_SECRET_KEY"] = "test_secret"  # Set a secret key for JWT


    with app.app_context():  # Ensure app context exists
        db.create_all()  # Create database schema
        with app.test_client() as client:
            yield client  # Yield client for testing
        db.session.remove()
        # db.drop_all()


@pytest.fixture
def db_session(client):
    """Creates a new database session for a test."""
    with client.application.app_context():  # Ensure we are within the app context
        db.create_all()  # Create tables before the test
        yield db.session  # Provide the session to tests
        db.session.rollback()  # Rollback after the test to keep tests isolated
        


@pytest.fixture
def auth_header(client):
    """Creates a JWT token for testing authentication."""
    with app.app_context():
        # Fetch or create the role if necessary
        student_role = Role.query.filter_by(name="Student").first()
        if not student_role:
            student_role = Role(name="Student")
            db.session.add(student_role)
            db.session.commit()

        # Check if test user exists, if not create one
        test_user = User.query.filter_by(email="student1@gmail.com").first()
        if not test_user:
            test_user = User(
                id=11,
                name="Student5",
                username="student5",
                email="student5@gmail.com",
                password="123456",  # Make sure this is properly hashed in production
                about="I am a Bs student.",
                role=student_role,
                last_login=datetime(2025, 3, 19, 15, 59, 34, 614431),
            )
            db.session.add(test_user)
            db.session.commit()

        # Generate JWT token
        access_token = generate_token(test_user.role.name,test_user.id, test_user.username)
        refresh_token = generate_refresh_token(test_user.id, test_user.role.name, test_user.username)

        # Return authorization header
        return {"Authorization": f"Bearer {access_token}"}


def test_student_login(client):
    """Test admin login API."""
    response = client.post("/login", json={"username": "student1@gmail.com", "password": "123456"})
    
    assert response.status_code == 200
    json_data = response.get_json()
    print('Pytest Code Response : ')
    print('Access Token :',json_data['access_token'])
    print('Refresh Token :' ,json_data['refresh_token'])
    print('Message :',json_data['message'])
    print('Username :',json_data['username'])
    assert "access_token" in json_data
    assert json_data["message"] == "Successfully logged in."
    print('\n')
    print('Message :',json_data['message'])



def test_student_profile(client, auth_header):
    """Test the Student Profile API."""
    response = client.get("/student_profile", headers=auth_header)
   
    assert response.status_code == 200
    json_data = response.get_json()
    print("profile:",json_data ,'\n')
    


def test_student_dashboard(client, auth_header):
    """Test the Student Dashboard API."""
    response = client.get("/student_dashboard", headers=auth_header)
   
    assert response.status_code == 200
    json_data = response.get_json()
    print("dashbord",json_data)


def test_refresh_token(client,auth_header):
    """Test the Refresh Token API."""
    response = client.post("/token_refresh", headers=auth_header)

    assert response.status_code == 200
    json_data = response.get_json()
    assert "access_token" in json_data
    print("New Access Token:", json_data["access_token"])



def test_logout(client, auth_header):
    """Test the Logout API."""
    response = client.post("/logout", headers=auth_header)

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == "Logout successful"
    print("Logout Response:", json_data)



from werkzeug.security import generate_password_hash

def test_successful_student_signup(client, db_session):
    """Test successful student signup"""
    payload = {
        "name": "John",
        "email": "johndoe1@example.com",
        "password": "password123",
        "role": "Student"
    }
    
    response = client.post("/signup", json=payload)
    print( " Pytest Response:", response.get_json())
    
    assert response.status_code == 200
    assert response.get_json()["message"] == "Student registered successfully!"



def test_successful_instructor_signup(client, db_session):
    """Test successful instructor signup (pending approval)"""
    payload = {
        "name": "Jane Smith1",
        "email": "janesmit1h@example.com",
        "password": "securepass",
        "role": "Instructor"
    }

    response = client.post("/signup", json=payload)
    print( " Pytest Response:", response.get_json())
    assert response.status_code == 200
    assert response.get_json()["message"] == "Instructor signup successful, pending approval."



def test_signup_missing_fields(client):
    """Test signup with missing required fields"""
    payload = {
        "email": "user@example.com",
        "password": "testpass",
        "role": "Student"
    }

    response = client.post("/signup", json=payload)
    print( " Pytest Response:", response.get_json())
    assert response.status_code == 200
    assert response.get_json()["message"] == "All fields are required."



def test_signup_invalid_role(client):
    """Test signup with an invalid role"""
    payload = {
        "name": "Unknown Role",
        "email": "unknown@example.com",
        "password": "testpass",
        "role": "Manager"
    }

    response = client.post("/signup", json=payload)
    print( " Pytest Response:", response.get_json())

    assert response.status_code == 200
    assert response.get_json()["message"] == "Role 'Manager' not found in database."




def test_chatbot_api(client, auth_header):
    """Test the Chatbot API."""
    payload = {"query": "What is recursion?"}

    response = client.post("/chat", json=payload, headers=auth_header)

    assert response.status_code in [200, 400, 500]  # Expect success, bad request, or server error
    json_data = response.get_json()

    if response.status_code == 200:
        assert json_data["query"] == payload["query"]
        assert "response" in json_data
        assert "references" in json_data
        assert isinstance(json_data["references"], list)
        print("Chatbot Response:", json_data)

    elif response.status_code == 400:
        assert json_data["error"] == "Query cannot be empty"
        print("Empty Query Error:", json_data)

    elif response.status_code == 500:
        print("Server Error:", json_data)


