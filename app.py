# Remote library imports
from flask import request, make_response, jsonify, session, render_template
from flask_restful import Resource
from models import User, Jobseeker, Employer, ContactRequest, Payment, Fileupload, JobCategory
# Local imports
from config import app, db, api, Message, mail
import datetime
from flask import flash
from flask_jwt_extended import create_access_token, get_jwt_identity, current_user, jwt_required, JWTManager


app.config["JWT_SECRET_KEY"] = "b'Y\xf1Xz\x01\xad|eQ\x80t \xca\x1a\x10K'"  
app.config['JWT_TOKEN_LOCATION'] = ['headers']
jwt = JWTManager(app)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


class Jobseekers(Resource):
    @jwt_required()
    def get(self):
        #Swagger annotations
        '''This is an endpoint that gets all jobseekers
        ---
        tags:
          - Jobseekers
        responses:
          200:
            description: Returns all jobseekers
        '''
        user = User.query.filter_by(id = current_user.id).first()
        if not user:
            return make_response({"message":"Unauthorized"}, 401)
        if user.role=='employer' or user.role=='admin':
            if user.role=='employer':
                employer = Employer.query.filter(Employer.user_id == user.id).first()
                if not employer.pay_to_view:
                    return make_response({"message": "Pay fee to have access!"}, 401)
            jobseekers = Jobseeker.query.all()
            return make_response([jobseeker.to_dict() for jobseeker in jobseekers], 200)
        else:
            return make_response({"message":"You don't have access!"}, 401)
    @jwt_required()
    def post(self):
        #Swagger annotations
        '''This is an endpoint that creates a new jobseeker
        ---
        tags:
          - Jobseekers
        parameters:
          - name: jobseeker
            in: body
            description: Jobseeker details
            schema:
              $ref: '#/definitions/Jobseeker'
        responses:
          201:
            description: Returns the created jobseeker
        '''
    
        data = request.get_json()
        new_jobseeker = Jobseeker(**data)
        new_jobseeker.user_id = current_user.id
        db.session.add(new_jobseeker)
        db.session.commit()
        return make_response(new_jobseeker.to_dict(), 201)
    
class JobseekerById(Resource):
    @jwt_required()
    def get(self, id):
        #Swagger annotations
        '''This is an endpoint that gets a jobseeker by ID
        ---
        tags:
          - Jobseekers
        parameters:
          - name: id
            in: path
            description: Jobseeker ID
            required: true
            type: integer
        responses:
          200:
            description: Returns the jobseeker
        '''
        if not current_user:
            return make_response({"message":"Unauthorized"}, 401)
        jobseeker = Jobseeker.query.filter(Jobseeker.user_id == id).first()
        if not jobseeker:
            return make_response({"message":"Jobseeker not found"}, 404)
        return make_response(jobseeker.to_dict(), 200)
    
    def patch(self, id):
        #Swagger annotations
        '''This is an endpoint that updates a jobseeker by ID
        ---
        tags:
          - Jobseekers
        parameters:
          - name: id
            in: path
            description: Jobseeker ID
            required: true
            type: integer
          - name: jobseeker
            in: body
            description: Jobseeker details
            schema:
              $ref: '#/definitions/Jobseeker'
        responses:
          200:
            description: Returns the updated jobseeker
        '''
        data = request.get_json()
        jobseeker = Jobseeker.query.filter(Jobseeker.user_id == id).first()
        
        if not jobseeker:
            return make_response({"message":"Jobseeker not found"}, 404)
        
        for key, value in data.items():
            setattr(jobseeker, key, value)
        
        db.session.add(jobseeker)
        db.session.commit()
        
        return make_response(jobseeker.to_dict(), 200)
    
    def delete(self, id):
        #Swagger annotations
        '''This is an endpoint that deletes a jobseeker by ID
        ---
        tags:
          - Jobseekers
        parameters:
          - name: id
            in: path
            description: Jobseeker ID
            required: true
            type: integer
        responses:
          204:
            description: Returns nothing
        '''
        jobseeker = Jobseeker.query.filter(Jobseeker.user_id == id).first()
        
        if not jobseeker:
            return make_response({"message":"Jobseeker not found"}, 404)
        
        db.session.delete(jobseeker)
        db.session.commit()
        
        return make_response({"message":"Jobseeker deleted"}, 204)
        

