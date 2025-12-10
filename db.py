"""
Database connection and schema management
"""
import pymysql as sql
import logging
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'passwd': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'MedRep')
}

def create_connection():
    """Create and return database connection"""
    try:
        conn = sql.connect(**DB_CONFIG)
        return conn
    except sql.Error as e:
        logger.error(f"Database connection error: {e}")
        raise

def create_tables():
    """Create all necessary tables"""
    try:
        conn = create_connection()
        cr = conn.cursor()
        
        # Admins table with role-based auth
        cr.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                AdminID INT AUTO_INCREMENT PRIMARY KEY,
                Username VARCHAR(50) UNIQUE NOT NULL,
                PasswordHash VARCHAR(255) NOT NULL,
                FullName VARCHAR(100),
                Email VARCHAR(100),
                Role ENUM('SuperAdmin', 'Admin', 'Viewer') DEFAULT 'Admin',
                IsActive BOOLEAN DEFAULT TRUE,
                LoginAttempts INT DEFAULT 0,
                LockedUntil DATETIME,
                LastLogin DATETIME,
                CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        
        # Users table
        cr.execute("""
            CREATE TABLE IF NOT EXISTS users (
                AdminNo INT PRIMARY KEY,
                Sname VARCHAR(25) NOT NULL
            )
        """)
        
        # Records table with constraints
        cr.execute("""
            CREATE TABLE IF NOT EXISTS records (
                AdminNo INT PRIMARY KEY,
                Sname VARCHAR(25) NOT NULL,
                Sex ENUM('M', 'F', 'Other') NOT NULL,
                Mname VARCHAR(20),
                Fname VARCHAR(20),
                Age INT NOT NULL CHECK (Age >= 5 AND Age <= 25),
                ClassSec VARCHAR(10) NOT NULL,
                DoB DATE NOT NULL,
                BloodGroup VARCHAR(4) NOT NULL,
                Height FLOAT CHECK (Height > 0),
                Weight FLOAT CHECK (Weight > 0),
                Allergies VARCHAR(255),
                Tetanus ENUM('Y', 'N') DEFAULT 'N',
                TetanusDate DATE,
                Cholera ENUM('Y', 'N') DEFAULT 'N',
                CholeraDate DATE,
                Typhoid ENUM('Y', 'N') DEFAULT 'N',
                TyphoidDate DATE,
                HepA ENUM('Y', 'N') DEFAULT 'N',
                HepADate DATE,
                HepB ENUM('Y', 'N') DEFAULT 'N',
                HepBDate DATE,
                ChickenPox ENUM('Y', 'N') DEFAULT 'N',
                ChickenPoxDate DATE,
                Measles ENUM('Y', 'N') DEFAULT 'N',
                MeaslesDate DATE,
                COVID ENUM('Y', 'N') DEFAULT 'N',
                COVIDDate DATE,
                AnyOther VARCHAR(255),
                CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (AdminNo) REFERENCES users(AdminNo) ON DELETE CASCADE
            )
        """)
        
        # Audit log table
        cr.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                LogID INT AUTO_INCREMENT PRIMARY KEY,
                AdminID INT NOT NULL,
                TargetAdminNo INT,
                ActionType ENUM('CREATE', 'UPDATE', 'DELETE', 'LOGIN', 'PASSWORD_CHANGE') NOT NULL,
                ChangedFields JSON,
                OldValues JSON,
                NewValues JSON,
                IPAddress VARCHAR(45),
                CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (AdminID) REFERENCES admins(AdminID)
            )
        """)
        
        conn.commit()
        logger.info("Database tables created successfully")
        cr.close()
        conn.close()
    except sql.Error as e:
        logger.error(f"Error creating tables: {e}")
        raise

def log_audit(admin_id, action_type, target_admin_no=None, changed_fields=None, old_values=None, new_values=None, ip_address=None):
    """Log an action to audit_log table"""
    try:
        conn = create_connection()
        cr = conn.cursor()
        
        import json
        cr.execute("""
            INSERT INTO audit_log 
            (AdminID, TargetAdminNo, ActionType, ChangedFields, OldValues, NewValues, IPAddress)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            admin_id,
            target_admin_no,
            action_type,
            json.dumps(changed_fields) if changed_fields else None,
            json.dumps(old_values) if old_values else None,
            json.dumps(new_values) if new_values else None,
            ip_address
        ))
        
        conn.commit()
        cr.close()
        conn.close()
        logger.info(f"Audit logged: {action_type} by admin {admin_id}")
    except sql.Error as e:
        logger.error(f"Error logging audit: {e}")

def get_audit_logs(limit=50):
    """Retrieve audit logs"""
    try:
        conn = create_connection()
        cr = conn.cursor()
        
        cr.execute("""
            SELECT LogID, AdminID, TargetAdminNo, ActionType, CreatedAt 
            FROM audit_log 
            ORDER BY CreatedAt DESC 
            LIMIT %s
        """, (limit,))
        
        logs = cr.fetchall()
        cr.close()
        conn.close()
        return logs
    except sql.Error as e:
        logger.error(f"Error retrieving audit logs: {e}")
        return []
