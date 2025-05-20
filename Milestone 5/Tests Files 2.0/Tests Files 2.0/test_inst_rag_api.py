import pytest
from flask import Flask
from flask.testing import FlaskClient
from your_module import StrugglingTopics, WeeklyAnalysis
from unittest.mock import patch, MagicMock
import pandas as pd
from io import StringIO


@pytest.fixture
def client() -> FlaskClient:
    app = Flask(__name__)
    app.add_url_rule('/struggling_topics', view_func=StrugglingTopics.as_view('struggling_topics'))
    app.add_url_rule('/weekly_analysis', view_func=WeeklyAnalysis.as_view('weekly_analysis'))
    
    # Use the test client for making API requests
    return app.test_client()


@pytest.fixture
def mock_get_queries_by_timeframe():
    with patch.object(WeeklyAnalysis, 'get_queries_by_timeframe', return_value=pd.DataFrame({
        'student_id': [1, 2, 3],
        'query': ['how to code', 'struggling with code', 'error in python'],
        'resource_guide': ['guide1', 'guide2', 'guide3'],
        'timestamp': ['2025-03-30 10:00:00', '2025-03-29 11:00:00', '2025-03-28 12:00:00'],
    })) as mock_method:
        yield mock_method


@pytest.fixture
def mock_llm_invoke():
    with patch('your_module.llm.invoke') as mock_method:
        yield mock_method


# Test for StrugglingTopics API
def test_struggling_topics(client, mock_get_queries_by_timeframe, mock_llm_invoke):
    mock_llm_invoke.return_value.content = "Top struggling topics analysis"
    
    # Make a GET request with custom query parameter
    response = client.get('/struggling_topics?days=30')
    
    # Assert the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert response JSON contains expected keys
    data = response.get_json()
    assert 'analysis_period' in data
    assert 'top_struggling_topics' in data
    
    # Assert the top_struggling_topics contains analysis response
    assert data['top_struggling_topics'] == "Top struggling topics analysis"


# Test for WeeklyAnalysis API
def test_weekly_analysis(client, mock_get_queries_by_timeframe):
    # Make a GET request for weekly analysis with default days (7)
    response = client.get('/weekly_analysis?days=7')
    
    # Assert the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert response JSON contains expected keys
    data = response.get_json()
    assert 'status' in data
    assert data['status'] == "success"
    assert 'message' in data
    assert 'report_content' in data
    
    # Check the report content for the expected format
    report_content = data['report_content']
    assert 'total_queries' in report_content
    assert 'unique_students' in report_content
    assert 'queries_per_student' in report_content


# Test for error handling in WeeklyAnalysis API
def test_weekly_analysis_error(client, mock_get_queries_by_timeframe):
    # Mocking the method to raise an exception
    with patch.object(WeeklyAnalysis, 'analyze_weekly_query_patterns', side_effect=Exception("Database error")):
        response = client.get('/weekly_analysis?days=7')
        
    # Assert the response status code is 500 for server error
    assert response.status_code == 500
    data = response.get_json()
    assert data['status'] == "error"
    assert 'message' in data
    assert "Database error" in data['message']


if __name__ == '__main__':
    pytest.main()