api.add_resource(Jobseekers, '/jobseekers', endpoint='jobseekers')
api.add_resource(JobseekerById, '/jobseekers/<int:id>', endpoint='jobseeker_by_id')

class Employers(Resource):
    @jwt_required()
    def get(self):
        #Swagger annotations
        '''This is an endpoint that gets all employers
        ---
        tags:
          - Employers
        responses:
          200:
            description: Returns all employers
        '''
        if not current_user or not current_user.role=='admin':
            return make_response({"message":"Unauthorized"}, 401)
        employers = Employer.query.all()
        return make_response([employer.to_dict() for employer in employers], 200)
    @jwt_required()
    def post(self):
        #Swagger annotations
        '''This is an endpoint that creates a new employer
        ---
        tags:
          - Employers
        parameters:
          - name: employer
            in: body
            description: Employer details
            schema:
              $ref: '#/definitions/Employer'
        responses:
          201:
            description: Returns the created employer
        '''
        data = request.get_json()
        new_employer = Employer(**data)
        new_employer.user_id = current_user.id
        db.session.add(new_employer)
        db.session.commit()
        return make_response(new_employer.to_dict(), 201)
    
api.add_resource(Employers, '/employers', endpoint='employers')
    
class EmployerById(Resource):
    @jwt_required()
    def get(self, id):
        #Swagger annotations
        '''This is an endpoint that gets an employer by ID
        ---
        tags:
          - Employers
        parameters:
          - name: id
            in: path
            description: Employer ID
            required: true
            type: integer
        responses:
          200:
            description: Returns the employer
        '''
        if not current_user:
            return make_response({"message":"Unauthorized"}, 401)
        employer = Employer.query.filter(Employer.user_id==id).first()
        if not employer:
            return make_response({"message":"Employer not found"}, 404)
        return make_response(employer.to_dict(), 200)
    
    def patch(self, id):
        #Swagger annotations
        '''This is an endpoint that updates an employer by ID
        ---
        tags:
          - Employers
        parameters:
          - name: id
            in: path
            description: Employer ID
            required: true
            type: integer
          - name: employer
            in: body
            description: Employer details
            schema:
              $ref: '#/definitions/Employer'
        responses:
          200:
            description: Returns the updated employer
        '''
        data = request.get_json()
        employer = Employer.query.filter(Employer.user_id==id).first()
        
        if not employer:
            return make_response({"message":"Employer not found"}, 404)
        
        for attr in data:
            setattr(employer, attr, data.get(attr))
        
        db.session.add(employer)
        db.session.commit()
        
        return make_response(employer.to_dict(), 200)
    
    def delete(self, id):
        #Swagger annotations
        '''This is an endpoint that deletes an employer by ID
        ---
        tags:
          - Employers
        parameters:
          - name: id
            in: path
            description: Employer ID
            required: true
            type: integer
        responses:
          200:
            description: Returns nothing
        '''
        employer = Employer.query.filter_by(id=id).first()
        
        if not employer:
            return make_response({"message":"Employer not found"}, 404)
        
        db.session.delete(employer)
        db.session.commit()
        
        return make_response({"message":"Employer deleted"}, 200)
    
api.add_resource(EmployerById, '/employers/<int:id>', endpoint='employer_by_id')

class Users(Resource):
    @jwt_required()
    def get(self):
        #Swagger annotations
        '''This is an endpoint that gets all users
        ---
        tags:
          - Users
        responses:
          200:
            description: Returns all users
        '''
        if not current_user.id or not current_user.role=='admin':
            return make_response({"message":"Unauthorized"}, 401)
        users = User.query.all()
        return make_response([user.to_dict() for user in users], 200)
    
