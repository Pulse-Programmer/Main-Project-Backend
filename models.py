from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

class Admin(db.Model, SerializerMixin):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

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
    verification_status = db.Column(db.Boolean)
    work_experience = db.Column(db.Text)
    education = db.Column(db.Text)
    skills = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    #one-to-many relationship with job seeker
    fileuploads = db.relationship('Fileupload', backref='jobseeker', lazy=True)
    contact_requests = db.relationship('ContactRequest', backref='jobseeker', lazy=True)

    #serialization rules
    serialize_rules = ("-fileuploads.jobseeker", "-contact_requests.jobseeker")

    def __repr__(self):
        return f"<Jobseeker(id={self.id}, user_id={self.user_id})>"

class Employer(db.Model, SerializerMixin):
    __tablename__ = 'employers'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String)
    company_profile = db.Column(db.String)
    verification_status = db.Column(db.Boolean)
    contact_details = db.Column(db.String)
    pay_to_view = db.Column(db.Boolean)
    history = db.Column(db.String)
    services_offered = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    #Many to one relationship with an employee
    contact_requests = db.relationship('ContactRequest', backref='employer', lazy=True)
    payments = db.relationship('Payment', backref='employer', lazy=True)

    #serialization rules
    serialize_rules = ("-contact_requests.employer", "-payments.employer")

    def __repr__(self):
        return f"<Employer(id={self.id}, user_id={self.user_id})>"

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    first_name = db.Column(db.String(64))
    sir_name = db.Column(db.String(64))
    role = db.Column(db.String(64))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.Integer)
    password = db.Column(db.String(128), nullable=False)
    verified = db.Column(db.Boolean)

    #Relationships
    jobseeker = db.relationship('Jobseeker', backref='user', uselist=False)
    employer = db.relationship('Employer', backref='user', uselist=False)
    admin = db.relationship('Admin', backref='user', uselist=False)
    contact_requests = db.relationship('ContactRequest', backref='user', lazy=True)
    fileuploads = db.relationship('Fileupload', backref='user', lazy=True)
    payments = db.relationship('Payment', backref='user', lazy=True)

    #serialization rules
    serialize_rules = ("-jobseeker.user", "-employer.user", "-admin.user", "-contact_requests.user", "-fileuploads.user", "-payments.user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

class ContactRequest(db.Model, SerializerMixin):
    __tablename__ = 'contactrequests'
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('employers.id'))
    jobseeker_id = db.Column(db.Integer, db.ForeignKey('jobseekers.id'))
    message = db.Column(db.String)
    status = db.Column(db.String)
    created_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"<ContactRequest(id={self.id}, employer_id={self.employer_id}, jobseeker_id={self.jobseeker_id})>"

class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('employers.id'), unique=True)
    amount = db.Column(db.Float)
    payment_date = db.Column(db.DateTime)
    payment_status = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Payment(id={self.id}, employer_id={self.employer_id}, amount={self.amount})>"

class Fileupload(db.Model, SerializerMixin):
    __tablename__ = 'fileuploads'
    id = db.Column(db.Integer, primary_key=True)
    jobseeker_id = db.Column(db.Integer, db.ForeignKey('jobseekers.id'))
    file_path = db.Column(db.String)
    file_type = db.Column(db.String)
    uploaded_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Fileupload(id={self.id}, jobseeker_id={self.jobseeker_id}, file_path='{self.file_path}')>"

class JobCategory(db.Model, SerializerMixin):
    __tablename__ = 'jobcategories'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String)
    
    jobseekers = db.relationship('Jobseeker', backref='jobcategory', lazy=True)

    def __repr__(self):
        return f"<JobCategory(id={self.id}, category_name='{self.category_name}')>"
