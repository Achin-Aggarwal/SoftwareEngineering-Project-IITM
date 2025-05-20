import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import Counter
import re
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import seaborn as sns


from flask_restful import Resource, Api
from flask import Flask, request, jsonify

# Load environment variables
load_dotenv()

# Paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sqlite_db_path = os.path.join(current_dir, "chatbot_data.db")




class WeeklyAnalysis(Resource):
    def get(self):
        try:
            # Get number of days from request args
            days = request.args.get('days', default=7, type=int)
            report = self.analyze_weekly_query_patterns(days)
            
            return {
                "status": "success",
                "message": "Weekly analysis report generated successfully",
                "report_content": report
            }, 200
        except Exception as e:
            return {"status": "error", "message": str(e)}, 500
    
    def get_queries_by_timeframe(self, days):
        conn = sqlite3.connect(sqlite_db_path)
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
        
        query = """
        SELECT student_id, query, hint, example_code, resource_guide, timestamp
        FROM query_responses
        WHERE timestamp >= ?
        ORDER BY timestamp DESC
        """
        
        df = pd.read_sql_query(query, conn, params=(cutoff_date,))
        conn.close()
        
        return df if not df.empty else None
    
    def analyze_weekly_query_patterns(self, days):
        data = self.get_queries_by_timeframe(7)
        if data is None or data.empty:
            return f"No queries found in the last {days} days."
        
        total_queries = len(data)
        unique_students = data['student_id'].nunique()
        queries_per_student = data.groupby('student_id').size().mean()
        
        if not pd.api.types.is_datetime64_any_dtype(data['timestamp']):
            data['timestamp'] = pd.to_datetime(data['timestamp'])
        
        # Convert date keys to strings for JSON serialization
        data['date'] = data['timestamp'].dt.strftime('%Y-%m-%d')
        daily_query_counts = data.groupby('date').size().to_dict()
        
        all_queries = " ".join(data['query'].tolist())
        ngram_counts = Counter()
        for query in data['query']:
            for ngram in query.split():
                ngram_counts[ngram] += 1
        
        top_ngrams = ngram_counts.most_common(20)
        
        ai_analysis = """
        Based on the query patterns over the past week, the following trends were identified:
        1. Increase in queries about programming languages.
        2. High volume of syntax error-related questions.
        3. Consider providing more detailed examples in materials.
        """
        
        return {
            "total_queries": total_queries,
            "unique_students": unique_students,
            "queries_per_student": queries_per_student,
            "daily_query_counts": daily_query_counts,
            "top_ngrams": top_ngrams,
            "ai_analysis": ai_analysis
        }

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.2,
    max_tokens=1024,
    top_p=0.9
)

def get_queries_by_timeframe(days=30):
    """Retrieve all queries from the last specified number of days."""
    try:
        conn = sqlite3.connect(sqlite_db_path)
        
        # Calculate the date cutoff for filtering
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
        
        query = """
        SELECT student_id, query, hint, example_code, resource_guide, timestamp
        FROM query_responses
        WHERE timestamp >= ?
        ORDER BY timestamp DESC
        """
        
        df = pd.read_sql_query(query, conn, params=(cutoff_date,))
        return df if not df.empty else None

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
    finally:
        conn.close()

class StrugglingTopics(Resource):
    def get(self):
        days = request.args.get('days', default=30, type=int)
        data = get_queries_by_timeframe(days=days)
        
        if data is None or data.empty:
            return jsonify({"message": f"No queries found in the last {days} days."})
        
        queries = data['query'].tolist()
        repeated_queries = data.groupby('query').size().reset_index(name='count')
        repeated_queries = repeated_queries.sort_values('count', ascending=False)
        
        struggling_indicators = ['confused', "don't understand", 'struggling', 'help', 'difficulty', 'error', 'problem', 'stuck']
        topic_struggle_count = {}
        stop_words = {'how', 'to', 'what', 'is', 'are', 'the', 'a', 'an', 'in', 'for', 'of', 'and', 'with', 'can', 'i', 'you', 'me', 'my', 'we', 'our'}
        
        for query in queries:
            contains_indicator = any(indicator in query.lower() for indicator in struggling_indicators)
            words = re.findall(r'\b\w+\b', query.lower())
            topic_words = [word for word in words if word not in stop_words and len(word) > 3]
            score_multiplier = 2 if contains_indicator else 1
            for word in topic_words:
                topic_struggle_count[word] = topic_struggle_count.get(word, 0) + score_multiplier
        
        resources = data['resource_guide'].dropna().tolist()
        resource_topics = {}
        for resource in resources:
            words = re.findall(r'\b\w+\b', resource.lower())
            for word in words:
                if len(word) > 3 and word not in stop_words:
                    resource_topics[word] = resource_topics.get(word, 0) + 1
        
        system_prompt = """You are an educational data analyst identifying struggling topics.
        Identify the top 5 specific topics students struggle with, provide reasons, evidence, and instructional interventions."""
        
        context = {
            "repeated_queries": repeated_queries.head(20).to_dict('records'),
            "topic_struggle_scores": dict(sorted(topic_struggle_count.items(), key=lambda item: item[1], reverse=True)[:50]),
            "resource_topics": dict(sorted(resource_topics.items(), key=lambda item: item[1], reverse=True)[:30]),
            "raw_queries_sample": queries[:100]
        }
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Struggling Topics Analysis ({days} Days): {context}")
        ]
        
        response = llm.invoke(messages)
        
        result = {
            "analysis_period": {
                "start_date": (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d'),
                "end_date": datetime.now().strftime('%Y-%m-%d'),
                "total_queries": len(queries),
                "unique_students": data['student_id'].nunique()
            },
            "top_struggling_topics": response.content
        }
        
        return jsonify(result)