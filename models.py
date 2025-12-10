"""
Models and database operations for users, records, and admins
"""
import pymysql as sql
from datetime import datetime
import logging
from utils import (
    validate_date, validate_blood_group, validate_sex, validate_age,
    validate_vaccination_status, validate_admin_no, hash_password, verify_password
)
from db import create_connection, log_audit

logger = logging.getLogger(__name__)

class StudentRecords:
    """Handle student record operations"""
    
    @staticmethod
    def create_user(admin_no, student_name):
        """Create a new user"""
        try:
            if not validate_admin_no(admin_no):
                return False, "Invalid Admin No."
            
            conn = create_connection()
            cr = conn.cursor()
            cr.execute(
                "INSERT INTO users (AdminNo, Sname) VALUES (%s, %s)",
                (admin_no, student_name)
            )
            conn.commit()
            cr.close()
            conn.close()
            return True, "User created successfully"
        except sql.IntegrityError:
            logger.warning(f"Duplicate Admin No.: {admin_no}")
            return False, "Admin No. already exists"
        except sql.Error as e:
            logger.error(f"Error creating user: {e}")
            return False, str(e)
    
    @staticmethod
    def create_record(admin_no, student_data):
        """Create a complete student record with validation"""
        try:
            # Validate all fields
            if not validate_admin_no(admin_no):
                return False, "Invalid Admin No."
            if not validate_sex(student_data['sex']):
                return False, "Invalid sex value (M/F/Other)"
            if not validate_age(student_data['age']):
                return False, "Age must be between 5 and 25"
            if not validate_date(student_data['dob']):
                return False, "Invalid date format for DoB (YYYY-MM-DD)"
            if not validate_blood_group(student_data['blood_group']):
                return False, "Invalid blood group"
            
            conn = create_connection()
            cr = conn.cursor()
            
            cr.execute("""
                INSERT INTO records VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                admin_no,
                student_data['name'],
                student_data['sex'].upper(),
                student_data.get('mother_name'),
                student_data.get('father_name'),
                student_data['age'],
                student_data['class_sec'],
                student_data['dob'],
                student_data['blood_group'].upper(),
                student_data.get('height'),
                student_data.get('weight'),
                student_data.get('allergies'),
                student_data.get('tetanus', 'N'),
                student_data.get('tetanus_date'),
                student_data.get('cholera', 'N'),
                student_data.get('cholera_date'),
                student_data.get('typhoid', 'N'),
                student_data.get('typhoid_date'),
                student_data.get('hep_a', 'N'),
                student_data.get('hep_a_date'),
                student_data.get('hep_b', 'N'),
                student_data.get('hep_b_date'),
                student_data.get('chicken_pox', 'N'),
                student_data.get('chicken_pox_date'),
                student_data.get('measles', 'N'),
                student_data.get('measles_date'),
                student_data.get('covid', 'N'),
                student_data.get('covid_date'),
                student_data.get('other_info')
            ))
            
            conn.commit()
            cr.close()
            conn.close()
            return True, "Record created successfully"
        except sql.Error as e:
            logger.error(f"Error creating record: {e}")
            return False, str(e)
    
    @staticmethod
    def get_record(admin_no):
        """Get a student record"""
        try:
            conn = create_connection()
            cr = conn.cursor()
            cr.execute("SELECT * FROM records WHERE AdminNo = %s", (admin_no,))
            record = cr.fetchone()
            cr.close()
            conn.close()
            return record
        except sql.Error as e:
            logger.error(f"Error retrieving record: {e}")
            return None
    
    @staticmethod
    def get_all_records():
        """Get all student records"""
        try:
            conn = create_connection()
            cr = conn.cursor()
            cr.execute("SELECT * FROM records")
            records = cr.fetchall()
            cr.close()
            conn.close()
            return records
        except sql.Error as e:
            logger.error(f"Error retrieving records: {e}")
            return []
    
    @staticmethod
    def search_records(field, value):
        """Search records by field"""
        try:
            conn = create_connection()
            cr = conn.cursor()
            
            if field == "name":
                cr.execute("SELECT * FROM records WHERE Sname LIKE %s", (f"%{value}%",))
            elif field == "class":
                cr.execute("SELECT * FROM records WHERE ClassSec = %s", (value,))
            elif field == "admin_no":
                cr.execute("SELECT * FROM records WHERE AdminNo = %s", (value,))
            else:
                return []
            
            records = cr.fetchall()
            cr.close()
            conn.close()
            return records
        except sql.Error as e:
            logger.error(f"Error searching records: {e}")
            return []
    
    @staticmethod
    def update_record(admin_no, admin_id, **kwargs):
        """Update a student record with audit logging"""
        try:
            # Get old values for audit
            old_record = StudentRecords.get_record(admin_no)
            if not old_record:
                return False, "Record not found"
            
            conn = create_connection()
            cr = conn.cursor()
            
            # Build update query
            updates = []
            params = []
            changed_fields = []
            
            valid_fields = {
                'height': 'Height', 'weight': 'Weight', 'class_sec': 'ClassSec',
                'allergies': 'Allergies', 'tetanus': 'Tetanus', 'tetanus_date': 'TetanusDate',
                'cholera': 'Cholera', 'cholera_date': 'CholeraDate',
                'typhoid': 'Typhoid', 'typhoid_date': 'TyphoidDate',
                'hep_a': 'HepA', 'hep_a_date': 'HepADate',
                'hep_b': 'HepB', 'hep_b_date': 'HepBDate',
                'chicken_pox': 'ChickenPox', 'chicken_pox_date': 'ChickenPoxDate',
                'measles': 'Measles', 'measles_date': 'MeaslesDate',
                'covid': 'COVID', 'covid_date': 'COVIDDate',
                'other_info': 'AnyOther'
            }
            
            for key, value in kwargs.items():
                if key in valid_fields:
                    updates.append(f"{valid_fields[key]} = %s")
                    params.append(value)
                    changed_fields.append(key)
            
            if not updates:
                return False, "No valid fields to update"
            
            params.append(admin_no)
            query = "UPDATE records SET " + ", ".join(updates) + " WHERE AdminNo = %s"
            cr.execute(query, params)
            
            # Log audit
            log_audit(admin_id, 'UPDATE', admin_no, changed_fields)
            
            conn.commit()
            cr.close()
            conn.close()
            return True, "Record updated successfully"
        except sql.Error as e:
            logger.error(f"Error updating record: {e}")
            return False, str(e)
    
    @staticmethod
    def delete_record(admin_no, admin_id):
        """Delete a student record with audit logging"""
        try:
            conn = create_connection()
            cr = conn.cursor()
            
            # Log audit before deletion
            log_audit(admin_id, 'DELETE', admin_no)
            
            cr.execute("DELETE FROM records WHERE AdminNo = %s", (admin_no,))
            cr.execute("DELETE FROM users WHERE AdminNo = %s", (admin_no,))
            
            conn.commit()
            cr.close()
            conn.close()
            return True, "Record deleted successfully"
        except sql.Error as e:
            logger.error(f"Error deleting record: {e}")
            return False, str(e)

class AdminAuth:
    """Handle admin authentication and authorization"""
    
    @staticmethod
    def create_admin(username, password, full_name, email, role='Admin'):
        """Create a new admin user"""
        try:
            hashed_password = hash_password(password)
            conn = create_connection()
            cr = conn.cursor()
            
            cr.execute("""
                INSERT INTO admins (Username, PasswordHash, FullName, Email, Role, IsActive)
                VALUES (%s, %s, %s, %s, %s, TRUE)
            """, (username, hashed_password, full_name, email, role))
            
            conn.commit()
            cr.close()
            conn.close()
            logger.info(f"Admin created: {username}")
            return True, "Admin created successfully"
        except sql.IntegrityError:
            logger.warning(f"Username already exists: {username}")
            return False, "Username already exists"
        except sql.Error as e:
            logger.error(f"Error creating admin: {e}")
            return False, str(e)
    
    @staticmethod
    def authenticate(username, password):
        """Authenticate admin user with brute-force protection"""
        try:
            conn = create_connection()
            cr = conn.cursor()
            
            cr.execute("""
                SELECT AdminID, PasswordHash, LockedUntil, IsActive 
                FROM admins WHERE Username = %s
            """, (username,))
            
            admin = cr.fetchone()
            
            if not admin:
                cr.close()
                conn.close()
                return None, "Invalid credentials"
            
            admin_id, hashed_password, locked_until, is_active = admin
            
            # Check if account is locked
            if locked_until:
                from datetime import datetime
                if datetime.now() < locked_until:
                    cr.close()
                    conn.close()
                    return None, "Account is locked. Try again later."
                else:
                    # Unlock the account
                    cr.execute("UPDATE admins SET LoginAttempts = 0, LockedUntil = NULL WHERE AdminID = %s", (admin_id,))
            
            if not is_active:
                cr.close()
                conn.close()
                return None, "Account is inactive"
            
            # Verify password
            if verify_password(password, hashed_password):
                # Reset login attempts on successful login
                cr.execute("""
                    UPDATE admins 
                    SET LoginAttempts = 0, LastLogin = NOW() 
                    WHERE AdminID = %s
                """, (admin_id,))
                conn.commit()
                cr.close()
                conn.close()
                logger.info(f"Admin authenticated: {username}")
                return admin_id, "Authentication successful"
            else:
                # Increment login attempts
                cr.execute("""
                    SELECT LoginAttempts FROM admins WHERE AdminID = %s
                """, (admin_id,))
                attempts = cr.fetchone()[0] + 1
                
                # Lock after 5 failed attempts
                if attempts >= 5:
                    from datetime import datetime, timedelta
                    lock_until = datetime.now() + timedelta(minutes=15)
                    cr.execute("""
                        UPDATE admins 
                        SET LoginAttempts = %s, LockedUntil = %s 
                        WHERE AdminID = %s
                    """, (attempts, lock_until, admin_id))
                    logger.warning(f"Account locked after failed attempts: {username}")
                else:
                    cr.execute("""
                        UPDATE admins SET LoginAttempts = %s WHERE AdminID = %s
                    """, (attempts, admin_id))
                
                conn.commit()
                cr.close()
                conn.close()
                return None, f"Invalid credentials ({5 - attempts} attempts remaining)"
        except sql.Error as e:
            logger.error(f"Error authenticating admin: {e}")
            return None, str(e)
    
    @staticmethod
    def change_password(admin_id, old_password, new_password):
        """Change admin password"""
        try:
            conn = create_connection()
            cr = conn.cursor()
            
            cr.execute("SELECT PasswordHash FROM admins WHERE AdminID = %s", (admin_id,))
            result = cr.fetchone()
            
            if not result:
                return False, "Admin not found"
            
            if not verify_password(old_password, result[0]):
                return False, "Current password is incorrect"
            
            hashed_new = hash_password(new_password)
            cr.execute("""
                UPDATE admins SET PasswordHash = %s WHERE AdminID = %s
            """, (hashed_new, admin_id))
            
            log_audit(admin_id, 'PASSWORD_CHANGE', admin_id)
            
            conn.commit()
            cr.close()
            conn.close()
            logger.info(f"Password changed for admin: {admin_id}")
            return True, "Password changed successfully"
        except sql.Error as e:
            logger.error(f"Error changing password: {e}")
            return False, str(e)
