# Medical Record Management System - Setup & Implementation Guide

## Overview
A comprehensive student medical record management system with role-based authentication, audit logging, data validation, and advanced analytics.

## Features Implemented

### 1. **Role-Based Authentication**
- Admin authentication with username/password
- Brute-force protection (5 failed attempts → 15-minute lockout)
- Password hashing using bcrypt
- Login attempt tracking
- Password change functionality

### 2. **Security & Data Validation**
- Parameterized SQL queries (prevent SQL injection)
- Field validation: dates, blood groups, sex, age, vaccination status
- Database constraints (CHECK, ENUM, FOREIGN KEY)
- Input sanitization

### 3. **Audit Logging**
- Every create/update/delete operation logged
- Tracks: admin_id, action_type, target_record, timestamp
- Complete audit trail for compliance

### 4. **Admin Features**
- View all student records with search/filter
- Sort by name, age, class, blood group
- Update individual fields with audit trail
- Delete records with confirmation
- Vaccination tracking with dates
- BMI calculation and categorization

### 5. **Analytics & Reports**
- Blood group distribution
- BMI distribution (Underweight/Normal/Overweight/Obese)
- Vaccination coverage percentages
- Class distribution
- Age statistics
- Missing records detection
- CSV export functionality

### 6. **Code Structure**
- `main.py` - Application entry point
- `db.py` - Database connection & schema
- `models.py` - CRUD operations
- `ui.py` - CLI interface
- `utils.py` - Utility functions
- `reports.py` - Analytics module
- `logger_config.py` - Logging configuration
- `test_health.py` - Unit tests

---

## Installation & Setup

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Environment Configuration**
Copy `.env.example` to `.env` and update:
```bash
cp .env.example .env
```

Edit `.env`:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=MedRep
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
ADMIN_OTP_SECRET=0001
```

### 3. **Create MySQL Database**
```sql
CREATE DATABASE MedRep;
```

### 4. **Run Application**
```bash
python main.py
```

---

## Usage Guide

### Admin Account Setup
When the application starts, you need to create an admin account:
1. Run `python main.py`
2. Admin credentials are created via database insert:

```python
# Create initial admin (run once):
from models import AdminAuth
AdminAuth.create_admin('admin', 'SecurePassword123!', 'Admin Name', 'admin@example.com', 'Admin')
```

### Admin Login
- Username/Password authentication
- Lockout after 5 failed attempts (15 minutes)
- Change password from admin menu

### Student Registration
- Enter all personal details
- Medical information (height, weight, blood group)
- Vaccination history with dates

### Student Login
- View own medical record
- See BMI calculation
- View vaccination history

### Admin Dashboard Features
1. **View Records** - Search by AdminNo, Name, or Class
2. **Sort Records** - Sort by Name, Age, Class, Blood Group
3. **Update Records** - Modify any field with audit tracking
4. **Delete Records** - Remove with confirmation
5. **Vaccination Alerts** - Due for boosters, missing vaccinations
6. **Allergy Search** - Find students with specific allergies
7. **Reports** - Analytics and statistics
8. **Audit Logs** - View all administrative changes

---

## Database Schema

### admins table
- AdminID (Primary Key)
- Username (Unique)
- PasswordHash
- FullName
- Email
- Role (SuperAdmin, Admin, Viewer)
- IsActive
- LoginAttempts (Brute-force protection)
- LockedUntil (Lockout timestamp)
- LastLogin
- CreatedAt, UpdatedAt

### users table
- AdminNo (Primary Key)
- Sname

### records table
- AdminNo (Primary Key)
- Personal info (Sname, Sex, Age, DoB, etc.)
- Physical measurements (Height, Weight, BloodGroup)
- Allergies
- Vaccination records with dates
- Timestamps (CreatedAt, UpdatedAt)
- CHECK constraints on Age, Height, Weight
- ENUM constraints on Sex, Vaccination status

### audit_log table
- LogID (Primary Key)
- AdminID (Foreign Key)
- TargetAdminNo
- ActionType (CREATE, UPDATE, DELETE, LOGIN, PASSWORD_CHANGE)
- ChangedFields (JSON)
- OldValues (JSON)
- NewValues (JSON)
- IPAddress
- CreatedAt

---

## Testing

Run unit tests:
```bash
pytest test_health.py -v
```

Tests cover:
- BMI calculation (all categories)
- Date validation
- Blood group validation
- Age validation
- Vaccination booster logic
- Invalid input handling

---

## Logging

Logs are written to:
- Console (INFO level and above)
- `logs/app_YYYYMMDD.log` (DEBUG level and above)

Log rotation occurs at 10MB per file, keeping 5 backups.

---

## Security Considerations

✓ SQL injection prevention via parameterized queries
✓ Password hashing with bcrypt
✓ Brute-force protection (login attempt limits)
✓ Audit logging for accountability
✓ Input validation and sanitization
✓ Database constraints (CHECK, ENUM)
✓ Role-based access control ready
✓ Environment variable configuration (no hardcoded secrets)

---

## Future Enhancements

- [ ] OTP via email/SMS
- [ ] Security questions for password reset
- [ ] 2FA implementation
- [ ] API endpoints (REST/GraphQL)
- [ ] Web UI (Flask/Django)
- [ ] Batch import from CSV
- [ ] Advanced analytics dashboard
- [ ] Medical alerts/notifications

---

