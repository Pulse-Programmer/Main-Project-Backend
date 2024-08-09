# Remote library imports
from flask import request, make_response, jsonify, session, render_template
from flask_restful import Resource
from models import User, Jobseeker, Employer, ContactRequest, Payment, Fileupload, JobCategory
# Local imports
from config import app, db, api
# Model imports
# from flask_swagger_ui import get_swaggerui_blueprint


# # Swagger setup
# SWAGGER_URL = '/swagger'
# API_URL = '/static/swagger.json'  # URL for the Swagger JSON file

# swaggerui_blueprint = get_swaggerui_blueprint(
#     SWAGGER_URL,
#     API_URL,
#     config={
#         'app_name': "Job Portal API"
#     }
# )

# app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
class Jobseekers(Resource):
    def get(self):
        if not session.get('user_id'):
            return make_response({"message":"Unauthorized"}, 401)
        if session['role']=='employer' or session['role']=='admin':
            if session['role']=='employer':
                employer = Employer.query.get(session['user_id'])
                if not employer.pay_to_view:
                    return make_response({"message": "Pay fee to have access!"}, 401)
            jobseekers = Jobseeker.query.all()
            return make_response([jobseeker.to_dict() for jobseeker in jobseekers], 200)
        else:
            return make_response({"message":"You don't have access!"}, 401)
        
    def post(self):
        data = request.get_json()
        new_jobseeker = Jobseeker(**data)
        db.session.add(new_jobseeker)
        db.session.commit()
        return make_response(new_jobseeker.to_dict(), 201)
    
class JobseekerById(Resource):
    def get(self, id):
        if not session.get('user_id'):
            return make_response({"message":"Unauthorized"}, 401)
        jobseeker = Jobseeker.query.filter_by(id=id).first()
        if not jobseeker:
            return make_response({"message":"Jobseeker not found"}, 404)
        return make_response(jobseeker.to_dict(), 200)
    
    def patch(self, id):
        data = request.get_json()
        jobseeker = Jobseeker.query.filter_by(id=id).first()
        
        if not jobseeker:
            return make_response({"message":"Jobseeker not found"}, 404)
        
        for key, value in data.items():
            setattr(jobseeker, key, value)
        
        db.session.add(jobseeker)
        db.session.commit()
        
        return make_response(jobseeker.to_dict(), 200)
    
    def delete(self, id):
        jobseeker = Jobseeker.query.filter_by(id=id).first()
        
        if not jobseeker:
            return make_response({"message":"Jobseeker not found"}, 404)
        
        db.session.delete(jobseeker)
        db.session.commit()
        
        return make_response({"message":"Jobseeker deleted"}, 204)
        

api.add_resource(Jobseekers, '/jobseekers', endpoint='jobseekers')
api.add_resource(JobseekerById, '/jobseekers/<int:id>', endpoint='jobseeker_by_id')

class Employers(Resource):
    def get(self):
        if not session.get('user_id') or not session['role']=='admin':
            return make_response({"message":"Unauthorized"}, 401)
        employers = Employer.query.all()
        return make_response([employer.to_dict() for employer in employers], 200)
    
    def post(self):
        data = request.get_json()
        new_employer = Employer(**data)
        db.session.add(new_employer)
        db.session.commit()
        return make_response(new_employer.to_dict(), 201)
    
api.add_resource(Employers, '/employers', endpoint='employers')
    
class EmployerById(Resource):
    def get(self, id):
        if not session.get('user_id') or not session['role']=='admin':
            return make_response({"message":"Unauthorized"}, 401)
        employer = Employer.query.filter_by(id=id).first()
        if not employer:
            return make_response({"message":"Employer not found"}, 404)
        return make_response(employer.to_dict(), 200)
    
    def patch(self, id):
        data = request.get_json()
        employer = Employer.query.filter_by(id=id).first()
        
        if not employer:
            return make_response({"message":"Employer not found"}, 404)
        
        for attr in data:
            setattr(employer, attr, data.get(attr))
        
        db.session.add(employer)
        db.session.commit()
        
        return make_response(employer.to_dict(), 200)
    
    def delete(self, id):
        employer = Employer.query.filter_by(id=id).first()
        
        if not employer:
            return make_response({"message":"Employer not found"}, 404)
        
        db.session.delete(employer)
        db.session.commit()
        
        return make_response({"message":"Employer deleted"}, 200)
    
api.add_resource(EmployerById, '/employers/<int:id>', endpoint='employer_by_id')

class Signup(Resource):
    def post(self):
        data = request.get_json()
        
        username = data.get('username')
        email = data.get('email')
        phone_number = data.get('phone_number')
        password = data.get('password')
        role = data.get('role')
        
        if not email or not password or not role:
            return make_response({"message":"Missing required fields"}, 400)
        
        user = User(email=email, role=role, username=username, phone_number=phone_number)
        user.password_hash = password
        
        if user.role == 'admin':
            user.verified = True
        
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = user.id
        session['role'] = user.role
        
        response_body = user.to_dict(rules=('-_password_hash',))
        
        return make_response(response_body, 201)

class CheckSession(Resource):
    def get(self):
        if not session.get('user_id'):
            return make_response({"message":"Unauthorized"}, 401)
        
        user = User.query.get(session.get('user_id'))
        
        response_body = user.to_dict(rules=('-_password_hash',))
        
        return make_response(response_body, 200)
    
class Login(Resource):
    def post(self):
        data = request.get_json()
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return make_response({"message":"Missing required fields"}, 400)
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.authenticate(password):
            return make_response({"message":"Invalid credentials"}, 401)
        
        session['user_id'] = user.id
        session['role'] = user.role
        
        response_body = user.to_dict(rules=('-_password_hash',))
        
        return make_response(response_body, 200)
    
class Logout(Resource):
    def delete(self):
        if not session.get('user_id'):
            return make_response({"message":"Unauthorized"}, 401)
        
        session.pop('user_id')
        session.pop('role')
        
        return make_response({"message":"Logged out"}, 200)
    
    
    
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')

if __name__ == "__main__":
    app.run(port=5555, debug=True)