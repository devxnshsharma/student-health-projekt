# API Reference & Code Examples

## Core Modules

### 1. models.py - Database Operations

#### StudentRecords Class

```python
from models import StudentRecords

# Create a new user
success, msg = StudentRecords.create_user(
    admin_no=101,
    student_name="John Doe"
)

# Get a single record
record = StudentRecords.get_record(admin_no=101)

# Get all records
all_records = StudentRecords.get_all_records()

# Search records
results = StudentRecords.search_records(field="name", value="John")
# field can be: "name", "class", "admin_no"

# Update record (with audit logging)
success, msg = StudentRecords.update_record(
    admin_no=101,
    admin_id=1,  # Admin making the change
    height=175.5,
    weight=70.0,
    allergies="Penicillin"
)

# Delete record (with audit logging)
success, msg = StudentRecords.delete_record(
    admin_no=101,
    admin_id=1  # Admin making the change
)
```

#### AdminAuth Class

```python
from models import AdminAuth

# Create new admin user
success, msg = AdminAuth.create_admin(
    username="john_admin",
    password="SecurePass123!",
    full_name="John Administrator",
    email="john@admin.com",
    role="Admin"  # "SuperAdmin", "Admin", "Viewer"
)

# Authenticate admin
admin_id, msg = AdminAuth.authenticate(
    username="john_admin",
    password="SecurePass123!"
)

# Change password
success, msg = AdminAuth.change_password(
    admin_id=1,
    old_password="OldPass123!",
    new_password="NewPass456!"
)
```

### 2. utils.py - Utility Functions

#### Validation Functions

```python
from utils import (
    calculate_bmi, validate_date, validate_blood_group,
    validate_sex, validate_age, is_due_for_booster
)

# BMI Calculation
bmi, status = calculate_bmi(height_cm=170, weight_kg=65)
# Returns: (23.43, "Normal")

# Date validation
is_valid = validate_date("2024-12-10")  # True
is_valid = validate_date("12-10-2024")   # False

# Blood group validation
is_valid = validate_blood_group("O+")    # True
is_valid = validate_blood_group("C+")    # False

# Sex validation
is_valid = validate_sex("M")             # True
is_valid = validate_sex("F")             # True

# Age validation (must be 5-25)
is_valid = validate_age(15)              # True
is_valid = validate_age(30)              # False

# Vaccination booster check
is_due = is_due_for_booster("2019-06-15", years_between=5)
# Returns True if more than 5 years have passed
```

### 3. reports.py - Analytics

```python
from reports import ReportsAnalytics

# Blood group distribution
data = ReportsAnalytics.blood_group_distribution()
# Returns: [(('O+', 25), ('A+', 18), ('B+', 12), ...)]

# BMI distribution
data = ReportsAnalytics.bmi_distribution()
# Returns: {'Underweight': 5, 'Normal': 45, 'Overweight': 8, 'Obese': 2}

# Vaccination coverage percentages
data = ReportsAnalytics.vaccination_coverage()
# Returns: {'Tetanus': 95.5, 'COVID': 87.3, ...}

# Class distribution
data = ReportsAnalytics.class_distribution()
# Returns: [(('10A', 30), ('10B', 28), ...)]

# Age statistics
data = ReportsAnalytics.age_statistics()
# Returns: {'min': 8, 'max': 17, 'avg': 12.3, 'total': 150}

# Find incomplete records
missing = ReportsAnalytics.missing_records()
# Returns: [(101, 'John', 1, 0, 1), ...]  # AdminNo, Name, MissingHeight, Weight, Allergies

# Export to CSV
filename = ReportsAnalytics.export_report_csv(report_type='comprehensive')
# report_type: 'comprehensive', 'health'
```

### 4. db.py - Database Layer

```python
from db import create_connection, log_audit, get_audit_logs

# Create connection
conn = create_connection()
cr = conn.cursor()
# ... use cursor ...
cr.close()
conn.close()

# Log audit action
log_audit(
    admin_id=1,
    action_type='UPDATE',  # 'CREATE', 'UPDATE', 'DELETE', 'LOGIN', 'PASSWORD_CHANGE'
    target_admin_no=101,
    changed_fields=['height', 'weight'],
    old_values={'height': 170, 'weight': 70},
    new_values={'height': 175, 'weight': 72},
    ip_address='192.168.1.100'
)

# Get audit logs
logs = get_audit_logs(limit=50)
for log in logs:
    print(f"LogID: {log[0]}, Admin: {log[1]}, Action: {log[2]}, Time: {log[4]}")
```

