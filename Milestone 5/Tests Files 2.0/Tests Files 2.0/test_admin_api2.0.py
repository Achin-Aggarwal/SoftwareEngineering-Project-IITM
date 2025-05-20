import pytest
from flask import Flask
from Application import app  # Adjust import based on your Flask app structure
from Application import db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///appdatabase.db"  # Use an in-memory DB for tests
    app.config["JWT_SECRET_KEY"] = "test_secret"  # Set a secret key for JWT


    with app.app_context():  # Ensure app context exists
        db.create_all()  # Create database schema
        with app.test_client() as client:
            yield client  # Yield client for testing
        db.session.remove()

@pytest.fixture
def auth_header(client):
    """Logs in as admin and returns authentication headers."""
    login_data = {
        "username": "admin@example.com",
        "password": "admin123"
    }

    response = client.post("/login", json=login_data)
    
    assert response.status_code == 200, "Login failed, check API response."
    
    json_data = response.get_json()
    access_token = json_data.get("access_token")

    return {"Authorization": f"Bearer {access_token}"}

def test_admin_login(client):
    """Test admin login API."""
    response = client.post("/login", json={"username": "admin@example.com", "password": "admin123"})
    
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


def test_login_invalid_password(client):
    """Test login with incorrect password."""
    response = client.post("/login", json={"username": "admin@example.com", "password": "wrongpassword"})
    
    assert response.status_code == 200  # Your API returns 200 even for invalid credentials
    json_data = response.get_json()
    print('Pytest Code Response:\n',json_data ,'\n')
    assert json_data["message"] == "Invalid credentials"


def test_login_nonexistent_user(client):
    """Test login with a non-existing username."""
    response = client.post("/login", json={"username": "nonexistent@example.com", "password": "admin123"})
    
    assert response.status_code == 200
    json_data = response.get_json()
    print('Pytest Code Response :\n',json_data ,'\n')
    assert json_data["message"] == "Invalid credentials"


def test_login_missing_username(client):
    """Test login with missing username."""
    response = client.post("/login", json={"password": "admin123"})
    
    assert response.status_code == 200
    json_data = response.get_json()
    print('Pytest Code Response :\n',json_data ,'\n')
    assert json_data["message"] == "Invalid credentials"



def test_login_empty_credentials(client):
    """Test login with empty credentials."""
    response = client.post("/login", json={})
    
    assert response.status_code == 200
    json_data = response.get_json()
    print('Pytest Code Response:\n',json_data ,'\n')
    assert json_data["message"] == "Invalid credentials"



def test_login_invalid_json(client):
    """Test login with invalid JSON format."""
    response = client.post("/login", data="invalid_json", content_type="application/json")
    
    assert response.status_code == 400  # Assuming Flask handles bad JSON format errors
    json_data = response.get_json()
    
    print('Pytest Code Response : \n',json_data ,'\n')
    assert "message" in json_data



def test_admin_details(client, auth_header):
    """Test fetching admin details API."""
    response = client.get("/admin_details", headers=auth_header)

    assert response.status_code == 200
    json_data = response.get_json()
    print('admin details:',json_data,'\n')

    assert json_data["username"] == "admin"
    assert json_data["email"] == "admin@example.com"
    assert json_data["role"].lower() == "admin"


def test_admin_details_unauthorized(client):
    """Test fetching admin details without authentication."""
    response = client.get("/admin_details")  # No auth header provided
    
    assert response.status_code == 401  # Expected: Unauthorized
    json_data = response.get_json()
    print("Pytest Code Response :",json_data)
    assert "msg" in json_data  # Typical Flask-JWT error response
    assert json_data["msg"] == "Missing Authorization Header"


def test_admin_details_invalid_token(client):
    """Test fetching admin details with an invalid token."""
    response = client.get("/admin_details", headers={"Authorization": "Bearer invalid_token"})
    
    assert response.status_code == 422  # Expected: Unauthorized
    json_data = response.get_json()
    print("Pytest Code Response :", json_data)





def test_get_all_courses(client, auth_header):
    """Test fetching all courses API."""
    response = client.get("/admin_courses", headers=auth_header)

    assert response.status_code == 200
    json_data = response.get_json()
    print("Pytest Code Response :", json_data,'\n')

    assert "courses" in json_data
    assert isinstance(json_data["courses"], list)




def test_get_all_students(client, auth_header):
    """Test fetching all students API (admin access only)."""
    response = client.get("/admin_students", headers=auth_header)

    assert response.status_code == 200
    json_data = response.get_json()
    print("Students:", json_data,'\n')

    assert "students" in json_data
    assert isinstance(json_data["students"], list)



def test_add_course(client, auth_header):
    """Test adding a new course."""
    response = client.post("/add_course", json={"name": "Python 101", "description": "Intro to Python"}, headers=auth_header)
    print("Pytest Response :",response.get_json(),'\n')
    assert response.status_code == 201
    assert response.get_json()["message"] == "Course added successfully!"



