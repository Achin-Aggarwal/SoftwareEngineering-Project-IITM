

from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt
import os
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from collections import Counter
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, send_file, send_from_directory
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import json
import uuid
import time

# Load environment variables
load_dotenv()




# Paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sqlite_db_path = os.path.join(current_dir, "chatbot_data.db")
output_dir = os.path.join(current_dir, "academic_plans")
viz_dir = os.path.join(output_dir, "visualizations")

# Create output directories if they don't exist
for directory in [output_dir, viz_dir]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Initialize GenAI model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.3,
    max_tokens=1024,
    top_p=0.9
)

def get_academic_year_data(start_date=None):
    """
    Retrieve query data for the last academic year.
    If start_date is not provided, it defaults to one year ago from today.
    """
    conn = sqlite3.connect(sqlite_db_path)
    
    if start_date is None:
        # Default to one year ago
        one_year_ago = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        query = f"""
        SELECT student_id, query, hint, example_code, resource_guide, timestamp
        FROM query_responses
        WHERE timestamp >= '{one_year_ago}'
        """
    else:
        query = f"""
        SELECT student_id, query, hint, example_code, resource_guide, timestamp
        FROM query_responses
        WHERE timestamp >= '{start_date}'
        """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df

def extract_course_from_resource_guide(resource_guide):
    """Extract course/subject information from resource guide text."""
    if pd.isna(resource_guide) or not resource_guide:
        return "Unknown"
    
    # Try to find subject/course information in the resource guide
    if "Subject:" in resource_guide:
        parts = resource_guide.split("Subject:")
        if len(parts) > 1:
            course = parts[1].split()[0].strip()
            return course
    
    # Check for common patterns like "Check [Subject]"
    if "Check" in resource_guide:
        parts = resource_guide.split("Check")
        if len(parts) > 1:
            course = parts[1].split()[0].strip()
            if course.endswith(','):
                course = course[:-1]
            return course
    
    return "Unknown"

def analyze_student_queries(df):
    """
    Analyze student queries to identify common topics, 
    challenging areas, and study patterns.
    """
    analysis = {}
    
    # Group by student
    student_groups = df.groupby('student_id')
    
    # Extract courses from resource guides
    df['course'] = df['resource_guide'].apply(extract_course_from_resource_guide)
    course_groups = df.groupby('course')
    
    # Create student-specific analysis
    for student_id, student_data in student_groups:
        # Count most common topics for this student
        topics = Counter()
        for query in student_data['query']:
            # Simple topic extraction - split query and count significant words
            words = [w.lower() for w in query.split() if len(w) > 4]
            topics.update(words)
        
        # Get timestamp data to analyze study patterns
        timestamps = pd.to_datetime(student_data['timestamp'])
        
        # Store analysis for this student
        analysis[student_id] = {
            'total_queries': len(student_data),
            'common_topics': dict(topics.most_common(10)),
            'earliest_query': timestamps.min().strftime('%Y-%m-%d'),
            'latest_query': timestamps.max().strftime('%Y-%m-%d'),
            'courses': student_data['course'].unique().tolist()
        }
    
    # Create course-specific analysis
    course_analysis = {}
    for course, course_data in course_groups:
        if course == "Unknown":
            continue
            
        # Count common topics for this course
        topics = Counter()
        for query in course_data['query']:
            words = [w.lower() for w in query.split() if len(w) > 4]
            topics.update(words)
            
        course_analysis[course] = {
            'total_queries': len(course_data),
            'students': course_data['student_id'].nunique(),
            'common_topics': dict(topics.most_common(10)),
        }
    
    return analysis, course_analysis

def generate_academic_plan_for_student(student_id, student_analysis, course_analysis):
    """
    Generate personalized academic plan for a student based on their query patterns.
    """
    # Extract relevant data for this student
    topics = student_analysis['common_topics']
    courses = student_analysis['courses']
    
    # Prepare context for AI
    context = f"""
    Student ID: {student_id}
    
    Query Analysis:
    - Total queries: {student_analysis['total_queries']}
    - Common topics: {', '.join([f'{topic} ({count})' for topic, count in topics.items()])}
    - Courses taken: {', '.join(courses)}
    
    Course-specific data:
    """
    
    for course in courses:
        if course in course_analysis:
            context += f"""
            {course}:
            - Most common topics across all students: {', '.join([f'{topic} ({count})' for topic, count in course_analysis[course]['common_topics'].items()][:5])}
            - Total queries from all students: {course_analysis[course]['total_queries']}
            """
    
    # System prompt for academic plan generation
    system_prompt = """You are an educational advisor tasked with creating personalized academic plans. 
    Analyze the provided student query data to:
    
    1. Identify knowledge gaps and areas where the student needs more support
    2. Recommend specific study resources and activities
    3. Suggest a weekly schedule that addresses their specific learning needs
    4. Provide tailored advice on how to improve understanding of difficult topics
    
    Be specific and practical. Format your response as a complete academic plan with clear sections.
    """
    
    # Generate the academic plan using AI
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"""
        Based on the following student data, create a personalized academic plan:
        
        {context}
        
        Create a comprehensive academic plan divided into these sections:
        1. Areas for Improvement (based on frequent queries)
        2. Recommended Resources
        3. Weekly Study Schedule
        4. Additional Support Recommendations
        """)
    ]
    
    response = llm.invoke(messages)
    return response.content