## Usage Examples

### Example 1: Complete Student Registration Flow

```python
from models import StudentRecords

# Student data
student_data = {
    'name': 'Alice Johnson',
    'sex': 'F',
    'mother_name': 'Jane Johnson',
    'father_name': 'Bob Johnson',
    'age': 14,
    'class_sec': '9A',
    'dob': '2010-05-15',
    'blood_group': 'O+',
    'height': 165.0,
    'weight': 55.0,
    'allergies': 'Shellfish',
    'tetanus': 'Y',
    'tetanus_date': '2023-06-15',
    'hep_b': 'Y',
    'hep_b_date': '2023-03-20',
    'covid': 'Y',
    'covid_date': '2024-01-10',
}

# Create user first
success, msg = StudentRecords.create_user(101, student_data['name'])
if success:
    # Create record
    success, msg = StudentRecords.create_record(101, student_data)
    print(msg)
```

### Example 2: Admin Report Generation

```python
from reports import ReportsAnalytics

# Generate comprehensive health report
print("=== Health Statistics Report ===\n")

# Age stats
stats = ReportsAnalytics.age_statistics()
print(f"Age Range: {stats['min']} - {stats['max']} years")
print(f"Average Age: {stats['avg']} years")
print(f"Total Students: {stats['total']}\n")

# BMI distribution
bmi_dist = ReportsAnalytics.bmi_distribution()
print("BMI Distribution:")
for category, count in bmi_dist.items():
    print(f"  {category}: {count} students")

# Vaccination coverage
vacc_cov = ReportsAnalytics.vaccination_coverage()
print("\nVaccination Coverage:")
for vaccine, percentage in vacc_cov.items():
    print(f"  {vaccine}: {percentage}%")

# Export
filename = ReportsAnalytics.export_report_csv('comprehensive')
print(f"\nReport exported to: {filename}")
```

### Example 3: Admin Authentication with Audit

```python
from models import AdminAuth
from db import log_audit

# Login
admin_id, msg = AdminAuth.authenticate("john_admin", "password123")

if admin_id:
    print(f"Welcome Admin {admin_id}")
    
    # Log the successful login
    log_audit(
        admin_id=admin_id,
        action_type='LOGIN',
        ip_address='192.168.1.100'
    )
    
    # Change password
    success, msg = AdminAuth.change_password(
        admin_id=admin_id,
        old_password="password123",
        new_password="newpassword456"
    )
    print(msg)
```

## Testing Examples

```python
import pytest
from utils import calculate_bmi, validate_date

def test_bmi_calculation():
    """Test BMI calculation"""
    bmi, status = calculate_bmi(170, 65)
    assert 22 <= bmi <= 23
    assert status == "Normal"

def test_date_validation():
    """Test date validation"""
    assert validate_date("2024-12-10") == True
    assert validate_date("invalid") == False

# Run tests
pytest test_health.py -v
```

## Error Handling

```python
from models import StudentRecords
import logging

logger = logging.getLogger(__name__)

try:
    success, message = StudentRecords.create_record(admin_no, student_data)
    if not success:
        logger.warning(f"Failed to create record: {message}")
        print(f"Error: {message}")
    else:
        logger.info(f"Record created successfully for admin {admin_no}")
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    print("An unexpected error occurred")
```

## Database Schema Quick Reference

### admins table columns
- AdminID, Username, PasswordHash, FullName, Email, Role, IsActive, LoginAttempts, LockedUntil, LastLogin, CreatedAt, UpdatedAt

### records table columns
- AdminNo, Sname, Sex, Mname, Fname, Age, ClassSec, DoB, BloodGroup, Height, Weight, Allergies
- Tetanus, TetanusDate, Cholera, CholeraDate, Typhoid, TyphoidDate
- HepA, HepADate, HepB, HepBDate, ChickenPox, ChickenPoxDate
- Measles, MeaslesDate, COVID, COVIDDate, AnyOther
- CreatedAt, UpdatedAt

### audit_log table columns
- LogID, AdminID, TargetAdminNo, ActionType, ChangedFields, OldValues, NewValues, IPAddress, CreatedAt