class UsersById(Resource):
    @jwt_required()
    def get(self, id):
        #Swagger annotations
        '''This is an endpoint that gets a user by ID
        ---
        tags:
          - Users
        parameters:
          - name: id
            in: path
            description: User ID
            required: true
            type: integer
        responses:
          200:
            description: Returns the user
        '''
        if not current_user.id:
            return make_response({"message":"Unauthorized"}, 401)
        user = User.query.filter_by(id=id).first()
        if not user:
            return make_response({"message":"User not found"}, 404)
        return make_response(user.to_dict(), 200)
    
    @jwt_required()
    def patch(self, id):
        #Swagger annotations
        '''This is an endpoint that updates a user by ID
        ---
        tags:
          - Users
        parameters:
          - name: id
            in: path
            description: User ID
            required: true
            type: integer
          - name: user
            in: body
            description: User details
            schema:
              $ref: '#/definitions/User'
        responses:
          200:
            description: Returns the updated user
        '''
        if not current_user:
            return make_response({"message":"Unauthorized"}, 401)
        data = request.get_json()
        user = User.query.filter_by(id=id).first()
        
        if not user:
            return make_response({"message":"User not found"}, 404)
        
        for attr in data:
            setattr(user, attr, data.get(attr))
        
        db.session.add(user)
        db.session.commit()
        
        return make_response(user.to_dict(), 200)
    
    @jwt_required()
    def delete(self, id):
        #Swagger annotations
        '''This is an endpoint that deletes a user by ID
        ---
        tags:
          - Users
        parameters:
          - name: id
            in: path
            description: User ID
            required: true
            type: integer
        responses:
          200:
            description: Returns nothing
        '''
        if not current_user.id:
            return make_response({"message":"Unauthorized"}, 401)
        user = User.query.filter_by(id=id).first()
        
        if not user:
            return make_response({"message":"User not found"}, 404)
        
        db.session.delete(user)
        db.session.commit()
        
        return make_response({"message":"User deleted"}, 200)

api.add_resource(Users, '/users', endpoint='users')
api.add_resource(UsersById, '/users/<int:id>', endpoint='user_by_id')

class Payments(Resource):
    @jwt_required()
    def get(self):
        #Swagger annotations
        '''This is an endpoint that gets all payments
        ---
        tags:
          - Payments
        responses:
          200:
            description: Returns all payments
        '''
        if not current_user: #or not session['role']=='admin'
            return make_response({"message":"Unauthorized"}, 401)
        payments = Payment.query.all()
        return make_response([payment.to_dict() for payment in payments], 200)
    
    @jwt_required()
    def post(self):
        #Swagger annotations
        '''This is an endpoint that creates a new payment
        ---
        tags:
          - Payments
        parameters:
          - name: payment
            in: body
            description: Payment details
            schema:
              $ref: '#/definitions/Payment'
        responses:
          201:
            description: Returns the created payment
        '''
        data = request.get_json()
        new_payment = Payment(**data)
        employer = Employer.query.filter(Employer.user_id==current_user.id).first()
        new_payment.employer_id = employer.id
        new_payment.payment_status = True
        employer.pay_to_view = True
        
        db.session.add(new_payment)
        db.session.commit()
        msg_title = f"Hey {employer.user.username}"
        msg_body = f"We received your payment of {new_payment.amount} for {employer.company_name}"  #employer.name
        # sender = "noreply@gmail.com"
        msg = Message(subject=msg_title, recipients=[employer.user.email])  #jobseeker.email
        msg.body = msg_body
        try:
            mail.send(msg)
            print("Mail sent successfully!")
        except Exception as e:
            flash(f"Failed to send mail: {str(e)}", 'error')
        return make_response(new_payment.to_dict(), 201)
    
api.add_resource(Payments, "/payments", endpoint='payments')

