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
        test_user = User.query.filter_by(email="int5@gmail.com").first()
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
    


def test_inst_login(client):
    """Test admin login API."""
    response = client.post("/login", json={"username": "int5@gmail.com", "password": "123456"})
    
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


def test_inst_details(client, auth_header):
    """Test fetching admin details API."""
    response = client.get("/instructor_details", headers=auth_header)

    assert response.status_code == 200
    json_data = response.get_json()
    print('Pytest Response:',json_data,'\n')


def test_top_support_queries(client, auth_header):
    """Test the Top Support Queries API."""
    response = client.get("/topquery", headers=auth_header)

    assert response.status_code in [200, 404]  # Expect success or no queries found
    json_data = response.get_json()

    if response.status_code == 200:
        assert isinstance(json_data, list)  # The response should be a list of queries
        assert all("query_text" in query and "count" in query for query in json_data)
        print("Top Support Queries Response:", json_data)

    elif response.status_code == 404:
        assert json_data["message"] == "No queries found"
        print("No Queries Found:", json_data)


def test_add_live_session(client, auth_header):
    """Test the Add Live Session API."""
    payload = {
        "course_id": 1,
        "yt_link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "description": "Live session on Python Basics"
    }

    response = client.post("/add_livesession", json=payload, headers=auth_header)

    assert response.status_code in [201, 400]  # Expect success or missing fields error
    json_data = response.get_json()

    if response.status_code == 201:
        assert json_data["message"] == "Live session added successfully"
        print("Live Session Added:", json_data)

    elif response.status_code == 400:
        assert json_data["message"] == "Missing required fields"
        print("Missing Fields Error:", json_data)



