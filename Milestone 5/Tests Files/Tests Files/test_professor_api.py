import pytest
import sys
import os
from flask import Flask
from flask_jwt_extended import create_access_token
from Application.model import db, User, Role # Import the database and User model
from datetime import datetime


# Ensure the Backend folder is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Import Flask app after updating the path
from Application import app  # Adjust if app is inside main.py

def generate_token(user_role, user_id, user_username):
    return create_access_token(identity=user_role, additional_claims={'role': user_role,'id':user_id, 'username': user_username})

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
        test_user = User.query.filter_by(email="professor1@gmail.com").first()
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

        # Return authorization header
        return {"Authorization": f"Bearer {access_token}"}

def test_professor_details(client, auth_header):
    """Test fetching admin details API."""
    response = client.get("/professor_details", headers=auth_header)

    assert response.status_code == 200
    json_data = response.get_json()
    print('Pytest Response:',json_data,'\n')

def test_pending_instructors(client, auth_header):
    """Test the Pending Instructors API."""
    response = client.get("/pending_instructor", headers=auth_header)

    assert response.status_code in [200, 404]  # Either success or professor not found
    json_data = response.get_json()

    if response.status_code == 200:
        assert isinstance(json_data, list)  # The response should be a list
        if json_data:  # If there are pending instructors
            for req in json_data:
                assert "id" in req
                assert "instructor_id" in req
                assert "status" in req
                assert "created_at" in req
        print("Pending Instructors:", json_data)
    else:
        assert json_data["message"] == "Professor not found"
        print("Professor Not Found:", json_data)


def test_professor_login(client):
    """Test admin login API."""
    response = client.post("/login", json={"username": "professor1@gmail.com", "password": "123456"})
    
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

def test_approve_instructor(client, auth_header):
    """Test the Approve Instructor API."""
    payload = {"status": "Approved"}  # Change to "Rejected" to test rejection flow
    response = client.put(f"/approve_instructor/6", json=payload, headers=auth_header)

    assert response.status_code in [200, 400, 404]  # Expect success, bad request, or not found
    json_data = response.get_json()

    if response.status_code == 200:
        assert "message" in json_data
        assert json_data["message"] in [f"Instructor request approved successfully",
                                        f"Instructor request rejected successfully"]
        print("Approve Instructor Response:", json_data)

    elif response.status_code == 400:
        assert json_data["message"] == "Invalid status, use 'Approved' or 'Rejected'"
        print("Invalid Status Error:", json_data)

    elif response.status_code == 404:
        assert json_data["message"] in ["Professor not found", "Instructor request not found"]
        print("Not Found Error:", json_data)


def test_add_lesson(client, auth_header):
    """Test the Add Lesson API."""
    payload = {
        "course_id": 1,  # Replace with a valid course_id from your test database
        "material_type": "Video",  # Example material type
        "content": "https://example.com/lesson.mp4"  # Example content (URL or text)
    }
    
    response = client.post("/add_suplementary", json=payload, headers=auth_header)

    assert response.status_code in [201, 400]  # Expect success or bad request
    json_data = response.get_json()

    if response.status_code == 201:
        assert json_data["message"] == "Lesson added successfully"
        print("Lesson Added Successfully:", json_data)

    elif response.status_code == 400:
        assert json_data["message"] == "Missing required fields"
        print("Missing Fields Error:", json_data)


