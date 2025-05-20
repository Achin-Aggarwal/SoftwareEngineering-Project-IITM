import pytest
import json
from app import create_app  # Assume this creates the Flask app with API routes
from flask import jsonify
from unittest.mock import patch

@pytest.fixture
def app():
    app = create_app()  # assuming create_app() is your app factory function
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_student_plan_post_success(client):
    """Test StudentPlan POST request when data is valid."""
    with patch('app.get_academic_year_data') as mock_get_data, \
         patch('app.analyze_student_queries') as mock_analyze, \
         patch('app.generate_academic_plan_for_student') as mock_generate_plan:
        
        # Mocking the functions
        mock_get_data.return_value = mock_data = {'student_id': [1, 2, 3], 'other_data': [1, 2, 3]}
        mock_analyze.return_value = ({1: {'analysis': 'student1'}}, {'course1': 'analysis'})
        mock_generate_plan.return_value = "Sample Academic Plan"
        
        response = client.post('/student_plan/1', json={'start_date': '2023-01-01'})
        assert response.status_code == 200
        assert 'Content-Disposition' in response.headers

def test_student_plan_post_student_not_found(client):
    """Test when student is not found."""
    with patch('app.get_academic_year_data') as mock_get_data:
        mock_get_data.return_value = {'student_id': [2, 3]}  # Mocking different student IDs
        
        response = client.post('/student_plan/1', json={'start_date': '2023-01-01'})
        assert response.status_code == 404
        assert response.json['error'] == 'Student 1 not found.'

def test_course_plan_post_success(client):
    """Test CoursePlan POST request when data is valid."""
    with patch('app.get_academic_year_data') as mock_get_data, \
         patch('app.analyze_student_queries') as mock_analyze, \
         patch('app.generate_course_improvement_plan') as mock_generate_plan:
        
        # Mocking the functions
        mock_get_data.return_value = mock_data = {'course': ['course1', 'course2'], 'other_data': [1, 2]}
        mock_analyze.return_value = ({}, {'course1': 'analysis'})
        mock_generate_plan.return_value = "Sample Course Plan"
        
        response = client.post('/course_plan/course1', json={'start_date': '2023-01-01'})
        assert response.status_code == 200
        assert 'Content-Disposition' in response.headers

def test_course_plan_post_course_not_found(client):
    """Test when course is not found."""
    with patch('app.get_academic_year_data') as mock_get_data:
        mock_get_data.return_value = {'course': ['course2']}  # Mocking different course name
        
        response = client.post('/course_plan/course1', json={'start_date': '2023-01-01'})
        assert response.status_code == 404
        assert response.json['error'] == 'Course course1 not found in the data.'

def test_visualizations_get_success(client):
    """Test Visualizations GET request when data is valid."""
    with patch('app.get_academic_year_data') as mock_get_data, \
         patch('app.analyze_student_queries') as mock_analyze, \
         patch('app.generate_visualizations') as mock_generate_visualizations:
        
        mock_get_data.return_value = {'some_data': 'mock'}
        mock_analyze.return_value = ({}, {})
        mock_generate_visualizations.return_value = '/path/to/visualization.png'

        response = client.get('/visualizations?start_date=2023-01-01')
        assert response.status_code == 200
        assert 'Content-Disposition' in response.headers

def test_visualizations_get_no_data(client):
    """Test Visualizations GET request when no data is found."""
    with patch('app.get_academic_year_data') as mock_get_data:
        mock_get_data.return_value = {}  # Simulate no data
        
        response = client.get('/visualizations?start_date=2023-01-01')
        assert response.status_code == 404
        assert response.json['error'] == "No data found for the specified time period."

def test_bulk_student_plans_post_success(client):
    """Test BulkStudentPlans POST request when data is valid."""
    with patch('app.get_academic_year_data') as mock_get_data, \
         patch('app.analyze_student_queries') as mock_analyze, \
         patch('app.generate_academic_plan_for_student') as mock_generate_plan, \
         patch('app.send_file') as mock_send_file:
        
        # Mocking the functions
        mock_get_data.return_value = {'student_id': [1, 2, 3], 'other_data': [1, 2, 3]}
        mock_analyze.return_value = ({1: {'analysis': 'student1'}}, {'course1': 'analysis'})
        mock_generate_plan.return_value = "Sample Academic Plan"
        mock_send_file.return_value = 'mock_file_path.zip'
        
        response = client.post('/bulk_student_plans', json={'start_date': '2023-01-01'})
        assert response.status_code == 200
        assert 'Content-Disposition' in response.headers
        assert 'bulk_academic_plans' in response.json['data']

def test_bulk_student_plans_post_no_data(client):
    """Test BulkStudentPlans POST request when no data is found."""
    with patch('app.get_academic_year_data') as mock_get_data:
        mock_get_data.return_value = {}  # Simulating no data
        
        response = client.post('/bulk_student_plans', json={'start_date': '2023-01-01'})
        assert response.status_code_


