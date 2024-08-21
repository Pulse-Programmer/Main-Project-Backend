# Overview

This is is a platform designed to bridge the gap between job seekers and employers by providing a space where employers can browse through verified profiles of potential candidates without publicly advertising vacancies. This app is akin to LinkedIn but with a specific focus on direct employer-job seeker interactions, ensuring that only qualified candidates are contacted, thus streamlining the recruitment process. It is a Flask-based web application configured with PostgreSQL, integrating several libraries to facilitate user authentication, email notifications, API documentation, and more.

## Problem statement

Many employers, especially those in private companies, prefer not to publicly advertise open positions. This is due to concerns over the time-consuming process of sorting through numerous applications and the perception that advertising certain positions might reflect poorly on the company. Currently, no dedicated platform exists that allows employers to browse through verified job-seeker profiles without the need for public job postings.

## Minimum Viable Product (MVP)

The MVP for this project includes the following features:

- User Management:

-- Admin: Approve files uploaded by users, general administration.
-- Jobseeker: Upload and update profile, verify profile, manage availability, job category, and salary expectations.
-- Employer: View jobseeker profiles, verify their status to view profiles, and contact jobseekers.

- Authentication:

-- Login using username, email, or phone number.
-- Privilege-based access for jobseekers, employers, and admins.

- Notifications & Communication:

-- Email notifications for activities, including payments and job offers.
-- Push notifications for the Android app.

- Payment Integration:

-- Integration with Safaricom Daraja API for employer payments.

## Features

### Jobseeker

- **Profile Management**: Update personal information, upload qualification files, and verify profiles.
- **Searchable Profiles**: Employers can search for jobseekers based on specific criteria.
- **Notifications**: Receive notifications for new messages and offers.

### Employer

- **Search & Filter**: Search for jobseekers who meet specific job criteria.
- **Contact Management**: Contact jobseekers directly after viewing their profiles.
- **Payments**: Pay a fee to access the jobseeker profiles and additional services.

### Admin

- **User Management**: Oversee and manage user accounts, approve file uploads.
- **Payment Oversight**: Monitor and manage payments made by employers.

## API Endpoints

### User Authentication

- **POST `/login`**: Authenticate users.
- **POST `/signup`**: Register a new user.
- **POST `/logout`**: Logout the current user.

### Jobseekers

- **GET `/jobseekers`**: Retrieve all jobseekers (restricted to verified employers/admins).
- **POST `/jobseekers`**: Create a new jobseeker profile.
- **GET `/jobseekers/:id`**: Get details of a specific jobseeker.
- **PATCH `/jobseekers/:id`**: Update a jobseeker profile.
- **DELETE `/jobseekers/:id`**: Delete a jobseeker profile.

### Employers

- **GET `/employers`**: Retrieve all employers (restricted to admins).
- **POST `/employers`**: Create a new employer profile.
- **GET `/employers/:id`**: Get details of a specific employer.
- **PATCH `/employers/:id`**: Update an employer profile.
- **DELETE `/employers/:id`**: Delete an employer profile.

### Payments

- **GET `/payments`**: Retrieve all payment records (restricted to admins).
- **POST `/payments`**: Create a new payment record.

### Contact Requests

- **GET `/contact_requests`**: Retrieve all contact requests (restricted to admins).
- **POST `/contact_requests`**: Create a new contact request.
- **GET `/contact_requests/:id`**: Get details of a specific contact request.
- **PATCH `/contact_requests/:id`**: Update a contact request.

## Technologies Used

- **Backend**: Python Flask
- **Database**: PostgreSQL
- **Libraries**:
  - Flask-Mail
  - Flask-Migrate
  - Flask-Bcrypt
  - Flask-CORS
  - Flask-RESTful
  - Flasgger (Swagger documentation)
- **Environment Variables Management**: python-dotenv
- **Testing**: Jest, Minitest
- **Frontend**: ReactJs, Redux Toolkit for state management
- **Wireframing**: Figma

## Configuration Details

- **Database Configuration**: The application uses PostgreSQL, and the database URI is securely stored as a secret in GitHub Secrets.
- **Mail Configuration**: Flask-Mail is configured to send emails using Gmail's SMTP server.
- **Environment Variables**: Managed using `dotenv` for database and mail settings.
- **Routes**: The application has routes for user authentication and session management, including signup, login, logout, and session check.
- **CORS**: Configured with support for credentials.

## Contributors

- **Stephen Ochieng** - Repository Owner
- **Lynelle Wanja** - Contributor
- **Victor Wangari** - Contributor
- **Edward Kariu** - Contributor
- **Mike Muigai** - Contributor

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

- Python 3.x
- PostgreSQL
- Node.js (for the frontend)

### Installation

1. **Clone the repository**:

   ```bash
   git clone git@github.com:Pulse-Programmer/Main-Project-Frontend.git
   git clone git@github.com:Pulse-Programmer/Main-Project-Backend.git
   ```
