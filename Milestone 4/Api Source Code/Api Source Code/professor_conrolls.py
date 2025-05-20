from flask_restful import Resource
from flask import request , jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime,timedelta
from . import db
from .model import User,InstructorRequest,RequestStatus,IssueQuery,SolveIssue


class PendingInstructors(Resource):
    @jwt_required()
    def get(self):
        """ Retrieve all pending instructors """
        current_user_id = get_jwt_identity()
        professor = User.query.get(current_user_id)

        if not professor:
            return {"message": "Professor not found"}, 404

        pending_requests = InstructorRequest.query.filter_by(status=RequestStatus.PENDING).all()

        return jsonify([{
            "id": req.id,
            "instructor_id": req.instructor_id,
            "status": req.status.value,
            "created_at": req.created_at
        } for req in pending_requests])


class ApproveInstructor(Resource):
    @jwt_required()
    def put(self, request_id):
        """ Professor approves/rejects an instructor request """
        current_user_id = get_jwt_identity()
        professor = User.query.get(current_user_id)

        if not professor:
            return {"message": "Professor not found"}, 404

        data = request.get_json()
        new_status = data.get("status")

        if new_status not in [RequestStatus.APPROVED.value, RequestStatus.REJECTED.value]:
            return {"message": "Invalid status, use 'Approved' or 'Rejected'"}, 400

        request_record = InstructorRequest.query.get(request_id)

        if not request_record:
            return {"message": "Instructor request not found"}, 404

        request_record.status = RequestStatus[new_status.upper()]
        db.session.commit()

        return {"message": f"Instructor request {new_status.lower()} successfully"}

# API for fetching solved issues
class SolvedIssues(Resource):
    def get(self):
        solved_issues = db.session.query(IssueQuery, SolveIssue).join(SolveIssue, IssueQuery.id == SolveIssue.issue_id).all()
        result = []
        for issue, solution in solved_issues:
            result.append({
                "issue_id": issue.id,
                "details": issue.details,
                "created_at": issue.created_at,
                "solver_id": solution.solver_id,
                "answer": solution.answer,
                "solved_at": solution.created_at
            })
        return jsonify({"count": len(result), "solved_issues": result})

# API for fetching pending issues (not yet solved)
class PendingIssues(Resource):
    def get(self):
        subquery = db.session.query(SolveIssue.issue_id).subquery()
        pending_issues = IssueQuery.query.filter(~IssueQuery.id.in_(subquery)).all()
        result = [{"issue_id": issue.id, "details": issue.details, "created_at": issue.created_at} for issue in pending_issues]
        return jsonify({"count": len(result), "pending_issues": result})