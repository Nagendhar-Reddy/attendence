# Attendance Management System

## Overview

The Attendance Management System is a web application designed for managing employee shifts, weekly offs, and attendance. It allows employees to view and request shift changes, mark attendance with a webcam, and allows managers to manage shifts, approve shift changes, and view attendance records.

## Setup and Running the Application

### Prerequisites

1. **Python 3.8 or higher**
2. **Django 4.0 or higher**
3. **Django REST framework**
4. **PostgreSQL or another supported database**
5. **Django REST Framework Simple JWT for authentication**


### Installation Steps

1. **create virtual envinorment**
  python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`


2. **Install Dependencies**
pip install -r requirements.txt



3. **Apply Migrations**
pip install -r requirements.txt


4. **Run Development Server**
python manage.py runserver


API Endpoints
User Management
Create User: POST /api/create_user/
Update User: PUT /api/update_user/<int:user_id>/
Shift Management
Create Shift: POST /api/create_shift/
View Shifts: GET /api/view_shifts/
Attendance Management
Mark Attendance: POST /api/mark_attendance/
View Attendance: GET /api/view_attendance/
Weekly Off Management
Set Weekly Off: POST /api/set_weekly_off/
Shift Change Management
Request Shift Change: POST /api/request_shift_change/
Approve/Reject Shift Change: POST /api/approve_reject_shift_change/








