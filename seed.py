from config import db
from models import User, Jobseeker, Employer, ContactRequest, Payment, Fileupload, JobCategory, Admin
from flask_bcrypt import generate_password_hash
from app import app  # Import the Flask application instance
from datetime import datetime

def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Create job categories
        category1 = JobCategory(category_name='Software Development')
        category2 = JobCategory(category_name='Marketing')
        category3 = JobCategory(category_name='Sales')
        category4 = JobCategory(category_name='Customer Support')
        db.session.add_all([category1, category2, category3, category4])
        db.session.commit()

        # Create users
        user1 = User(username="Samuel Smith", email="SamuelSmith@gmail.com", role="jobseeker", verified=True)
        user1.password_hash = "password1"
        user2 = User(username="Kimberly Parker", email="Kimberly@gmail.com", role="employer", verified=True)
        user2.password_hash = "password2"
        user3 = User(username="admin_user", email="admin@example.com", role="admin", verified=True)
        user3.password_hash = "password3"
        user4 = User(username="David Brown", email="DavidBrown@gmail.com", role="jobseeker", verified=True)
        user4.password_hash = "password4"
        user5 = User(username="Emily Clark", email="EmilyClark@gmail.com", role="employer", verified=True)
        user5.password_hash = "password5"
        db.session.add_all([user1, user2, user3, user4, user5])
        db.session.commit()

        # Create jobseekers
        jobseeker1 = Jobseeker(
            prof_pic="https://t4.ftcdn.net/jpg/03/64/21/11/360_F_364211147_1qgLVxv1Tcq0Ohz3FawUfrtONzz8nq3e.jpg",
            bio="Software developer with 5 years of experience.",
            availability=True,
            job_category_id=category1.id,
            salary_expectation=60000,
            verification_status=True,
            work_experience="5 years at XYZ Company",
            education="BSc in Computer Science",
            skills="Python, Flask, SQLAlchemy",
            user_id=user1.id
        )
        jobseeker2 = Jobseeker(
            prof_pic="https://img.fixthephoto.com/blog/images/gallery/news_preview_mob_image__preview_11368.png",
            bio="Marketing expert with 3 years of experience.",
            availability=True,
            job_category_id=category2.id,
            salary_expectation=50000,
            verification_status=True,
            work_experience="3 years at ABC Company",
            education="BSc in Marketing",
            skills="SEO, SEM, Content Marketing",
            user_id=user4.id
        )
        db.session.add_all([jobseeker1, jobseeker2])
        db.session.commit()

        # Create employers
        employer1 = Employer(
            company_name="Jane's Tech",
            company_profile="A leading tech company.",
            verification_status=True,
            contact_details="jane@example.com",
            pay_to_view=True,
            history="10 years in the industry",
            services_offered="Software development, consulting",
            user_id=user2.id
        )
        employer2 = Employer(
            company_name="Tech Innovators",
            company_profile="Innovative tech solutions.",
            verification_status=True,
            contact_details="emily@example.com",
            pay_to_view=True,
            history="5 years in the industry",
            services_offered="App development, web development",
            user_id=user5.id
        )
        db.session.add_all([employer1, employer2])
        db.session.commit()

        # Create admin
        admin1 = Admin(
            first_name="Admin",
            last_name="User",
            user_id=user3.id
        )
        db.session.add(admin1)
        db.session.commit()

        # Create contact requests
        contact_request1 = ContactRequest(
            employer_id=employer1.id,
            jobseeker_id=jobseeker1.id,
            message="We would like to offer you a job.",
            status="Pending",
            created_at=datetime.utcnow()
        )
        contact_request2 = ContactRequest(
            employer_id=employer2.id,
            jobseeker_id=jobseeker2.id,
            message="We have a marketing position available.",
            status="Pending",
            created_at=datetime.utcnow()
        )
        db.session.add_all([contact_request1, contact_request2])
        db.session.commit()

        # Create payments
        payment1 = Payment(
            employer_id=employer1.id,
            amount=1000.0,
            payment_date=datetime.utcnow(),
            payment_status=True
        )
        payment2 = Payment(
            employer_id=employer2.id,
            amount=500.0,
            payment_date=datetime.utcnow(),
            payment_status=True
        )
        db.session.add_all([payment1, payment2])
        db.session.commit()

        # Create file uploads
        fileupload1 = Fileupload(
            jobseeker_id=jobseeker1.id,
            file_name="resume.pdf",
            file_type="application/pdf",
            uploaded_at=datetime.utcnow()
        )
        fileupload2 = Fileupload(
            jobseeker_id=jobseeker2.id,
            file_name="portfolio.pdf",
            file_type="application/pdf",
            uploaded_at=datetime.utcnow()
        )
        db.session.add_all([fileupload1, fileupload2])
        db.session.commit()

        print("Database seeded successfully.")

if __name__ == "__main__":
    seed()
