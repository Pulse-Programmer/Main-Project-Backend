from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy

from config import db, bcrypt

class Admin(db.Model, SerializerMixin):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    #one-to-one relationship with user
    user = db.relationship('User', back_populates='admin')

    def __repr__(self):
        return f"<Admin(id={self.id}, user_id={self.user_id})>"

class Jobseeker(db.Model, SerializerMixin):
    __tablename__ = 'jobseekers'
    id = db.Column(db.Integer, primary_key=True)
    prof_pic = db.Column(db.String)
    fileupload_id = db.Column(db.Integer, db.ForeignKey('fileuploads.id'))
    bio = db.Column(db.String)
    availability = db.Column(db.Boolean)
    job_category_id = db.Column(db.Integer, db.ForeignKey('jobcategories.id'))
    salary_expectation = db.Column(db.Float)
    verification_status = db.Column(db.Boolean, default=False)
    work_experience = db.Column(db.Text)
    education = db.Column(db.Text)
    skills = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    #one-to-one relationship with user
    user = db.relationship('User', back_populates='jobseeker')

    #one-to-many relationship with job seeker
    fileuploads = db.relationship('Fileupload', back_populates='jobseeker', cascade='all, delete-orphan')
    contact_requests = db.relationship('ContactRequest', back_populates='jobseeker', cascade='all, delete-orphan')

    job_category = db.relationship('JobCategory', back_populates='jobseekers')
    # Association proxy to get employers for this jobseeker through ContactRequest
    employers = association_proxy('contact_requests', 'employer', creator=lambda employer_obj: ContactRequest(employer=employer_obj))
    
    #serialization rules
    serialize_rules = ("-fileuploads.jobseeker", "-contact_requests.jobseeker")

    def __repr__(self):
        return f"<Jobseeker(id={self.id}, user_id={self.user_id})>"

class Employer(db.Model, SerializerMixin):
    __tablename__ = 'employers'
    
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String)
    company_profile = db.Column(db.String)
    verification_status = db.Column(db.Boolean, default=False)
    contact_details = db.Column(db.String)
    pay_to_view = db.Column(db.Boolean)
    history = db.Column(db.String)
    services_offered = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    #one-to-one relationship with user
    user = db.relationship('User', back_populates='employer')

    #Many to one relationship with an employee
    contact_requests = db.relationship('ContactRequest', back_populates='employer', cascade='all, delete-orphan')
    payments = db.relationship('Payment', back_populates='employer', cascade='all, delete-orphan')

    # Association proxy to get jobseekers for this employer through ContactRequest
    jobseekers = association_proxy('contact_requests', 'jobseeker', creator=lambda jobseeker_obj: ContactRequest(jobseeker=jobseeker_obj))

    #serialization rules
    serialize_rules = ("-contact_requests.employer", "-payments.employer")

    def __repr__(self):
        return f"<Employer(id={self.id}, user_id={self.user_id})>"

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    # first_name = db.Column(db.String(64))
    # last_name = db.Column(db.String(64))
    role = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.Integer)
    _password_hash = db.Column(db.String(128), nullable=False)
    verified = db.Column(db.Boolean, default=False)

    # One to one relationship with employer
    employer = db.relationship('Employer', back_populates='user', uselist=False)
    # One to one relationship with jobseeker
    jobseeker = db.relationship('Jobseeker', back_populates='user', uselist=False)
    # One to one relationship with admin
    admin = db.relationship('Admin', back_populates='user', uselist=False)

    #serialization rules
    serialize_rules = ("-jobseeker.user", "-employer.user", "-admin.user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
    
    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes may not be viewed.")
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')
        
    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

class ContactRequest(db.Model, SerializerMixin):
    __tablename__ = 'contactrequests'
    
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('employers.id'))
    jobseeker_id = db.Column(db.Integer, db.ForeignKey('jobseekers.id'))
    message = db.Column(db.String)
    status = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    
    #relationships
    employer = db.relationship('Employer', back_populates='contact_requests')
    jobseeker = db.relationship('Jobseeker', back_populates='contact_requests')

    def __repr__(self):
        return f"<ContactRequest(id={self.id}, employer_id={self.employer_id}, jobseeker_id={self.jobseeker_id})>"

class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('employers.id'), unique=True)
    amount = db.Column(db.Float)
    payment_date = db.Column(db.DateTime)
    payment_status = db.Column(db.Boolean)
    
    #relationship
    employer = db.relationship('Employer', back_populates='payments')

    def __repr__(self):
        return f"<Payment(id={self.id}, employer_id={self.employer_id}, amount={self.amount})>"

class Fileupload(db.Model, SerializerMixin):
    __tablename__ = 'fileuploads'
    
    id = db.Column(db.Integer, primary_key=True)
    jobseeker_id = db.Column(db.Integer, db.ForeignKey('jobseekers.id'))
    file_path = db.Column(db.String)
    file_type = db.Column(db.String)
    uploaded_at = db.Column(db.DateTime)
    
    #relationship
    jobseeker = db.relationship('Jobseeker', back_populates='fileuploads')

    def __repr__(self):
        return f"<Fileupload(id={self.id}, jobseeker_id={self.jobseeker_id}, file_path='{self.file_path}')>"

class JobCategory(db.Model, SerializerMixin):
    __tablename__ = 'jobcategories'
    
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String)
    
    jobseekers = db.relationship('Jobseeker', back_populates='job_category', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<JobCategory(id={self.id}, category_name='{self.category_name}')>"