def generate_course_improvement_plan(course, course_data, all_data):
    """
    Generate suggestions for improving a course based on student queries.
    """
    # Prepare context for AI
    topics = course_data['common_topics']
    
    # Get some example queries for this course
    course_queries = all_data[all_data['course'] == course]['query'].tolist()
    example_queries = course_queries[:5] if len(course_queries) >= 5 else course_queries
    
    context = f"""
    Course: {course}
    
    Analysis:
    - Total queries: {course_data['total_queries']}
    - Number of students: {course_data['students']}
    - Common topics: {', '.join([f'{topic} ({count})' for topic, count in topics.items()])}
    
    Example student queries:
    {chr(10).join(['- ' + query for query in example_queries])}
    """
    
    # System prompt for course improvement
    system_prompt = """You are an educational curriculum advisor tasked with improving course materials.
    Analyze the provided query data to:
    
    1. Identify gaps in the current course materials based on frequent student queries
    2. Suggest specific improvements to address these gaps
    3. Recommend additional resources or content that should be created
    4. Suggest changes to the order or presentation of topics
    
    Be specific and actionable in your recommendations.
    """
    
    # Generate the course improvement plan using AI
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"""
        Based on the following course query data, create an improvement plan:
        
        {context}
        
        Create a comprehensive course improvement plan divided into these sections:
        1. Identified Gaps in Current Materials
        2. Suggested Content Improvements
        3. Recommended Additional Resources
        4. Proposed Structural Changes
        """)
    ]
    
    response = llm.invoke(messages)
    return response.content

def generate_visualizations(df, analysis, course_analysis):
    """Generate visualizations of the query data."""
    # Create unique file names based on timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    file_paths = {}
    
    # 1. Query volume over time
    plt.figure(figsize=(12, 6))
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    query_counts = df.groupby('date').size()
    query_counts.plot(kind='line')
    plt.title('Query Volume Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Queries')
    filename = f'query_volume_time_{timestamp}.png'
    filepath = os.path.join(viz_dir, filename)
    plt.savefig(filepath)
    plt.close()
    file_paths['query_volume'] = filename
    
    # 2. Queries by course
    plt.figure(figsize=(12, 6))
    course_counts = df['course'].value_counts()
    course_counts.plot(kind='bar')
    plt.title('Queries by Course')
    plt.xlabel('Course')
    plt.ylabel('Number of Queries')
    plt.xticks(rotation=45)
    plt.tight_layout()
    filename = f'queries_by_course_{timestamp}.png'
    filepath = os.path.join(viz_dir, filename)
    plt.savefig(filepath)
    plt.close()
    file_paths['queries_by_course'] = filename
    
    # 3. Student activity levels
    plt.figure(figsize=(12, 6))
    student_counts = df['student_id'].value_counts().head(20)  # Top 20 students
    student_counts.plot(kind='bar')
    plt.title('Query Counts for Most Active Students')
    plt.xlabel('Student ID')
    plt.ylabel('Number of Queries')
    plt.xticks(rotation=90)
    plt.tight_layout()
    filename = f'student_activity_{timestamp}.png'
    filepath = os.path.join(viz_dir, filename)
    plt.savefig(filepath)
    plt.close()
    file_paths['student_activity'] = filename
    
    return file_paths

def generate_summary_report(df, student_analysis, course_analysis, start_date):
    """Generate a summary report of the analysis."""
    summary = {
        "generated_on": datetime.now().strftime('%Y-%m-%d'),
        "analysis_period": {
            "start_date": start_date,
            "end_date": datetime.now().strftime('%Y-%m-%d')
        },
        "overview": {
            "total_queries": len(df),
            "total_students": df['student_id'].nunique(),
            "total_courses": df['course'].nunique()
        },
        "most_active_students": df['student_id'].value_counts().head(10).to_dict(),
        "most_queried_courses": df['course'].value_counts().head(10).to_dict()
    }
    
    # Common topics across all queries
    all_words = []
    for query in df['query']:
        words = [w.lower() for w in query.split() if len(w) > 4]
        all_words.extend(words)
    
    summary["common_topics"] = dict(Counter(all_words).most_common(15))
    
    return summary

