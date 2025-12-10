"""
UI/CLI handling for the application
"""
import os
import sys
import logging
from datetime import datetime
from models import StudentRecords, AdminAuth
from reports import ReportsAnalytics
from utils import (
    validate_date, validate_blood_group, validate_sex, validate_age,
    calculate_bmi, sanitize_string
)

logger = logging.getLogger(__name__)

class CLI:
    """Command-line interface"""
    
    def __init__(self):
        self.current_admin_id = None
        self.current_username = None
    
    def user_input(self, prompt, data_type=str, allow_empty=False):
        """Get user input with type checking"""
        while True:
            try:
                user_val = input(prompt)
                if not user_val and not allow_empty:
                    print("Input cannot be empty.")
                    continue
                if allow_empty and not user_val:
                    return None
                return data_type(user_val)
            except ValueError:
                print(f"Invalid input. Please enter a valid {data_type.__name__}.")
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self, title):
        """Display a formatted header"""
        print("\n" + "="*60)
        print(f"{title:^60}")
        print("="*60)
    
    def sign_up(self):
        """Student signup"""
        self.display_header("Student Registration")
        
        print('\n--- Personal Details ---\n')
        admin_no = self.user_input("Enter Admin No.: ", int)
        student_name = self.user_input("Enter Student Name: ")
        
        # Create user first
        success, message = StudentRecords.create_user(admin_no, student_name)
        if not success:
            print(f"Error: {message}")
            return
        
        print('\n--- Sex, Guardians ---\n')
        sex = self.user_input("Enter Sex (M/F/Other): ")
        if not validate_sex(sex):
            print("Invalid sex. Please enter M, F, or Other.")
            return
        
        mother_name = self.user_input("Enter Mother's Name: ", allow_empty=True)
        father_name = self.user_input("Enter Father's Name: ", allow_empty=True)
        
        print('\n--- Age & Academic Info ---\n')
        age = self.user_input("Enter Age: ", int)
        if not validate_age(age):
            print(f"Invalid age. Must be between 5 and 25.")
            return
        
        class_sec = self.user_input("Enter Class & Section: ")
        
        print('\n--- Medical Info ---\n')
        dob = self.user_input("Enter Date of Birth [YYYY-MM-DD]: ")
        if not validate_date(dob):
            print("Invalid date format. Use YYYY-MM-DD.")
            return
        
        blood_group = self.user_input("Enter Blood Group (O+, O-, A+, A-, B+, B-, AB+, AB-): ")
        if not validate_blood_group(blood_group):
            print("Invalid blood group.")
            return
        
        print('\n--- Physical Measurements ---\n')
        height = self.user_input("Enter Height (cm): ", float)
        weight = self.user_input("Enter Weight (kg): ", float)
        allergies = self.user_input("Enter Allergies (or press Enter for none): ", allow_empty=True)
        
        print('\n--- Vaccinations ---\n')
        vaccinations = {}
        vaccines = ['Tetanus', 'Cholera', 'Typhoid', 'Hepatitis A', 'Hepatitis B', 'Chickenpox', 'Measles', 'COVID']
        vacc_fields = ['tetanus', 'cholera', 'typhoid', 'hep_a', 'hep_b', 'chicken_pox', 'measles', 'covid']
        
        for i, vaccine in enumerate(vaccines):
            status = self.user_input(f"{vaccine} vaccinated? (Y/N): ").upper()
            vaccinations[vacc_fields[i]] = status
            if status == 'Y':
                date_input = self.user_input(f"{vaccine} Date [YYYY-MM-DD]: ", allow_empty=True)
                if date_input and validate_date(date_input):
                    vaccinations[f"{vacc_fields[i]}_date"] = date_input
        
        other_info = self.user_input("Any other medical information: ", allow_empty=True)
        
        # Compile student data
        student_data = {
            'name': sanitize_string(student_name, 25),
            'sex': sex,
            'mother_name': sanitize_string(mother_name, 20) if mother_name else None,
            'father_name': sanitize_string(father_name, 20) if father_name else None,
            'age': age,
            'class_sec': sanitize_string(class_sec, 10),
            'dob': dob,
            'blood_group': blood_group,
            'height': height,
            'weight': weight,
            'allergies': sanitize_string(allergies, 255) if allergies else None,
            'other_info': sanitize_string(other_info, 255) if other_info else None,
            **vaccinations
        }
        
        success, message = StudentRecords.create_record(admin_no, student_data)
        print(f"\n{message}")
        if success:
            logger.info(f"Student registered: AdminNo {admin_no}, Name {student_name}")
    
    def admin_login(self):
        """Admin login"""
        self.display_header("Administrator Login")
        
        username = self.user_input("Username: ")
        password = self.user_input("Password: ")
        
        admin_id, message = AdminAuth.authenticate(username, password)
        if admin_id:
            self.current_admin_id = admin_id
            self.current_username = username
            print(f"\n✓ {message}")
            logger.info(f"Admin logged in: {username}")
            self.admin_dashboard()
        else:
            print(f"\n✗ {message}")
    
    def student_login(self):
        """Student login"""
        self.display_header("Student Login")
        
        admin_no = self.user_input("Enter Admin No.: ", int)
        student_name = self.user_input("Enter Student Name: ")
        
        record = StudentRecords.search_records("admin_no", admin_no)
        if record and len(record) > 0:
            found = False
            for r in record:
                if r[1] == student_name:  # r[1] is Sname
                    found = True
                    break
            
            if found:
                print("✓ Login successful.\n")
                self.student_menu(admin_no, student_name, r)
            else:
                print("✗ Invalid credentials.")
        else:
            print("✗ Invalid credentials.")
    
    def student_menu(self, admin_no, student_name, record):
        """Student menu"""
        while True:
            print("\n--- Student Menu ---")
            print("1. View your medical record")
            print("2. Change password")
            print("3. Exit")
            
            choice = self.user_input("Enter choice: ", int)
            
            if choice == 1:
                self.display_full_record(record)
            elif choice == 2:
                print("Note: Contact administrator to change password.")
            elif choice == 3:
                print("Logging out...")
                break
            else:
                print("Invalid choice.")
    
    def display_full_record(self, record):
        """Display complete student record"""
        print("\n--- Student Medical Record ---")
        print(f"Admin No.: {record[0]}")
        print(f"Name: {record[1]}")
        print(f"Sex: {record[2]}")
        print(f"Mother: {record[3]}")
        print(f"Father: {record[4]}")
        print(f"Age: {record[5]}")
        print(f"Class/Section: {record[6]}")
        print(f"DOB: {record[7]}")
        print(f"Blood Group: {record[8]}")
        print(f"Height (cm): {record[9]}")
        print(f"Weight (kg): {record[10]}")
        
        if record[9] and record[10]:
            bmi, status = calculate_bmi(record[9], record[10])
            print(f"BMI: {bmi} ({status})")
        
        print(f"Allergies: {record[11]}")
        print(f"\n--- Vaccinations ---")
        print(f"Tetanus: {record[12]} ({record[13]})")
        print(f"Cholera: {record[14]} ({record[15]})")
        print(f"Typhoid: {record[16]} ({record[17]})")
        print(f"Hep A: {record[18]} ({record[19]})")
        print(f"Hep B: {record[20]} ({record[21]})")
        print(f"Chickenpox: {record[22]} ({record[23]})")
        print(f"Measles: {record[24]} ({record[25]})")
        print(f"COVID: {record[26]} ({record[27]})")
        print(f"Other: {record[28]}")
    
    def admin_dashboard(self):
        """Admin dashboard"""
        while True:
            self.display_header(f"Admin Dashboard - {self.current_username}")
            print("1. View Student Records")
            print("2. Sort Student Records")
            print("3. Update Student Record")
            print("4. Delete Student Record")
            print("5. Vaccination Alerts")
            print("6. Search by Allergy")
            print("7. Reports & Analytics")
            print("8. View Audit Logs")
            print("9. Change Password")
            print("10. Logout")
            
            choice = self.user_input("Enter choice: ", int)
            
            if choice == 1:
                self.view_records()
            elif choice == 2:
                self.sort_records()
            elif choice == 3:
                self.update_record()
            elif choice == 4:
                self.delete_record()
            elif choice == 5:
                self.vaccination_alerts()
            elif choice == 6:
                self.search_allergy()
            elif choice == 7:
                self.reports_menu()
            elif choice == 8:
                self.view_audit_logs()
            elif choice == 9:
                self.change_password()
            elif choice == 10:
                print("Logging out...")
                self.current_admin_id = None
                self.current_username = None
                break
            else:
                print("Invalid choice.")
    
    def view_records(self):
        """View student records"""
        print("\n--- View Student Records ---")
        print("1. View all records")
        print("2. Search by Admin No.")
        print("3. Search by name")
        print("4. Search by class")
        
        choice = self.user_input("Enter choice: ", int)
        
        if choice == 1:
            records = StudentRecords.get_all_records()
            self.display_records_table(records)
        elif choice == 2:
            admin_no = self.user_input("Admin No.: ", int)
            record = StudentRecords.get_record(admin_no)
            if record:
                self.display_full_record(record)
            else:
                print("Record not found.")
        elif choice == 3:
            name = self.user_input("Student name: ")
            records = StudentRecords.search_records("name", name)
            self.display_records_table(records)
        elif choice == 4:
            class_sec = self.user_input("Class/Section: ")
            records = StudentRecords.search_records("class", class_sec)
            self.display_records_table(records)
    
    def display_records_table(self, records):
        """Display records in table format"""
        if not records:
            print("No records found.")
            return
        
        print(f"\n{'AdminNo':<10} {'Name':<25} {'Sex':<8} {'Age':<5} {'Class':<10} {'Blood':<7}")
        print("-" * 70)
        for r in records:
            print(f"{r[0]:<10} {r[1]:<25} {r[2]:<8} {r[5]:<5} {r[6]:<10} {r[8]:<7}")
    
    def sort_records(self):
        """Sort records"""
        print("\n--- Sort Records ---")
        print("1. By name")
        print("2. By age")
        print("3. By class")
        print("4. By blood group")
        
        choice = self.user_input("Enter choice: ", int)
        
        try:
            from db import create_connection
            conn = create_connection()
            cr = conn.cursor()
            
            if choice == 1:
                cr.execute("SELECT * FROM records ORDER BY Sname ASC")
            elif choice == 2:
                cr.execute("SELECT * FROM records ORDER BY Age ASC")
            elif choice == 3:
                cr.execute("SELECT * FROM records ORDER BY ClassSec ASC")
            elif choice == 4:
                cr.execute("SELECT * FROM records ORDER BY BloodGroup ASC")
            else:
                return
            
            records = cr.fetchall()
            self.display_records_table(records)
            cr.close()
            conn.close()
        except Exception as e:
            print(f"Error: {e}")
    
    def update_record(self):
        """Update student record"""
        print("\n--- Update Student Record ---")
        admin_no = self.user_input("Admin No.: ", int)
        
        record = StudentRecords.get_record(admin_no)
        if not record:
            print("Record not found.")
            return
        
        self.display_full_record(record)
        
        print("\nWhat to update?")
        print("1. Height")
        print("2. Weight")
        print("3. Class/Section")
        print("4. Allergies")
        print("5. Vaccination")
        
        choice = self.user_input("Enter choice: ", int)
        
        try:
            if choice == 1:
                height = self.user_input("New height (cm): ", float)
                StudentRecords.update_record(admin_no, self.current_admin_id, height=height)
                print("✓ Updated.")
            elif choice == 2:
                weight = self.user_input("New weight (kg): ", float)
                StudentRecords.update_record(admin_no, self.current_admin_id, weight=weight)
                print("✓ Updated.")
            elif choice == 3:
                class_sec = self.user_input("New class/section: ")
                StudentRecords.update_record(admin_no, self.current_admin_id, class_sec=class_sec)
                print("✓ Updated.")
            elif choice == 4:
                allergies = self.user_input("New allergies: ")
                StudentRecords.update_record(admin_no, self.current_admin_id, allergies=allergies)
                print("✓ Updated.")
            elif choice == 5:
                print("Select vaccination:")
                vaccines = ['Tetanus', 'Cholera', 'Typhoid', 'HepA', 'HepB', 'ChickenPox', 'Measles', 'COVID']
                for i, v in enumerate(vaccines, 1):
                    print(f"{i}. {v}")
                
                vacc_choice = self.user_input("Enter choice: ", int)
                if 1 <= vacc_choice <= len(vaccines):
                    vacc = vaccines[vacc_choice - 1].lower()
                    status = self.user_input("Status (Y/N): ").upper()
                    date = self.user_input("Date [YYYY-MM-DD] (or blank): ", allow_empty=True)
                    StudentRecords.update_record(admin_no, self.current_admin_id, **{vacc: status, f"{vacc}_date": date})
                    print("✓ Updated.")
        except Exception as e:
            print(f"Error: {e}")
    
    def delete_record(self):
        """Delete student record"""
        print("\n--- Delete Student Record ---")
        admin_no = self.user_input("Admin No.: ", int)
        
        record = StudentRecords.get_record(admin_no)
        if not record:
            print("Record not found.")
            return
        
        print(f"About to delete: {record[1]}")
        confirm = self.user_input("Confirm? (Y/N): ").upper()
        
        if confirm == 'Y':
            StudentRecords.delete_record(admin_no, self.current_admin_id)
            print("✓ Deleted.")
    
    def vaccination_alerts(self):
        """Show vaccination alerts"""
        print("\n--- Vaccination Alerts ---")
        print("1. Due for booster")
        print("2. Missing critical vaccinations")
        
        choice = self.user_input("Enter choice: ", int)
        # Implementation in next section
        print("Feature coming soon.")
    
    def search_allergy(self):
        """Search by allergy"""
        print("\n--- Search by Allergy ---")
        allergy = self.user_input("Allergy to search: ")
        
        try:
            from db import create_connection
            conn = create_connection()
            cr = conn.cursor()
            cr.execute("SELECT AdminNo, Sname, Age, ClassSec, Allergies FROM records WHERE Allergies LIKE %s", (f"%{allergy}%",))
            records = cr.fetchall()
            cr.close()
            conn.close()
            
            if records:
                print(f"\n--- Students with {allergy} ---")
                for r in records:
                    print(f"AdminNo: {r[0]}, Name: {r[1]}, Age: {r[2]}, Class: {r[3]}, Allergies: {r[4]}")
            else:
                print("No students found.")
        except Exception as e:
            print(f"Error: {e}")
    
    def reports_menu(self):
        """Reports menu"""
        print("\n--- Reports & Analytics ---")
        print("1. Blood group distribution")
        print("2. BMI distribution")
        print("3. Vaccination coverage")
        print("4. Class distribution")
        print("5. Age statistics")
        print("6. Missing records")
        print("7. Export report")
        
        choice = self.user_input("Enter choice: ", int)
        
        if choice == 1:
            data = ReportsAnalytics.blood_group_distribution()
            print("\n--- Blood Group Distribution ---")
            print(f"{'Blood Group':<15} {'Count':<10}")
            print("-" * 25)
            for row in data:
                print(f"{row[0]:<15} {row[1]:<10}")
        
        elif choice == 2:
            data = ReportsAnalytics.bmi_distribution()
            print("\n--- BMI Distribution ---")
            for status, count in data.items():
                print(f"{status}: {count} students")
        
        elif choice == 3:
            data = ReportsAnalytics.vaccination_coverage()
            print("\n--- Vaccination Coverage ---")
            for vacc, coverage in data.items():
                print(f"{vacc}: {coverage}%")
        
        elif choice == 4:
            data = ReportsAnalytics.class_distribution()
            print("\n--- Class Distribution ---")
            print(f"{'Class':<15} {'Count':<10}")
            print("-" * 25)
            for row in data:
                print(f"{row[0]:<15} {row[1]:<10}")
        
        elif choice == 5:
            data = ReportsAnalytics.age_statistics()
            print("\n--- Age Statistics ---")
            print(f"Min Age: {data.get('min')}")
            print(f"Max Age: {data.get('max')}")
            print(f"Avg Age: {data.get('avg')}")
            print(f"Total Students: {data.get('total')}")
        
        elif choice == 6:
            data = ReportsAnalytics.missing_records()
            print("\n--- Missing Records ---")
            if data:
                for row in data:
                    print(f"AdminNo {row[0]}: {row[1]}")
            else:
                print("All records are complete.")
        
        elif choice == 7:
            report_type = input("Report type (comprehensive/health): ")
            filename = ReportsAnalytics.export_report_csv(report_type)
            if filename:
                print(f"✓ Exported: {filename}")
    
    def view_audit_logs(self):
        """View audit logs"""
        from db import get_audit_logs
        logs = get_audit_logs(20)
        
        if not logs:
            print("No audit logs found.")
            return
        
        print("\n--- Recent Audit Logs ---")
        print(f"{'LogID':<8} {'AdminID':<10} {'Action':<15} {'Target':<10} {'Time':<20}")
        print("-" * 65)
        for log in logs:
            print(f"{log[0]:<8} {log[1]:<10} {log[2]:<15} {log[3] or '-':<10} {str(log[4]):<20}")
    
    def change_password(self):
        """Change admin password"""
        old_pass = self.user_input("Current password: ")
        new_pass = self.user_input("New password: ")
        confirm = self.user_input("Confirm password: ")
        
        if new_pass != confirm:
            print("Passwords don't match.")
            return
        
        success, message = AdminAuth.change_password(self.current_admin_id, old_pass, new_pass)
        print(message)
    
    def main_menu(self):
        """Main menu"""
        while True:
            self.display_header("Medical Record Management System")
            print("1. Student Registration")
            print("2. Student Login")
            print("3. Admin Login")
            print("4. Exit")
            
            choice = self.user_input("Enter choice: ", int)
            
            if choice == 1:
                self.sign_up()
            elif choice == 2:
                self.student_login()
            elif choice == 3:
                self.admin_login()
            elif choice == 4:
                print("Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice.")
