
# Appointment Scheduling and Management System

## 1. Project Description

The Appointment Scheduling and Management System is a web-based application developed using Python, Flask, and MariaDB.

It allows customers to register, log in, view available services, book appointments, view appointment records, and cancel pending appointments.

Administrators can log in, view customer appointments, and approve or reject booking requests.

## 2. Technologies Used

- Python
- Flask
- MariaDB
- HTML
- CSS
- Jinja2
- Git
- Visual Studio Code

## 3. System Features

### Customer Features
- Customer registration and login
- Secure password hashing
- View available services
- Book appointments
- Automatic appointment end-time calculation
- Business-hours validation
- Appointment conflict checking
- View appointment history
- Cancel pending appointments

### Administrator Features
- Administrator login
- View all customer appointments
- View customer information
- Approve appointment requests
- Reject appointment requests
- View appointment statuses

## 4. Object-Oriented Programming Concepts

### Encapsulation
Private attributes and properties are used to protect object data and validate values.

### Abstraction
The User abstract class defines a common structure and an abstract dashboard method.

### Inheritance
Customer and Admin classes inherit from the User class.

### Polymorphism
Customer and Admin provide their own implementations of the dashboard message method.

### Composition
AppointmentManager manages and stores Appointment objects.

## 5. Database Design

The system uses MariaDB with five main tables:

1. users
2. services
3. appointments
4. business_hours
5. appointment_logs

Primary keys and foreign keys establish relationships between the tables.

## 6. Project Architecture

- models/ - Contains application classes and data models.
- repositories/ - Handles database operations and SQL queries.
- services/ - Contains application business logic.
- exceptions/ - Contains custom application exceptions.
- database/ - Contains database connection and SQL files.
- templates/ - Contains HTML pages.
- static/ - Contains static resources.
- tests/ - Contains unit tests.

## 7. Database Transactions

The system uses database transactions to ensure that related operations are completed together.

For example, when a customer cancels an appointment:

1. The appointment status is updated.
2. A cancellation record is inserted into appointment_logs.
3. Both operations are committed together.
4. If an error occurs, the transaction is rolled back.

## 8. Installation and Setup

### Requirements
- Python
- XAMPP or MariaDB Server
- Git
- Visual Studio Code

### Installation

1. Clone or copy the project folder.
2. Open the project directory in Visual Studio Code.
3. Create a virtual environment:

   python -m venv venv

4. Activate the virtual environment:

   .\venv\Scripts\Activate.ps1

5. Install dependencies:

   pip install -r requirements.txt

6. Create a MariaDB database named:

   appointment_python_db

7. Import the following SQL files through phpMyAdmin:

   - database/schema.sql
   - database/business_hours.sql
   - database/services.sql

8. Create a .env file using .env.example as a guide.
9. Configure the database credentials in .env.
10. Run the application:

    python app.py

11. Open the application in your browser:

    http://127.0.0.1:5000

## 9. Running Unit Tests

Run the following command in the project terminal:

python -m unittest discover -s tests -v

The project currently contains 33 unit tests.

## 10. Version Control

Git is used to track project development and maintain version history.

The initial project version has been saved using Git.

## 11. Project Developers

Project Members:
- Jamie Robedillo
- Add other group members here

Course: CSDF101 - Object-Oriented Programming in Python
Project: Appointment Scheduling and Management System
