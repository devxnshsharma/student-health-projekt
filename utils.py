"""
Utility functions for validation, BMI calculation, and data processing
"""
import re
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def calculate_bmi(height_cm, weight_kg):
    """Calculate BMI and return status"""
    if not height_cm or not weight_kg or height_cm <= 0 or weight_kg <= 0:
        return None, "Invalid measurements"
    
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    
    if bmi < 18.5:
        status = "Underweight"
    elif bmi < 25:
        status = "Normal"
    elif bmi < 30:
        status = "Overweight"
    else:
        status = "Obese"
    
    return round(bmi, 2), status

def validate_date(date_string):
    """Validate date format YYYY-MM-DD"""
    if not date_string:
        return False
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_blood_group(blood_group):
    """Validate blood group format"""
    valid_groups = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
    return blood_group.upper() in valid_groups

def validate_sex(sex):
    """Validate sex field"""
    return sex.upper() in ['M', 'F', 'OTHER']

def validate_age(age):
    """Validate age is reasonable"""
    return 5 <= age <= 25

def validate_vaccination_status(status):
    """Validate vaccination status"""
    return status.upper() in ['Y', 'N']

def validate_admin_no(admin_no):
    """Validate admin number is positive"""
    return admin_no > 0

def validate_vaccination_date(date_string):
    """Validate vaccination date is not in the future"""
    if not validate_date(date_string):
        return False
    date_obj = datetime.strptime(date_string, '%Y-%m-%d')
    return date_obj <= datetime.now()

def sanitize_string(value, max_length=None):
    """Sanitize string input"""
    if not isinstance(value, str):
        return str(value)
    sanitized = value.strip()
    if max_length:
        sanitized = sanitized[:max_length]
    return sanitized

def is_due_for_booster(last_date_string, years_between=5):
    """Check if vaccination is due for booster"""
    if not last_date_string:
        return False
    try:
        last_date = datetime.strptime(last_date_string, '%Y-%m-%d')
        booster_date = last_date + timedelta(days=years_between*365)
        return datetime.now() >= booster_date
    except ValueError:
        return False

def hash_password(password):
    """Hash password using bcrypt (requires bcrypt package)"""
    try:
        import bcrypt
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    except ImportError:
        logger.warning("bcrypt not installed, using plain password (NOT SECURE)")
        return password

def verify_password(password, hashed):
    """Verify password against hash"""
    try:
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except ImportError:
        return password == hashed