class ContactRequests(Resource):
    @jwt_required()
    def get(self):
        #Swagger annotations
        '''This is an endpoint that gets all contact requests
        ---
        tags:
          - Contact Requests
        responses:
          200:
            description: Returns all contact requests
        '''
        if not current_user or not current_user.role=='admin':
            return make_response({"message":"Unauthorized"}, 401)
        contact_requests = ContactRequest.query.all()
        return make_response([contact_request.to_dict() for contact_request in contact_requests], 200)
    
    @jwt_required()
    def post(self):
        #Swagger annotations
        '''This is an endpoint that creates a new contact request
        ---
        tags:
          - Contact Requests
        parameters:
          - name: contact_request
            in: body
            description: Contact request details
            schema:
              $ref: '#/definitions/ContactRequest'
        responses:
          201:
            description: Returns the created contact request
        '''
        data = request.get_json()
        jobseeker = Jobseeker.query.filter_by(id=data.get('jobseekerID')).first()
        employer = Employer.query.filter(Employer.user_id==current_user.id).first()
        if not jobseeker or not employer:
            return make_response({"message":"User not found"}, 404)
        new_contact_request = ContactRequest(jobseeker=jobseeker, employer=employer, message=data['message'])
        new_contact_request.created_at = datetime.datetime.now()
        new_contact_request.status = "false"
        db.session.add(new_contact_request)
        db.session.commit()
        msg_title = f"Hey {jobseeker.name}"
        msg_body = f"New contact request from {employer.company_name}: {new_contact_request.message}"  #employer.name
        # sender = "noreply@app.com"
        msg = Message(subject=msg_title, recipients=[jobseeker.user.email])  #jobseeker.email
        msg.body = msg_body
        try:
            mail.send(msg)
            print("Mail sent successfully!")
        except Exception as e:
            flash(f"Failed to send mail: {str(e)}", 'error')
        return make_response(new_contact_request.to_dict(), 201)


api.add_resource(ContactRequests, "/contact_requests", endpoint='contact_requests')

class ContactRequestById(Resource):
    @jwt_required()
    def get(self, id):
        #Swagger annotations
        '''This is an endpoint that gets a contact request by ID
        ---
        tags:
          - Contact Requests
        parameters:
          - name: id
            in: path
            description: Contact request ID
            required: true
            type: integer
        responses:
          200:
            description: Returns the contact request
        '''
        if not current_user:
            return make_response({"message":"Unauthorized"}, 401)
        contact_request = ContactRequest.query.filter_by(id=id).first()
        if not contact_request:
            return make_response({"message":"Contact request not found"}, 404)
        return make_response(contact_request.to_dict(), 200)
    
    @jwt_required()
    def patch(self, id):
        #Swagger annotations
        '''This is an endpoint that updates a contact request by ID
        ---
        tags:
          - Contact Requests
        parameters:
          - name: id
            in: path
            description: Contact request ID
            required: true
            type: integer
          - name: contact_request
            in: body
            description: Contact request details
            schema:
              $ref: '#/definitions/ContactRequest'
        responses:
          200:
            description: Returns the updated contact request
        '''
        if not current_user:
            return make_response({"message":"Unauthorized"}, 401)
        
        data = request.get_json()
        contact_request = ContactRequest.query.filter_by(id=id).first()
        
        if not contact_request:
            return make_response({"message":"Contact request not found"}, 404)
        
        for attr in data:
            setattr(contact_request, attr, data[attr])
        
        db.session.add(contact_request)
        db.session.commit()
        
        return make_response(contact_request.to_dict(), 200)
    
    @jwt_required()
    def delete(self, id):
        #Swagger annotations
        '''This is an endpoint that deletes a contact request by ID
        ---
        tags:
          - Contact Requests
        parameters:
          - name: id
            in: path
            description: Contact request ID
            required: true
            type: integer
        responses:
          200:
            description: Returns nothing
        '''
        if not current_user:
            return make_response({"message":"Unauthorized"}, 401)
        
        contact_request = ContactRequest.query.filter_by(id=id).first()
        
        if not contact_request:
            return make_response({"message":"Contact request not found"}, 404)
        
        db.session.delete(contact_request)
        db.session.commit()
        
        return make_response({"message":"Contact request deleted"}, 200)


api.add_resource(ContactRequestById, '/contact_requests/<int:id>', endpoint='contact_request_by_id')

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
        
        access_token = create_access_token(identity=user.id)

        return make_response({"user":user.to_dict(rules=('-_password_hash',)),'access_token': access_token},201)
        

class CheckSession(Resource):
    @jwt_required()
    def get(self):
        # We can now access our sqlalchemy User object via `current_user`
        return make_response(current_user.to_dict(),200)
    
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
        
        else:
          access_token = create_access_token(identity=user.id)
          
          response_body = make_response({"user":user.to_dict(rules=('-_password_hash',)),"access_token":access_token},201)     
          
          return response_body
          
          
    
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