def test_edit_course(client, auth_header):
    """Test editing an existing course."""
    response = client.put("/edit_course/6", json={"name": "Advanced Python Hack"}, headers=auth_header)
    print("Pytest response :",response.get_json(),'\n')
    
    assert response.status_code == 200
    assert response.get_json()["message"] == "Course updated successfully!"



def test_add_course_material(client, auth_header):
    response = client.post("/add_course/5/material", json={"week_number": 2, "title": "Introduction", "material_link": "http://example.com/video1"}, headers=auth_header)
    print("Pytest response:",response.get_json(),'\n')
    
    assert response.status_code == 200
    assert response.get_json()["message"] == "Course material added successfully!"



def test_edit_course_material(client, auth_header):
    """Test editing course material."""
    client.post("/edit_course/material/6", json={"week_number": 1, "title": "Introduction", "material_link": "http://example.com/video1"}, headers=auth_header)
    response = client.put("/edit_course_material/1", json={"title": "Updated Title"}, headers=auth_header)
    
    assert response.status_code == 200
    assert response.get_json()["message"] == "Course material updated successfully!"

def test_assign_course_success(client, auth_header):
    
    # Assign the course to a student
    response = client.post("/assign_course/6/2", headers=auth_header)
    print("pytest response:", response.get_json())
    assert response.status_code == 200
    assert response.get_json()["message"] == "Course assigned successfully!"

def test_stats_success(client, auth_header):
    """Test retrieving statistics with valid authentication."""
    response = client.get("/stats", headers=auth_header)
    
    assert response.status_code == 200
    json_data = response.get_json()
    
    assert "students" in json_data
    assert "professors" in json_data
    assert "instructors" in json_data
    assert "courses" in json_data
    assert "course_materials" in json_data
    assert "live_sessions" in json_data
    assert "supplementary_materials" in json_data
    assert "assignments" in json_data
    assert "queries" in json_data
    
    # You could also assert that counts are non-negative, assuming 0 or more records exist
    assert json_data["students"] >= 0
    assert json_data["professors"] >= 0
    assert json_data["instructors"] >= 0
    assert json_data["courses"] >= 0
    assert json_data["course_materials"] >= 0
    assert json_data["live_sessions"] >= 0
    assert json_data["supplementary_materials"] >= 0
    assert json_data["assignments"] >= 0
    assert json_data["queries"] >= 0

def test_stats_no_data(client, auth_header, mocker):
    """Test retrieving statistics when no data is present."""
    # Mocking the db queries to return no data
    mocker.patch("Application.db.session.query", return_value=0)
    
    response = client.get("/stats", headers=auth_header)
    
    assert response.status_code == 200
    json_data = response.get_json()
    
    # Expect all counts to be 0
    assert json_data["students"] == 0
    assert json_data["professors"] == 0
    assert json_data["instructors"] == 0
    assert json_data["courses"] == 0
    assert json_data["course_materials"] == 0
    assert json_data["live_sessions"] == 0
    assert json_data["supplementary_materials"] == 0
    assert json_data["assignments"] == 0
    assert json_data["queries"] == 0

def test_stats_partial_data(client, auth_header, mocker):
    """Test retrieving statistics when some entities are missing."""
    # Mocking the db queries to return data for some entities and 0 for others
    mocker.patch("Application.db.session.query", return_value=5)  # Mock all to return 5 for simplicity
    
    # Return specific values for each query
    mocker.patch("Application.db.session.query(User).filter_by(role_id=1).count", return_value=10)  # Students = 10
    mocker.patch("Application.db.session.query(User).filter_by(role_id=2).count", return_value=0)  # Professors = 0
    mocker.patch("Application.db.session.query(User).filter_by(role_id=3).count", return_value=3)  # Instructors = 3
    mocker.patch("Application.db.session.query(Course).count", return_value=5)
    mocker.patch("Application.db.session.query(CourseMaterial).count", return_value=4)
    mocker.patch("Application.db.session.query(LiveSession).count", return_value=2)
    mocker.patch("Application.db.session.query(SupplementaryMaterial).count", return_value=7)
    mocker.patch("Application.db.session.query(Assignment).count", return_value=3)
    mocker.patch("Application.db.session.query(IssueQuery).count", return_value=1)
    
    response = client.get("/stats", headers=auth_header)
    
    assert response.status_code == 200
    json_data = response.get_json()
    
    # Assert expected data
    assert json_data["students"] == 10
    assert json_data["professors"] == 0
    assert json_data["instructors"] == 3
    assert json_data["courses"] == 5
    assert json_data["course_materials"] == 4
    assert json_data["live_sessions"] == 2
    assert json_data["supplementary_materials"] == 7
    assert json_data["assignments"] == 3
    assert json_data["queries"] == 1

def test_stats_unauthorized(client):
    """Test retrieving statistics without authentication."""
    response = client.get("/stats")
    
    assert response.status_code == 401  # Unauthorized
    json_data = response.get_json()
    assert "msg" in json_data
    assert json_data["msg"] == "Missing Authorization Header"