class Data(Resource):
    def get(self):
        start_date = request.args.get('start_date', (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'))
        try:
            df = get_academic_year_data(start_date)
            if df.empty:
                return {"error": "No data found."}, 404
            student_analysis, course_analysis = analyze_student_queries(df)
            return {"status": "success", "data": {"query_count": len(df), "student_count": df['student_id'].nunique(), "course_count": df['course'].nunique(), "start_date": start_date, "end_date": datetime.now().strftime('%Y-%m-%d')}}
        except Exception as e:
            return {"error": str(e)}, 500

class Students(Resource):
    def get(self):
        start_date = request.args.get('start_date', None)
        try:
            df = get_academic_year_data(start_date)
            if df.empty:
                return {"error": "No data found."}, 404
            student_analysis, _ = analyze_student_queries(df)
            students = [{"id": sid, "total_queries": data['total_queries'], "courses": data['courses'], "earliest_query": data['earliest_query'], "latest_query": data['latest_query']} for sid, data in student_analysis.items()]
            return {"status": "success", "data": students}
        except Exception as e:
            return {"error": str(e)}, 500

class Courses(Resource):
    def get(self):
        start_date = request.args.get('start_date', None)
        try:
            df = get_academic_year_data(start_date)
            if df.empty:
                return {"error": "No data found."}, 404
            _, course_analysis = analyze_student_queries(df)
            courses = [{"name": cname, "total_queries": data['total_queries'], "student_count": data['students'], "common_topics": data['common_topics']} for cname, data in course_analysis.items()]
            return {"status": "success", "data": courses}
        except Exception as e:
            return {"error": str(e)}, 500


# class StudentPlan(Resource):
#     def post(self, student_id):
#         start_date = request.json.get('start_date', None) if request.is_json else None
#         try:
#             df = get_academic_year_data(start_date)
#             if df.empty or student_id not in df['student_id'].unique():
#                 return {"error": f"Student {student_id} not found."}, 404
#
#             student_analysis, course_analysis = analyze_student_queries(df)
#             plan = generate_academic_plan_for_student(student_id, student_analysis[student_id], course_analysis)
#
#             # Ensure 'files' directory exists
#             folder = os.path.join(os.getcwd(), "files")
#             os.makedirs(folder, exist_ok=True)
#
#             # Create the file
#             filename = f"academic_plan_{student_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
#             filepath = os.path.join(folder, filename)
#
#             with open(filepath, 'w') as f:
#                 f.write(plan)
#
#             # Ensure file is fully written before sending
#             time.sleep(0.5)  # Small delay to prevent race condition
#
#             # Check if file exists
#             if not os.path.exists(filepath):
#                 return {"error": f"File {filepath} not found after creation."}, 500
#
#             # Return file
#             return send_file(filepath, as_attachment=True)
#
#         except Exception as e:
#             import traceback
#             print(traceback.format_exc())  # Logs full error details
#             return {"error": str(e)}, 500



class StudentPlan(Resource):
    def post(self, student_id):
        start_date = request.json.get('start_date', None) if request.is_json else None
        try:
            df = get_academic_year_data(start_date)
            if df.empty or student_id not in df['student_id'].unique():
                return {"error": f"Student {student_id} not found."}, 404
            student_analysis, course_analysis = analyze_student_queries(df)
            plan = generate_academic_plan_for_student(student_id, student_analysis[student_id], course_analysis)
            filename = f"academic_plan_{student_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
            with open(filename, 'w') as f:
                f.write(plan)
            return {"status": "success", "data": {"student_id": student_id, "plan": plan, "file_path": filename}}
        except Exception as e:
            return {"error": str(e)}, 500

# class CoursePlan(Resource):
#     def post(self, course_name):
#         start_date = request.json.get('start_date', None) if request.is_json else None
#         try:
#             df = get_academic_year_data(start_date)
#             if df.empty or course_name not in df['course'].unique():
#                 return {"error": f"Course {course_name} not found."}, 404
#             _, course_analysis = analyze_student_queries(df)
#             plan = generate_course_improvement_plan(course_name, course_analysis[course_name], df)
#             filename = f"course_improvement_{course_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
#             with open(filename, 'w') as f:
#                 f.write(plan)
#             return {"status": "success", "data": {"course_name": course_name, "plan": plan, "file_path": filename}}
#         except Exception as e:
#             return {"error": str(e)}, 500


class CoursePlan(Resource):
    def post(self, course_name):
        """API endpoint to generate an improvement plan for a specific course."""
        start_date = request.json.get('start_date', None) if request.is_json else None
        
        try:
            df = get_academic_year_data(start_date)
            
            if df.empty:
                return jsonify({"error": "No data found for the specified time period."}), 404
            
            _, course_analysis = analyze_student_queries(df)
            
            if course_name not in course_analysis:
                return jsonify({"error": f"Course {course_name} not found in the data."}), 404
            
            # Generate the course improvement plan
            plan = generate_course_improvement_plan(course_name, course_analysis[course_name], df)
            
            # Save the plan
            filename = f"course_improvement_{course_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
            file_path = os.path.join(output_dir, filename)
            
            with open(file_path, 'w') as f:
                f.write(f"# Improvement Plan for Course: {course_name}\n\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d')}\n\n")
                f.write(plan)
            
            return {
                "status": "success",
                "data": {
                    "course_name": course_name,
                    "plan": plan,
                    "file_path": filename
                }
            }, 200
        except Exception as e:
            return {"error": str(e)}, 500
        


class Visualizations(Resource):
    def get(self):
        start_date = request.args.get('start_date', None)
        
        try:
            df = get_academic_year_data(start_date)
            if len(df) == 0:
                return {"error": "No data found for the specified time period."}, 404
            
            student_analysis, course_analysis = analyze_student_queries(df)
            file_paths = generate_visualizations(df, student_analysis, course_analysis)
            
            return {"status": "success", "data": {"visualizations": file_paths}}
        except Exception as e:
            return {"error": str(e)}, 500

class SummaryReport(Resource):
    def get(self):
        start_date = request.args.get('start_date', (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'))
        
        try:
            df = get_academic_year_data(start_date)
            if len(df) == 0:
                return {"error": "No data found for the specified time period."}, 404
            
            student_analysis, course_analysis = analyze_student_queries(df)
            summary = generate_summary_report(df, student_analysis, course_analysis, start_date)
            
            report_id = str(uuid.uuid4())[:8]
            filename = f"summary_report_{report_id}.md"
            file_path = os.path.join(output_dir, filename)
            
            with open(file_path, 'w') as f:
                f.write(f"# Academic Planning Summary Report\n\n")
                f.write(f"Generated on: {summary['generated_on']}\n\n")
                f.write(f"Analysis period: {summary['analysis_period']['start_date']} to {summary['analysis_period']['end_date']}\n\n")
                f.write("## Overview\n\n")
                f.write(f"- Total queries analyzed: {summary['overview']['total_queries']}\n")
                f.write(f"- Total students: {summary['overview']['total_students']}\n")
                f.write(f"- Total courses identified: {summary['overview']['total_courses']}\n\n")
            
            return {"status": "success", "data": {"summary": summary, "file_path": filename}}
        except Exception as e:
            return {"error": str(e)}, 500

class BulkStudentPlans(Resource):
    def post(self):
        start_date = request.json.get('start_date', None) if request.is_json else None
        
        try:
            df = get_academic_year_data(start_date)
            if len(df) == 0:
                return {"error": "No data found for the specified time period."}, 404
            
            student_analysis, course_analysis = analyze_student_queries(df)
            results = []
            
            for student_id, analysis_data in student_analysis.items():
                plan = generate_academic_plan_for_student(student_id, analysis_data, course_analysis)
                filename = f"academic_plan_{student_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
                file_path = os.path.join(output_dir, filename)
                
                with open(file_path, 'w') as f:
                    f.write(f"# Academic Plan for Student {student_id}\n\n")
                    f.write(plan)
                
                results.append({"student_id": student_id,"plan":plan})
            
            return {"status": "success", "data": {"plans_generated": len(results), "plans": results}}
        except Exception as e:
            return {"error": str(e)}, 500

class BulkCoursePlans(Resource):
    def post(self):
        start_date = request.json.get('start_date', None) if request.is_json else None
        
        try:
            df = get_academic_year_data(start_date)
            if len(df) == 0:
                return {"error": "No data found for the specified time period."}, 404
            
            _, course_analysis = analyze_student_queries(df)
            results = []
            
            for course, course_data in course_analysis.items():
                plan = generate_course_improvement_plan(course, course_data, df)
                filename = f"course_improvement_{course}_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
                file_path = os.path.join(output_dir, filename)
                
                with open(file_path, 'w') as f:
                    f.write(f"# Improvement Plan for Course: {course}\n\n")
                    f.write(plan)
                
                results.append({"course_name": course,"plan":plan})
            
            return {"status": "success", "data": {"plans_generated": len(results), "plans": results}}
        except Exception as e:
            return {"error": str(e)}, 500

class FileDownload(Resource):
    def get(self, filename):
        return send_from_directory(output_dir, filename)

class VisualizationDownload(Resource):
    def get(self, filename):
        return send_from_directory(viz_dir, filename)







# from flask_restful import Resource, Api
# from flask_jwt_extended import jwt_required, get_jwt
# import os
# import sqlite3
# import pandas as pd
# from datetime import datetime, timedelta
# from collections import Counter
# import matplotlib.pyplot as plt
# from flask import Flask, request, jsonify, send_file, send_from_directory
# from dotenv import load_dotenv
# from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_google_genai import ChatGoogleGenerativeAI
# import json
# import uuid
# import time
# import zipfile 


# # Load environment variables
# load_dotenv()




# # Paths
# current_dir = os.path.dirname(os.path.abspath(__file__))
# sqlite_db_path = os.path.join(current_dir, "chatbot_data.db")
# output_dir = os.path.join(current_dir, "academic_plans")
# viz_dir = os.path.join(output_dir, "visualizations")

# # Create output directories if they don't exist
# for directory in [output_dir, viz_dir]:
#     if not os.path.exists(directory):
#         os.makedirs(directory)

# # Initialize GenAI model
# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-pro",
#     temperature=0.3,
#     max_tokens=1024,
#     top_p=0.9
# )

# def get_academic_year_data(start_date=None):
#     """
#     Retrieve query data for the last academic year.
#     If start_date is not provided, it defaults to one year ago from today.
#     """
#     conn = sqlite3.connect(sqlite_db_path)
    
#     if start_date is None:
#         # Default to one year ago
#         one_year_ago = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
#         query = f"""
#         SELECT student_id, query, hint, example_code, resource_guide, timestamp
#         FROM query_responses
#         WHERE timestamp >= '{one_year_ago}'
#         """
#     else:
#         query = f"""
#         SELECT student_id, query, hint, example_code, resource_guide, timestamp
#         FROM query_responses
#         WHERE timestamp >= '{start_date}'
#         """
    
#     df = pd.read_sql_query(query, conn)
#     conn.close()
    
#     return df

# def extract_course_from_resource_guide(resource_guide):
#     """Extract course/subject information from resource guide text."""
#     if pd.isna(resource_guide) or not resource_guide:
#         return "Unknown"
    
#     # Try to find subject/course information in the resource guide
#     if "Subject:" in resource_guide:
#         parts = resource_guide.split("Subject:")
#         if len(parts) > 1:
#             course = parts[1].split()[0].strip()
#             return course
    
#     # Check for common patterns like "Check [Subject]"
#     if "Check" in resource_guide:
#         parts = resource_guide.split("Check")
#         if len(parts) > 1:
#             course = parts[1].split()[0].strip()
#             if course.endswith(','):
#                 course = course[:-1]
#             return course
    
#     return "Unknown"

# def analyze_student_queries(df):
#     """
#     Analyze student queries to identify common topics, 
#     challenging areas, and study patterns.
#     """
#     analysis = {}
    
#     # Group by student
#     student_groups = df.groupby('student_id')
    
#     # Extract courses from resource guides
#     df['course'] = df['resource_guide'].apply(extract_course_from_resource_guide)
#     course_groups = df.groupby('course')
    
#     # Create student-specific analysis
#     for student_id, student_data in student_groups:
#         # Count most common topics for this student
#         topics = Counter()
#         for query in student_data['query']:
#             # Simple topic extraction - split query and count significant words
#             words = [w.lower() for w in query.split() if len(w) > 4]
#             topics.update(words)
        
#         # Get timestamp data to analyze study patterns
#         timestamps = pd.to_datetime(student_data['timestamp'])
        
#         # Store analysis for this student
#         analysis[student_id] = {
#             'total_queries': len(student_data),
#             'common_topics': dict(topics.most_common(10)),
#             'earliest_query': timestamps.min().strftime('%Y-%m-%d'),
#             'latest_query': timestamps.max().strftime('%Y-%m-%d'),
#             'courses': student_data['course'].unique().tolist()
#         }
    
#     # Create course-specific analysis
#     course_analysis = {}
#     for course, course_data in course_groups:
#         if course == "Unknown":
#             continue
            
#         # Count common topics for this course
#         topics = Counter()
#         for query in course_data['query']:
#             words = [w.lower() for w in query.split() if len(w) > 4]
#             topics.update(words)
            
#         course_analysis[course] = {
#             'total_queries': len(course_data),
#             'students': course_data['student_id'].nunique(),
#             'common_topics': dict(topics.most_common(10)),
#         }
    
#     return analysis, course_analysis

# def generate_academic_plan_for_student(student_id, student_analysis, course_analysis):
#     """
#     Generate personalized academic plan for a student based on their query patterns.
#     """
#     # Extract relevant data for this student
#     topics = student_analysis['common_topics']
#     courses = student_analysis['courses']
    
#     # Prepare context for AI
#     context = f"""
#     Student ID: {student_id}
    
#     Query Analysis:
#     - Total queries: {student_analysis['total_queries']}
#     - Common topics: {', '.join([f'{topic} ({count})' for topic, count in topics.items()])}
#     - Courses taken: {', '.join(courses)}
    
#     Course-specific data:
#     """
    
#     for course in courses:
#         if course in course_analysis:
#             context += f"""
#             {course}:
#             - Most common topics across all students: {', '.join([f'{topic} ({count})' for topic, count in course_analysis[course]['common_topics'].items()][:5])}
#             - Total queries from all students: {course_analysis[course]['total_queries']}
#             """
    
#     # System prompt for academic plan generation
#     system_prompt = """You are an educational advisor tasked with creating personalized academic plans. 
#     Analyze the provided student query data to:
    
#     1. Identify knowledge gaps and areas where the student needs more support
#     2. Recommend specific study resources and activities
#     3. Suggest a weekly schedule that addresses their specific learning needs
#     4. Provide tailored advice on how to improve understanding of difficult topics
    
#     Be specific and practical. Format your response as a complete academic plan with clear sections.
#     """
    
#     # Generate the academic plan using AI
#     messages = [
#         SystemMessage(content=system_prompt),
#         HumanMessage(content=f"""
#         Based on the following student data, create a personalized academic plan:
        
#         {context}
        
#         Create a comprehensive academic plan divided into these sections:
#         1. Areas for Improvement (based on frequent queries)
#         2. Recommended Resources
#         3. Weekly Study Schedule
#         4. Additional Support Recommendations
#         """)
#     ]
    
#     response = llm.invoke(messages)
#     return response.content

# def generate_course_improvement_plan(course, course_data, all_data):
#     """
#     Generate suggestions for improving a course based on student queries.
#     """
#     # Prepare context for AI
#     topics = course_data['common_topics']
    
#     # Get some example queries for this course
#     course_queries = all_data[all_data['course'] == course]['query'].tolist()
#     example_queries = course_queries[:5] if len(course_queries) >= 5 else course_queries
    
#     context = f"""
#     Course: {course}
    
#     Analysis:
#     - Total queries: {course_data['total_queries']}
#     - Number of students: {course_data['students']}
#     - Common topics: {', '.join([f'{topic} ({count})' for topic, count in topics.items()])}
    
#     Example student queries:
#     {chr(10).join(['- ' + query for query in example_queries])}
#     """
    
#     # System prompt for course improvement
#     system_prompt = """You are an educational curriculum advisor tasked with improving course materials.
#     Analyze the provided query data to:
    
#     1. Identify gaps in the current course materials based on frequent student queries
#     2. Suggest specific improvements to address these gaps
#     3. Recommend additional resources or content that should be created
#     4. Suggest changes to the order or presentation of topics
    
#     Be specific and actionable in your recommendations.
#     """
    
#     # Generate the course improvement plan using AI
#     messages = [
#         SystemMessage(content=system_prompt),
#         HumanMessage(content=f"""
#         Based on the following course query data, create an improvement plan:
        
#         {context}
        
#         Create a comprehensive course improvement plan divided into these sections:
#         1. Identified Gaps in Current Materials
#         2. Suggested Content Improvements
#         3. Recommended Additional Resources
#         4. Proposed Structural Changes
#         """)
#     ]
    
#     response = llm.invoke(messages)
#     return response.content

# def generate_visualizations(df, analysis, course_analysis):
#     """Generate visualizations of the query data."""
#     # Create unique file names based on timestamp
#     timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
#     file_paths = {}
    
#     # 1. Query volume over time
#     plt.figure(figsize=(12, 6))
#     df['date'] = pd.to_datetime(df['timestamp']).dt.date
#     query_counts = df.groupby('date').size()
#     query_counts.plot(kind='line')
#     plt.title('Query Volume Over Time')
#     plt.xlabel('Date')
#     plt.ylabel('Number of Queries')
#     filename = f'query_volume_time_{timestamp}.png'
#     filepath = os.path.join(viz_dir, filename)
#     plt.savefig(filepath)
#     plt.close()
#     file_paths['query_volume'] = filename
    
#     # 2. Queries by course
#     plt.figure(figsize=(12, 6))
#     course_counts = df['course'].value_counts()
#     course_counts.plot(kind='bar')
#     plt.title('Queries by Course')
#     plt.xlabel('Course')
#     plt.ylabel('Number of Queries')
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     filename = f'queries_by_course_{timestamp}.png'
#     filepath = os.path.join(viz_dir, filename)
#     plt.savefig(filepath)
#     plt.close()
#     file_paths['queries_by_course'] = filename
    
#     # 3. Student activity levels
#     plt.figure(figsize=(12, 6))
#     student_counts = df['student_id'].value_counts().head(20)  # Top 20 students
#     student_counts.plot(kind='bar')
#     plt.title('Query Counts for Most Active Students')
#     plt.xlabel('Student ID')
#     plt.ylabel('Number of Queries')
#     plt.xticks(rotation=90)
#     plt.tight_layout()
#     filename = f'student_activity_{timestamp}.png'
#     filepath = os.path.join(viz_dir, filename)
#     plt.savefig(filepath)
#     plt.close()
#     file_paths['student_activity'] = filename
    
#     return file_paths

# def generate_summary_report(df, student_analysis, course_analysis, start_date):
#     """Generate a summary report of the analysis."""
#     summary = {
#         "generated_on": datetime.now().strftime('%Y-%m-%d'),
#         "analysis_period": {
#             "start_date": start_date,
#             "end_date": datetime.now().strftime('%Y-%m-%d')
#         },
#         "overview": {
#             "total_queries": len(df),
#             "total_students": df['student_id'].nunique(),
#             "total_courses": df['course'].nunique()
#         },
#         "most_active_students": df['student_id'].value_counts().head(10).to_dict(),
#         "most_queried_courses": df['course'].value_counts().head(10).to_dict()
#     }
    
#     # Common topics across all queries
#     all_words = []
#     for query in df['query']:
#         words = [w.lower() for w in query.split() if len(w) > 4]
#         all_words.extend(words)
    
#     summary["common_topics"] = dict(Counter(all_words).most_common(15))
    
#     return summary

# class Data(Resource):
#     def get(self):
#         start_date = request.args.get('start_date', (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'))
#         try:
#             df = get_academic_year_data(start_date)
#             if df.empty:
#                 return {"error": "No data found."}, 404
#             student_analysis, course_analysis = analyze_student_queries(df)
#             return {"status": "success", "data": {"query_count": len(df), "student_count": df['student_id'].nunique(), "course_count": df['course'].nunique(), "start_date": start_date, "end_date": datetime.now().strftime('%Y-%m-%d')}}
#         except Exception as e:
#             return {"error": str(e)}, 500

# class Students(Resource):
#     def get(self):
#         start_date = request.args.get('start_date', None)
#         try:
#             df = get_academic_year_data(start_date)
#             if df.empty:
#                 return {"error": "No data found."}, 404
#             student_analysis, _ = analyze_student_queries(df)
#             students = [{"id": sid, "total_queries": data['total_queries'], "courses": data['courses'], "earliest_query": data['earliest_query'], "latest_query": data['latest_query']} for sid, data in student_analysis.items()]
#             return {"status": "success", "data": students}
#         except Exception as e:
#             return {"error": str(e)}, 500

# class Courses(Resource):
#     def get(self):
#         start_date = request.args.get('start_date', None)
#         try:
#             df = get_academic_year_data(start_date)
#             if df.empty:
#                 return {"error": "No data found."}, 404
#             _, course_analysis = analyze_student_queries(df)
#             courses = [{"name": cname, "total_queries": data['total_queries'], "student_count": data['students'], "common_topics": data['common_topics']} for cname, data in course_analysis.items()]
#             return {"status": "success", "data": courses}
#         except Exception as e:
#             return {"error": str(e)}, 500

# class StudentPlan(Resource):
#     def post(self, student_id):
#         start_date = request.json.get('start_date', None) if request.is_json else None
#         try:
#             df = get_academic_year_data(start_date)
#             if df.empty or student_id not in df['student_id'].unique():
#                 return {"error": f"Student {student_id} not found."}, 404
#             student_analysis, course_analysis = analyze_student_queries(df)
#             plan = generate_academic_plan_for_student(student_id, student_analysis[student_id], course_analysis)
#             filename = f"academic_plan_{student_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
#             with open(filename, 'w') as f:
#                 f.write(plan)
#             return {"status": "success", "data": {"student_id": student_id, "plan": plan, "file_path": filename}}
#             # return send_file(filename, as_attachment=True)
#         except Exception as e:
#             return {"error": str(e)}, 500

# # class StudentPlan(Resource):
# #     def post(self, student_id):
# #         start_date = request.json.get('start_date', None) if request.is_json else None
# #         try:
# #             df = get_academic_year_data(start_date)
# #             if df.empty or student_id not in df['student_id'].unique():
# #                 return {"error": f"Student {student_id} not found."}, 404
            
# #             student_analysis, course_analysis = analyze_student_queries(df)
# #             plan = generate_academic_plan_for_student(student_id, student_analysis[student_id], course_analysis)

# #             # Ensure 'files' directory exists
# #             folder = os.path.join(os.getcwd(), "files")
# #             os.makedirs(folder, exist_ok=True)

# #             # Create the file
# #             filename = f"academic_plan_{student_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
# #             filepath = os.path.join(folder, filename)

# #             with open(filepath, 'w') as f:
# #                 f.write(plan)

# #             # Ensure file is fully written before sending
# #             time.sleep(0.5)  # Small delay to prevent race condition

# #             # Check if file exists
# #             if not os.path.exists(filepath):
# #                 return {"error": f"File {filepath} not found after creation."}, 500
            
# #             # Return file
# #             return send_file(filepath, as_attachment=True)

# #         except Exception as e:
# #             import traceback
# #             print(traceback.format_exc())  # Logs full error details
# #             return {"error": str(e)}, 500

# class CoursePlan(Resource):
#     def post(self, course_name):
#         start_date = request.json.get('start_date', None) if request.is_json else None
#         try:
#             df = get_academic_year_data(start_date)
#             if df.empty or course_name not in df['course'].unique():
#                 return {"error": f"Course {course_name} not found."}, 404
#             _, course_analysis = analyze_student_queries(df)
#             plan = generate_course_improvement_plan(course_name, course_analysis[course_name], df)
#             filename = f"course_improvement_{course_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
#             with open(filename, 'w') as f:
#                 f.write(plan)
#             return {"status": "success", "data": {"course_name": course_name, "plan": plan, "file_path": filename}}
#         except Exception as e:
#             return {"error": str(e)}, 500


# # class CoursePlan(Resource):
# #     def post(self, course_name):
# #         """API endpoint to generate an improvement plan for a specific course."""
# #         start_date = request.json.get('start_date', None) if request.is_json else None
        
# #         try:
# #             df = get_academic_year_data(start_date)
            
# #             if df.empty:
# #                 return jsonify({"error": "No data found for the specified time period."}), 404
            
# #             _, course_analysis = analyze_student_queries(df)
            
# #             if course_name not in course_analysis:
# #                 return jsonify({"error": f"Course {course_name} not found in the data."}), 404
            
# #             # Generate the course improvement plan
# #             plan = generate_course_improvement_plan(course_name, course_analysis[course_name], df)
            
# #             # Save the plan
# #             filename = f"course_improvement_{course_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
# #             file_path = os.path.join(output_dir, filename)
            
# #             with open(file_path, 'w') as f:
# #                 f.write(f"# Improvement Plan for Course: {course_name}\n\n")
# #                 f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d')}\n\n")
# #                 f.write(plan)
            
# #             return {
# #                 "status": "success",
# #                 "data": {
# #                     "course_name": course_name,
# #                     "plan": plan,
# #                     "file_path": filename
# #                 }
# #             }, 200
# #         except Exception as e:
# #             return {"error": str(e)}, 500

# # class CoursePlan(Resource):
# #     def post(self, course_name):
# #         """API endpoint to generate an improvement plan for a specific course."""
# #         start_date = request.json.get('start_date', None) if request.is_json else None
        
# #         try:
# #             df = get_academic_year_data(start_date)
            
# #             if df.empty:
# #                 return jsonify({"error": "No data found for the specified time period."}), 404
            
# #             _, course_analysis = analyze_student_queries(df)
            
# #             if course_name not in course_analysis:
# #                 return jsonify({"error": f"Course {course_name} not found in the data."}), 404
            
# #             # Generate the course improvement plan
# #             plan = generate_course_improvement_plan(course_name, course_analysis[course_name], df)
            
# #             # Ensure 'files' directory exists
# #             folder = os.path.join(os.getcwd(), "files")
# #             os.makedirs(folder, exist_ok=True)

# #             # Save the plan
# #             filename = f"course_improvement_{course_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
# #             file_path = os.path.join(folder, filename)

# #             with open(file_path, 'w') as f:
# #                 f.write(f"# Improvement Plan for Course: {course_name}\n\n")
# #                 f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d')}\n\n")
# #                 f.write(plan)

# #             # Ensure file is fully written before sending
# #             time.sleep(0.5)  # Small delay to prevent race condition

# #             # Check if file exists before sending
# #             if not os.path.exists(file_path):
# #                 return {"error": f"File {file_path} not found after creation."}, 500
            
# #             # Return the file as an attachment
# #             return send_file(file_path, as_attachment=True)

# #         except Exception as e:
# #             import traceback
# #             print(traceback.format_exc())  # Logs full error details
# #             return {"error": str(e)}, 500


# class Visualizations(Resource):
#     def get(self):
#         start_date = request.args.get('start_date', None)
        
#         try:
#             df = get_academic_year_data(start_date)
#             if len(df) == 0:
#                 return {"error": "No data found for the specified time period."}, 404
            
#             student_analysis, course_analysis = analyze_student_queries(df)
#             file_paths = generate_visualizations(df, student_analysis, course_analysis)
            
#             return send_file(file_paths, as_attachment=True)
#         except Exception as e:
#             return {"error": str(e)}, 500

# class SummaryReport(Resource):
#     def get(self):
#         start_date = request.args.get('start_date', (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'))
        
#         try:
#             df = get_academic_year_data(start_date)
#             if len(df) == 0:
#                 return {"error": "No data found for the specified time period."}, 404
            
#             student_analysis, course_analysis = analyze_student_queries(df)
#             summary = generate_summary_report(df, student_analysis, course_analysis, start_date)
            
#             report_id = str(uuid.uuid4())[:8]
#             filename = f"summary_report_{report_id}.md"
#             file_path = os.path.join(output_dir, filename)
            
#             with open(file_path, 'w') as f:
#                 f.write(f"# Academic Planning Summary Report\n\n")
#                 f.write(f"Generated on: {summary['generated_on']}\n\n")
#                 f.write(f"Analysis period: {summary['analysis_period']['start_date']} to {summary['analysis_period']['end_date']}\n\n")
#                 f.write("## Overview\n\n")
#                 f.write(f"- Total queries analyzed: {summary['overview']['total_queries']}\n")
#                 f.write(f"- Total students: {summary['overview']['total_students']}\n")
#                 f.write(f"- Total courses identified: {summary['overview']['total_courses']}\n\n")
            
#             return {"status": "success", "data": {"summary": summary, "file_path": filename}}
#         except Exception as e:
#             return {"error": str(e)}, 500

# # class SummaryReport(Resource):
# #     def get(self):
# #         start_date = request.args.get('start_date', (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'))
        
# #         try:
# #             df = get_academic_year_data(start_date)
# #             if df.empty:
# #                 return {"error": "No data found for the specified time period."}, 404
            
# #             student_analysis, course_analysis = analyze_student_queries(df)
# #             summary = generate_summary_report(df, student_analysis, course_analysis, start_date)
            
# #             # Ensure 'files' directory exists
# #             folder = os.path.join(os.getcwd(), "files")
# #             os.makedirs(folder, exist_ok=True)

# #             # Generate unique filename
# #             report_id = str(uuid.uuid4())[:8]
# #             filename = f"summary_report_{report_id}.md"
# #             file_path = os.path.join(folder, filename)

# #             # Write report to file
# #             with open(file_path, 'w') as f:
# #                 f.write(f"# Academic Planning Summary Report\n\n")
# #                 f.write(f"Generated on: {summary['generated_on']}\n\n")
# #                 f.write(f"Analysis period: {summary['analysis_period']['start_date']} to {summary['analysis_period']['end_date']}\n\n")
# #                 f.write("## Overview\n\n")
# #                 f.write(f"- Total queries analyzed: {summary['overview']['total_queries']}\n")
# #                 f.write(f"- Total students: {summary['overview']['total_students']}\n")
# #                 f.write(f"- Total courses identified: {summary['overview']['total_courses']}\n\n")

# #             # Ensure file is fully written before sending
# #             if not os.path.exists(file_path):
# #                 return {"error": f"File {file_path} not found after creation."}, 500
            
# #             # Return the file for download
# #             return send_file(file_path, as_attachment=True)

# #         except Exception as e:
# #             import traceback
# #             print(traceback.format_exc())  # Logs full error details
# #             return {"error": str(e)}, 500

# class BulkStudentPlans(Resource):
#     def post(self):
#         start_date = request.json.get('start_date', None) if request.is_json else None
        
#         try:
#             df = get_academic_year_data(start_date)
#             if len(df) == 0:
#                 return {"error": "No data found for the specified time period."}, 404
            
#             student_analysis, course_analysis = analyze_student_queries(df)
#             results = []
            
#             for student_id, analysis_data in student_analysis.items():
#                 plan = generate_academic_plan_for_student(student_id, analysis_data, course_analysis)
#                 filename = f"academic_plan_{student_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
#                 file_path = os.path.join(output_dir, filename)
                
#                 with open(file_path, 'w') as f:
#                     f.write(f"# Academic Plan for Student {student_id}\n\n")
#                     f.write(plan)
                
#                 results.append({"student_id": student_id,"plan":plan})
            
#             return {"status": "success", "data": {"plans_generated": len(results), "plans": results}}
#         except Exception as e:
#             return {"error": str(e)}, 500

# # class BulkStudentPlans(Resource):
# #     def post(self):
# #         start_date = request.json.get('start_date', None) if request.is_json else None
        
# #         try:
# #             df = get_academic_year_data(start_date)
# #             if df.empty:
# #                 return {"error": "No data found for the specified time period."}, 404
            
# #             student_analysis, course_analysis = analyze_student_queries(df)
# #             results = []

# #             # Ensure 'files' directory exists
# #             folder = os.path.join(os.getcwd(), "files")
# #             os.makedirs(folder, exist_ok=True)

# #             zip_filename = f"bulk_academic_plans_{datetime.now().strftime('%Y%m%d%H%M%S')}.zip"
# #             zip_filepath = os.path.join(folder, zip_filename)

# #             with zipfile.ZipFile(zip_filepath, 'w') as zipf:
# #                 for student_id, analysis_data in student_analysis.items():
# #                     filename = f"academic_plan_{student_id}.md"
# #                     file_path = os.path.join(folder, filename)

# #                     with open(file_path, 'w') as f:
# #                         f.write(f"# Academic Plan for Student {student_id}\n\n")
# #                         f.write(generate_academic_plan_for_student(student_id, analysis_data, course_analysis))
                    
# #                     zipf.write(file_path, filename)  # Add file to ZIP
# #                     results.append({"student_id": student_id, "file_name": filename})

# #             return send_file(zip_filepath, as_attachment=True)

# #         except Exception as e:
# #             import traceback
# #             print(traceback.format_exc())  # Logs full error details
# #             return {"error": str(e)}, 500

# class BulkCoursePlans(Resource):
#     def post(self):
#         start_date = request.json.get('start_date', None) if request.is_json else None
        
#         try:
#             df = get_academic_year_data(start_date)
#             if len(df) == 0:
#                 return {"error": "No data found for the specified time period."}, 404
            
#             _, course_analysis = analyze_student_queries(df)
#             results = []
            
#             for course, course_data in course_analysis.items():
#                 plan = generate_course_improvement_plan(course, course_data, df)
#                 filename = f"course_improvement_{course}_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
#                 file_path = os.path.join(output_dir, filename)
                
#                 with open(file_path, 'w') as f:
#                     f.write(f"# Improvement Plan for Course: {course}\n\n")
#                     f.write(plan)
                
#                 results.append({"course_name": course,"plan":plan})
            
#             return {"status": "success", "data": {"plans_generated": len(results), "plans": results}}
#         except Exception as e:
#             return {"error": str(e)}, 500

# # output_dir = "files"  # Directory to save generated files

# # class BulkCoursePlans(Resource):
# #     def post(self):
# #         start_date = request.json.get('start_date', None) if request.is_json else None

# #         try:
# #             df = get_academic_year_data(start_date)
# #             if df.empty:
# #                 return {"error": "No data found for the specified time period."}, 404

# #             _, course_analysis = analyze_student_queries(df)
# #             results = []

# #             # Ensure the 'files' directory exists
# #             folder = os.path.join(os.getcwd(), "files")
# #             os.makedirs(folder, exist_ok=True)

# #             # Create a zip file for all the course plans
# #             zip_filename = f"bulk_course_improvement_plans_{datetime.now().strftime('%Y%m%d%H%M%S')}.zip"
# #             zip_filepath = os.path.join(folder, zip_filename)

# #             with zipfile.ZipFile(zip_filepath, 'w') as zipf:
# #                 for course, course_data in course_analysis.items():
# #                     filename = f"course_improvement_{course}.md"
# #                     file_path = os.path.join(folder, filename)

# #                     # Generate the course improvement plan
# #                     with open(file_path, 'w') as f:
# #                         f.write(f"# Improvement Plan for Course: {course}\n\n")
# #                         f.write(generate_course_improvement_plan(course, course_data, df))

# #                     zipf.write(file_path, filename)  # Add each file to the ZIP
# #                     results.append({"course_name": course, "file_name": filename})

# #             # Send the ZIP file as a downloadable attachment
# #             return send_file(zip_filepath, as_attachment=True)

# #         except Exception as e:
# #             import traceback
# #             print(traceback.format_exc())  # Log full error details
# #             return {"error": str(e)}, 500

# class FileDownload(Resource):
#     def get(self, filename):
#         return send_from_directory(output_dir, filename)

# class VisualizationDownload(Resource):
#     def get(self, filename):
#         return send_from_directory(viz_dir, filename)




