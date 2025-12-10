"""
Reports and analytics module
"""
import csv
from datetime import datetime
import logging
from db import create_connection
from utils import calculate_bmi

logger = logging.getLogger(__name__)

class ReportsAnalytics:
    """Generate reports and statistics"""
    
    @staticmethod
    def blood_group_distribution():
        """Get count of students per blood group"""
        try:
            conn = create_connection()
            cr = conn.cursor()
            
            cr.execute("""
                SELECT BloodGroup, COUNT(*) as Count 
                FROM records 
                GROUP BY BloodGroup 
                ORDER BY Count DESC
            """)
            
            results = cr.fetchall()
            cr.close()
            conn.close()
            return results
        except Exception as e:
            logger.error(f"Error getting blood group distribution: {e}")
            return []
    
    @staticmethod
    def bmi_distribution():
        """Get BMI distribution across students"""
        try:
            conn = create_connection()
            cr = conn.cursor()
            
            cr.execute("""
                SELECT AdminNo, Sname, Height, Weight 
                FROM records 
                WHERE Height IS NOT NULL AND Weight IS NOT NULL
            """)
            
            records = cr.fetchall()
            cr.close()
            conn.close()
            
            distribution = {
                'Underweight': 0,
                'Normal': 0,
                'Overweight': 0,
                'Obese': 0
            }
            
            for record in records:
                bmi, status = calculate_bmi(record[2], record[3])
                if status in distribution:
                    distribution[status] += 1
            
            return distribution
        except Exception as e:
            logger.error(f"Error getting BMI distribution: {e}")
            return {}
    
    @staticmethod
    def vaccination_coverage():
        """Get vaccination coverage percentages"""
        try:
            conn = create_connection()
            cr = conn.cursor()
            
            cr.execute("SELECT COUNT(*) FROM records")
            total = cr.fetchone()[0]
            
            if total == 0:
                return {}
            
            vaccinations = ['Tetanus', 'Cholera', 'Typhoid', 'HepA', 'HepB', 'ChickenPox', 'Measles', 'COVID']
            coverage = {}
            
            for vacc in vaccinations:
                cr.execute(f"SELECT COUNT(*) FROM records WHERE {vacc} = 'Y'")
                count = cr.fetchone()[0]
                coverage[vacc] = round((count / total) * 100, 2)
            
            cr.close()
            conn.close()
            return coverage
        except Exception as e:
            logger.error(f"Error getting vaccination coverage: {e}")
            return {}
    
    @staticmethod
    def class_distribution():
        """Get student count per class/section"""
        try:
            conn = create_connection()
            cr = conn.cursor()
            
            cr.execute("""
                SELECT ClassSec, COUNT(*) as Count 
                FROM records 
                GROUP BY ClassSec 
                ORDER BY ClassSec
            """)
            
            results = cr.fetchall()
            cr.close()
            conn.close()
            return results
        except Exception as e:
            logger.error(f"Error getting class distribution: {e}")
            return []
    
    @staticmethod
    def age_statistics():
        """Get age statistics"""
        try:
            conn = create_connection()
            cr = conn.cursor()
            
            cr.execute("""
                SELECT 
                    MIN(Age) as MinAge,
                    MAX(Age) as MaxAge,
                    AVG(Age) as AvgAge,
                    COUNT(*) as TotalStudents
                FROM records
            """)
            
            result = cr.fetchone()
            cr.close()
            conn.close()
            
            return {
                'min': result[0],
                'max': result[1],
                'avg': round(result[2], 2) if result[2] else 0,
                'total': result[3]
            }
        except Exception as e:
            logger.error(f"Error getting age statistics: {e}")
            return {}
    
    @staticmethod
    def missing_records():
        """Find students with incomplete records"""
        try:
            conn = create_connection()
            cr = conn.cursor()
            
            cr.execute("""
                SELECT AdminNo, Sname, 
                       CASE WHEN Height IS NULL THEN 1 ELSE 0 END as MissingHeight,
                       CASE WHEN Weight IS NULL THEN 1 ELSE 0 END as MissingWeight,
                       CASE WHEN Allergies IS NULL OR Allergies = '' THEN 1 ELSE 0 END as MissingAllergies
                FROM records
                WHERE Height IS NULL OR Weight IS NULL OR Allergies IS NULL OR Allergies = ''
            """)
            
            results = cr.fetchall()
            cr.close()
            conn.close()
            return results
        except Exception as e:
            logger.error(f"Error getting missing records: {e}")
            return []
    
    @staticmethod
    def export_report_csv(report_type='comprehensive'):
        """Export report to CSV"""
        try:
            filename = f"report_{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            conn = create_connection()
            cr = conn.cursor()
            
            if report_type == 'comprehensive':
                cr.execute("SELECT * FROM records")
                records = cr.fetchall()
                fieldnames = [
                    'AdminNo', 'StudentName', 'Sex', 'MotherName', 'FatherName', 'Age',
                    'ClassSection', 'DateOfBirth', 'BloodGroup', 'Height', 'Weight', 'Allergies',
                    'Tetanus', 'TetanusDate', 'Cholera', 'CholeraDate', 'Typhoid', 'TyphoidDate',
                    'HepA', 'HepADate', 'HepB', 'HepBDate', 'ChickenPox', 'ChickenPoxDate',
                    'Measles', 'MeaslesDate', 'COVID', 'COVIDDate', 'OtherInfo'
                ]
            elif report_type == 'health':
                cr.execute("SELECT AdminNo, Sname, Age, ClassSec, Height, Weight, BloodGroup, Allergies FROM records")
                records = cr.fetchall()
                fieldnames = ['AdminNo', 'StudentName', 'Age', 'ClassSection', 'Height', 'Weight', 'BloodGroup', 'Allergies']
            else:
                cr.close()
                conn.close()
                return None
            
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(fieldnames)
                writer.writerows(records)
            
            cr.close()
            conn.close()
            logger.info(f"Report exported: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error exporting report: {e}")
            return None
