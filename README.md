# CivicTrack – Smart Complaint Management System

CivicTrack is a role-based web application built with Django that helps citizens raise civic complaints and enables government employees and administrators to manage, assign, track, and resolve those complaints efficiently.

The system focuses on transparency, automation, and accountability in civic issue handling.

##  Features
###  User (Citizen)

Register and log in securely

Raise complaints with:

Title & description

Category (Pothole, Garbage, Water Leak, etc.)

Priority (Low / Medium / High)

Department (Road, Water, Electricity, etc.)

Optional image upload

Track complaint status in real time

### Employee

View complaints assigned to their department

Accept and resolve complaints

Upload proof image while resolving

See only relevant complaints (role-based access)

### Admin

View all complaints with analytics

Filter complaints by:

Status

Category

Priority

Auto-assign complaints to employees

Manual assignment if required

Monitor employee workload

Escalation for high-priority unresolved complaints

### Smart Automation

Auto-assignment of complaints to the least-loaded employee based on department

Priority-based sorting (High → Medium → Low)

Escalation system for high-priority complaints not resolved in time

Email notifications on assignment and escalation

Action logs for complaint lifecycle tracking

### Project Architecture

User: Authentication & roles (User / Employee / Admin)

EmployeeProfile: Stores department and workload metadata

Complaint: Core complaint data and workflow

Department: Government departments

Utilities Layer:

Auto-assign logic

Escalation logic

Email notifications

Employee metadata is intentionally separated from User to keep authentication and business logic clean.

### Tech Stack

Backend: Django, Django ORM

Frontend: HTML, Bootstrap

Database: SQLite (can be upgraded to PostgreSQL)

Authentication: Django Auth

Email: Django Email Backend

Security: CSRF protection, role-based access
