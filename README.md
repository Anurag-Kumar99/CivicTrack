#  CivicTrack – Smart Complaint Management System

CivicTrack is a web-based complaint management system designed to provide a transparent and structured way for citizens to report civic issues and for authorities to resolve them efficiently. The system focuses on real-world workflows, role-based access, and secure data handling.

---

## Features

###  User Module
- User registration with personal and location details
- Raise civic complaints (road, sanitation, water, electricity, etc.)
- Track complaint status in real time
- View complaint history in a clean dashboard

###  Admin Module
- View all registered complaints
- Dashboard with complaint analytics (Total, Pending, Resolved)
- Filter complaints by status
- Assign complaints to employees
- Full system control with role-based authorization

###  Employee Module
- View only assigned complaints
- See complete user details including location
- Accept complaints and update status
- Resolve complaints with proof upload

---

##  Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite (can be upgraded to PostgreSQL/MySQL)
- **Architecture:** MVT (Model–View–Template)
- **Authentication:** Django Authentication System

---

##  Security Features

- Role-based access control (User, Employee, Admin)
- CSRF protection for all POST requests
- Secure session management
- Authentication and authorization using Django

---

##  Project Design Highlights

- Separate `UserProfile` model for storing personal and location data
- Clean separation of authentication and business logic
- Real-world complaint lifecycle (Pending → In Progress → Resolved)
- Scalable and interview-ready project structure

---

##  Project Structure (Simplified)

