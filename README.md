
# Appointment Scheduling and Management System

## 1. Project Description

The Appointment Scheduling and Management System is a web-based application developed using Python, Flask, and MariaDB.

It allows customers to register, log in, view available services, book appointments, view appointment records, and cancel pending appointments.

Administrators can log in, view customer appointments, search appointment records, and approve or reject booking requests.

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
- Search appointments by customer name, email, service, or status
- Approve appointment requests
- Reject appointment requests
- View appointment statuses

## 4. Object-Oriented Programming Concepts

### Encapsulation

Private attributes and properties are used to protect object data and validate values.

Examples include the private attributes and property setters in the User, Service, and Appointment classes.

### Abstraction

The User abstract class defines a common structure and an abstract dashboard message method.

### Inheritance

Customer and Admin classes inherit from the User class.

### Polymorphism

Customer and Admin provide their own implementations of the dashboard message method.

AuthService calls the overridden method without checking the specific child class.

### Composition

AppointmentManager manages and stores Appointment objects.

It can add, find, cancel, and count appointments.

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

For example, when a customer creates an appointment:

1. The appointment record is inserted into the appointments table.
2. An activity record is inserted into appointment_logs.
3. Both operations are committed together.
4. If an error occurs, the transaction is rolled back.

The cancellation feature also uses a transaction:

1. The appointment status is updated to cancelled.
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

The project currently contains 43 unit tests, all of which pass.

## 10. Version Control

Git is used to track project development and maintain version history.

Multiple commits document the development of the system, including:

- Initial project setup
- Project documentation
- Appointment search functionality
- Polymorphism implementation and testing
- Appointment manager improvements and unit tests

## 11. Screenshots

Screenshots of the working application will be included as evidence of system functionality.

Suggested screenshots:

- Homepage
- Customer registration and login
- Customer dashboard
- Appointment booking form
- Customer appointment history
- Admin dashboard
- Appointment search results
- Appointment approval and rejection
- Successful unit test execution

## 12. AI Assistance Disclosure

AI assistance was used to support programming explanations, debugging, code review, and development guidance.

The project developer reviewed, tested, and adapted the code during implementation.

## 13. Project Developers

## 13. Project Developers

This project was developed by a group of three students:

| Name | Roles and Contributions |
|---|---|
| **Jamie Robedillo** | Led the system development, implemented its features, conducted testing, and prepared the project documentation. |
| **Ace Redilla** | Helped plan the project and organized the code by placing it into the appropriate project files. |
| **Iggyboy Natividad** | Helped plan the project and contributed to the system's code development. |

**Course:** CSDF101 – Object-Oriented Programming in Python