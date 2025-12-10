import pymysql as sql
import csv
from datetime import datetime, timedelta

# Admin Credentials
ADMIN_NAME = "GOD01"
ADMIN_PASSWORD = "JAKSA$01#RX-7"
ADMIN_OTP = "0001"

def user_input(entry, data_type=str):
    while True:
        try:
            user_input = data_type(input(entry))
            return user_input
        except ValueError:
            print("Invalid input. Please try again.")

def create_connection():
    return sql.connect(host='localhost', user='root', passwd='XXXX', database='XXXX')

def create_table():
    try:
        conn = create_connection()
        cr = conn.cursor()
        cr.execute(
            "create table if not exists users ("
            "AdminNo int primary key, "
            "Sname varchar(25) not null"
            ");"
        )
        cr.execute(
            "create table if not exists records ("
            "AdminNo int primary key, "
            "Sname varchar(25) not null, "
            "Sex char(10) not null, "
            "Mname varchar(20), "
            "Fname varchar(20), "
            "Age int not null, "
            "ClassSec varchar(10) not null, "
            "DoB date not null, "
            "BloodGroup varchar(4) not null, "
            "Height float, "
            "Weight float, "
            "Allergies varchar(100), "
            "Tetanus varchar(10), "
            "TetanusDate date, "
            "Cholera varchar(10), "
            "CholeraDate date, "
            "Typhoid varchar(10), "
            "TyphoidDate date, "
            "HepA varchar(10), "
            "HepADate date, "
            "HepB varchar(10), "
            "HepBDate date, "
            "ChickenPox varchar(10), "
            "ChickenPoxDate date, "
            "Measles varchar(10), "
            "MeaslesDate date, "
            "COVID varchar(10), "
            "COVIDDate date, "
            "AnyOther varchar(100)"
            ");"
        )
        conn.commit()
        cr.close()
        conn.close()
    except sql.Error as e:
        print(f"Database error: {e}")
        return

def sign_up():
    print('\n- - -PERSONAL DETAILS- - -\n')
    admin_no = user_input("Enter Admin No.: ", int)
    s_name = user_input("Enter Student Name: ")
    sex = user_input("Enter Sex (M/F): ")
    mother_name = user_input("Enter Mother's Name: ")
    father_name = user_input("Enter Father's Name: ")
    age = user_input("Enter Age: ", int)
    class_sec = user_input("Enter Class & Sec: ")
    dob = user_input("Enter Date of Birth [YYYY-MM-DD]: ", str)
    bgrp = user_input("Enter Blood Group: ")
    print('\n- - -PHYSICAL RECORDS- - -\n')
    height = user_input("Enter Height (cm): ", float)
    weight = user_input("Enter Weight (kg): ", float)
    allergies = user_input("Enter Allergies: ")
    print('\n- - -VACCINATIONS- - -\n')
    tetanus = user_input("Tetanus Vaccinated? (Y/N): ").upper()
    tetanus_date = user_input("Tetanus Date [YYYY-MM-DD] (or press Enter to skip): ") if tetanus == "Y" else None
    cholera = user_input("Cholera Vaccinated? (Y/N): ").upper()
    cholera_date = user_input("Cholera Date [YYYY-MM-DD] (or press Enter to skip): ") if cholera == "Y" else None
    typhoid = user_input("Typhoid Vaccinated? (Y/N): ").upper()
    typhoid_date = user_input("Typhoid Date [YYYY-MM-DD] (or press Enter to skip): ") if typhoid == "Y" else None
    hep_a = user_input("Hepatitis A Vaccinated? (Y/N): ").upper()
    hep_a_date = user_input("Hepatitis A Date [YYYY-MM-DD] (or press Enter to skip): ") if hep_a == "Y" else None
    hep_b = user_input("Hepatitis B Vaccinated? (Y/N): ").upper()
    hep_b_date = user_input("Hepatitis B Date [YYYY-MM-DD] (or press Enter to skip): ") if hep_b == "Y" else None
    chicken_pox = user_input("Chickenpox Vaccinated? (Y/N): ").upper()
    chicken_pox_date = user_input("Chickenpox Date [YYYY-MM-DD] (or press Enter to skip): ") if chicken_pox == "Y" else None
    measles = user_input("Measles Vaccinated? (Y/N): ").upper()
    measles_date = user_input("Measles Date [YYYY-MM-DD] (or press Enter to skip): ") if measles == "Y" else None
    covid = user_input("COVID Vaccinated? (Y/N): ").upper()
    covid_date = user_input("COVID Date [YYYY-MM-DD] (or press Enter to skip): ") if covid == "Y" else None
    any_other = user_input("Any Other Information: ")
    
    try:
        conn = create_connection()
        cr = conn.cursor()
        
        # Insert user with parameterized query
        cr.execute(
            "INSERT INTO users (AdminNo, Sname) VALUES (%s, %s)",
            (admin_no, s_name)
        )
        
        # Insert record with parameterized query
        cr.execute("""
            INSERT INTO records VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            admin_no, s_name, sex, mother_name, father_name, age, class_sec, dob, bgrp,
            height, weight, allergies, tetanus, tetanus_date, cholera, cholera_date,
            typhoid, typhoid_date, hep_a, hep_a_date, hep_b, hep_b_date, chicken_pox,
            chicken_pox_date, measles, measles_date, covid, covid_date, any_other
        ))
        
        conn.commit()
        cr.close()
        conn.close()
        print('\n\nRecords successfully added!')
    except sql.Error as e:
        print(f"Database error: {e}")
        return
def adminsign_in():
    print("\nSigning in as Administrator\n")
    admin_name = user_input("Administrator name: ")
    admin_pass = user_input("Administrator password: ")
    if admin_name == ADMIN_NAME and admin_pass == ADMIN_PASSWORD:
        print("A one-time password (OTP) has been sent to your registered device.")
        admin_otp = user_input("Enter OTP: ")
        if admin_otp == ADMIN_OTP:
            print("Administrator sign-in successful.")
            admin_dash()
        else:
            print("Administrator sign-in failed.\nInvalid OTP.")
    else:
        print("Administrator sign-in failed.\nInvalid credentials.")

def calculate_bmi(height_cm, weight_kg):
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

def view_user_records():
    try:
        conn = create_connection()
        cr = conn.cursor()
        
        print("\n--- View User Records ---")
        print("1. View All Records")
        print("2. Search by Admin No.")
        print("3. Search by Student Name")
        print("4. Search by Class/Section")
        choice = user_input("Enter your choice: ", int)
        
        if choice == 1:
            cr.execute("SELECT AdminNo, Sname, Sex, Age, ClassSec, BloodGroup FROM records")
            records = cr.fetchall()
            if records:
                print("\n--- Summary of All Records ---")
                print(f"{'AdminNo':<10} {'Name':<25} {'Sex':<5} {'Age':<5} {'Class':<10} {'Blood':<6}")
                print("-" * 65)
                for record in records:
                    print(f"{record[0]:<10} {record[1]:<25} {record[2]:<5} {record[3]:<5} {record[4]:<10} {record[5]:<6}")
                
                admin_no = user_input("\nEnter Admin No. to view full details (or 0 to go back): ", int)
                if admin_no != 0:
                    cr.execute("SELECT * FROM records WHERE AdminNo = %s", (admin_no,))
                    full_record = cr.fetchone()
                    if full_record:
                        display_full_record(full_record)
                    else:
                        print("Record not found.")
            else:
                print("No records found.")
        
        elif choice == 2:
            admin_no = user_input("Enter Admin No.: ", int)
            cr.execute("SELECT * FROM records WHERE AdminNo = %s", (admin_no,))
            record = cr.fetchone()
            if record:
                display_full_record(record)
            else:
                print("Record not found.")
        
        elif choice == 3:
            s_name = user_input("Enter Student Name: ")
            cr.execute("SELECT AdminNo, Sname, Sex, Age, ClassSec, BloodGroup FROM records WHERE Sname LIKE %s", (f"%{s_name}%",))
            records = cr.fetchall()
            if records:
                print("\n--- Matching Records ---")
                print(f"{'AdminNo':<10} {'Name':<25} {'Sex':<5} {'Age':<5} {'Class':<10} {'Blood':<6}")
                print("-" * 65)
                for record in records:
                    print(f"{record[0]:<10} {record[1]:<25} {record[2]:<5} {record[3]:<5} {record[4]:<10} {record[5]:<6}")
                
                admin_no = user_input("\nEnter Admin No. for full details (or 0 to go back): ", int)
                if admin_no != 0:
                    cr.execute("SELECT * FROM records WHERE AdminNo = %s", (admin_no,))
                    full_record = cr.fetchone()
                    if full_record:
                        display_full_record(full_record)
            else:
                print("No matching records found.")
        
        elif choice == 4:
            class_sec = user_input("Enter Class/Section: ")
            cr.execute("SELECT AdminNo, Sname, Sex, Age, ClassSec, BloodGroup FROM records WHERE ClassSec = %s", (class_sec,))
            records = cr.fetchall()
            if records:
                print("\n--- Records for Class/Section ---")
                print(f"{'AdminNo':<10} {'Name':<25} {'Sex':<5} {'Age':<5} {'Class':<10} {'Blood':<6}")
                print("-" * 65)
                for record in records:
                    print(f"{record[0]:<10} {record[1]:<25} {record[2]:<5} {record[3]:<5} {record[4]:<10} {record[5]:<6}")
            else:
                print("No records found for this class/section.")
        
        cr.close()
        conn.close()
    except sql.Error as e:
        print(f"Database error: {e}")

def display_full_record(record):
    """Display complete record details"""
    print("\n--- Full Student Record ---")
    print(f"Admin No.: {record[0]}")
    print(f"Student Name: {record[1]}")
    print(f"Sex: {record[2]}")
    print(f"Mother's Name: {record[3]}")
    print(f"Father's Name: {record[4]}")
    print(f"Age: {record[5]}")
    print(f"Class & Sec: {record[6]}")
    print(f"Date of Birth: {record[7]}")
    print(f"Blood Group: {record[8]}")
    print(f"Height (cm): {record[9]}")
    print(f"Weight (kg): {record[10]}")
    
    # Calculate and display BMI
    if record[9] and record[10]:
        bmi, status = calculate_bmi(record[9], record[10])
        print(f"BMI: {bmi} ({status})")
    
    print(f"Allergies: {record[11]}")
    print("\n--- Vaccination Records ---")
    print(f"Tetanus: {record[12]} (Date: {record[13]})")
    print(f"Cholera: {record[14]} (Date: {record[15]})")
    print(f"Typhoid: {record[16]} (Date: {record[17]})")
    print(f"Hepatitis A: {record[18]} (Date: {record[19]})")
    print(f"Hepatitis B: {record[20]} (Date: {record[21]})")
    print(f"Chickenpox: {record[22]} (Date: {record[23]})")
    print(f"Measles: {record[24]} (Date: {record[25]})")
    print(f"COVID: {record[26]} (Date: {record[27]})")
    print(f"Other Information: {record[28]}")

def sort_user_records():
    """Sort records by different criteria"""
    try:
        conn = create_connection()
        cr = conn.cursor()
        
        print("\n--- Sort User Records ---")
        print("1. Sort by Name (Alphabetical)")
        print("2. Sort by Age")
        print("3. Sort by Class/Section")
        print("4. Sort by Blood Group")
        choice = user_input("Enter your choice: ", int)
        
        if choice == 1:
            cr.execute("SELECT AdminNo, Sname, Sex, Age, ClassSec, BloodGroup FROM records ORDER BY Sname ASC")
        elif choice == 2:
            cr.execute("SELECT AdminNo, Sname, Sex, Age, ClassSec, BloodGroup FROM records ORDER BY Age ASC")
        elif choice == 3:
            cr.execute("SELECT AdminNo, Sname, Sex, Age, ClassSec, BloodGroup FROM records ORDER BY ClassSec ASC")
        elif choice == 4:
            cr.execute("SELECT AdminNo, Sname, Sex, Age, ClassSec, BloodGroup FROM records ORDER BY BloodGroup ASC")
        else:
            print("Invalid choice.")
            return
        
        records = cr.fetchall()
        if records:
            print("\n--- Sorted Records ---")
            print(f"{'AdminNo':<10} {'Name':<25} {'Sex':<5} {'Age':<5} {'Class':<10} {'Blood':<6}")
            print("-" * 65)
            for record in records:
                print(f"{record[0]:<10} {record[1]:<25} {record[2]:<5} {record[3]:<5} {record[4]:<10} {record[5]:<6}")
        else:
            print("No records found.")
        
        cr.close()
        conn.close()
    except sql.Error as e:
        print(f"Database error: {e}")

def update_user_record():
    """Update a user record"""
    try:
        conn = create_connection()
        cr = conn.cursor()
        
        print("\n--- Update User Record ---")
        admin_no = user_input("Enter Admin No. to update: ", int)
        
        cr.execute("SELECT * FROM records WHERE AdminNo = %s", (admin_no,))
        record = cr.fetchone()
        
        if not record:
            print("Record not found.")
            return
        
        display_full_record(record)
        
        print("\nWhat would you like to update?")
        print("1. Height")
        print("2. Weight")
        print("3. Class/Section")
        print("4. Allergies")
        print("5. Vaccination Status")
        print("6. Other Information")
        choice = user_input("Enter your choice: ", int)
        
        if choice == 1:
            new_height = user_input("Enter new height (cm): ", float)
            cr.execute("UPDATE records SET Height = %s WHERE AdminNo = %s", (new_height, admin_no))
            print("Height updated successfully.")
        
        elif choice == 2:
            new_weight = user_input("Enter new weight (kg): ", float)
            cr.execute("UPDATE records SET Weight = %s WHERE AdminNo = %s", (new_weight, admin_no))
            print("Weight updated successfully.")
        
        elif choice == 3:
            new_class = user_input("Enter new class/section: ")
            cr.execute("UPDATE records SET ClassSec = %s WHERE AdminNo = %s", (new_class, admin_no))
            print("Class/Section updated successfully.")
        
        elif choice == 4:
            new_allergies = user_input("Enter new allergies: ")
            cr.execute("UPDATE records SET Allergies = %s WHERE AdminNo = %s", (new_allergies, admin_no))
            print("Allergies updated successfully.")
        
        elif choice == 5:
            print("\nVaccinations:")
            print("1. Tetanus")
            print("2. Cholera")
            print("3. Typhoid")
            print("4. Hepatitis A")
            print("5. Hepatitis B")
            print("6. Chickenpox")
            print("7. Measles")
            print("8. COVID")
            vacc_choice = user_input("Select vaccination: ", int)
            
            vacc_map = {
                1: ("Tetanus", "TetanusDate"),
                2: ("Cholera", "CholeraDate"),
                3: ("Typhoid", "TyphoidDate"),
                4: ("HepA", "HepADate"),
                5: ("HepB", "HepBDate"),
                6: ("ChickenPox", "ChickenPoxDate"),
                7: ("Measles", "MeaslesDate"),
                8: ("COVID", "COVIDDate")
            }
            
            if vacc_choice in vacc_map:
                vacc_col, date_col = vacc_map[vacc_choice]
                status = user_input(f"Vaccinated? (Y/N): ").upper()
                date = user_input(f"Vaccination Date [YYYY-MM-DD]: ") if status == "Y" else None
                cr.execute(f"UPDATE records SET {vacc_col} = %s, {date_col} = %s WHERE AdminNo = %s", (status, date, admin_no))
                print("Vaccination status updated successfully.")
        
        elif choice == 6:
            new_other = user_input("Enter new other information: ")
            cr.execute("UPDATE records SET AnyOther = %s WHERE AdminNo = %s", (new_other, admin_no))
            print("Other information updated successfully.")
        
        else:
            print("Invalid choice.")
        
        conn.commit()
        cr.close()
        conn.close()
    except sql.Error as e:
        print(f"Database error: {e}")

def delete_user_record():
    """Delete a user record"""
    try:
        conn = create_connection()
        cr = conn.cursor()
        
        print("\n--- Delete User Record ---")
        admin_no = user_input("Enter Admin No. to delete: ", int)
        
        cr.execute("SELECT Sname FROM records WHERE AdminNo = %s", (admin_no,))
        record = cr.fetchone()
        
        if not record:
            print("Record not found.")
            return
        
        print(f"\nYou are about to delete the record for: {record[0]}")
        confirm = user_input("Are you sure? (Y/N): ").upper()
        
        if confirm == "Y":
            cr.execute("DELETE FROM records WHERE AdminNo = %s", (admin_no,))
            cr.execute("DELETE FROM users WHERE AdminNo = %s", (admin_no,))
            conn.commit()
            print("Record deleted successfully.")
        else:
            print("Deletion cancelled.")
        
        cr.close()
        conn.close()
    except sql.Error as e:
        print(f"Database error: {e}")

def vaccination_alerts():
    """Generate vaccination alerts for due boosters"""
    try:
        conn = create_connection()
        cr = conn.cursor()
        
        print("\n--- Vaccination Alerts ---")
        print("1. Students due for Tetanus booster (5+ years)")
        print("2. Students missing Hepatitis B vaccination")
        print("3. Students missing critical vaccinations")
        choice = user_input("Enter your choice: ", int)
        
        if choice == 1:
            # Tetanus boosters every 5 years
            five_years_ago = datetime.now() - timedelta(days=5*365)
            cr.execute("""
                SELECT AdminNo, Sname, TetanusDate FROM records 
                WHERE TetanusDate IS NOT NULL AND TetanusDate < %s
            """, (five_years_ago.strftime('%Y-%m-%d'),))
            records = cr.fetchall()
            if records:
                print("\n--- Students Due for Tetanus Booster ---")
                for r in records:
                    print(f"AdminNo: {r[0]}, Name: {r[1]}, Last Date: {r[2]}")
            else:
                print("No students are currently due for Tetanus booster.")
        
        elif choice == 2:
            cr.execute("SELECT AdminNo, Sname FROM records WHERE HepB IS NULL OR HepB = 'N'")
            records = cr.fetchall()
            if records:
                print("\n--- Students Missing Hepatitis B Vaccination ---")
                for r in records:
                    print(f"AdminNo: {r[0]}, Name: {r[1]}")
            else:
                print("All students have Hepatitis B vaccination on record.")
        
        elif choice == 3:
            cr.execute("""
                SELECT AdminNo, Sname FROM records 
                WHERE HepB IS NULL OR HepB = 'N' 
                   OR COVID IS NULL OR COVID = 'N'
                   OR Measles IS NULL OR Measles = 'N'
            """)
            records = cr.fetchall()
            if records:
                print("\n--- Students Missing Critical Vaccinations ---")
                for r in records:
                    print(f"AdminNo: {r[0]}, Name: {r[1]}")
            else:
                print("All students are up-to-date on critical vaccinations.")
        
        cr.close()
        conn.close()
    except sql.Error as e:
        print(f"Database error: {e}")

def search_allergy():
    """Search for students with specific allergies"""
    try:
        conn = create_connection()
        cr = conn.cursor()
        
        print("\n--- Search Students by Allergy ---")
        allergy = user_input("Enter allergy to search for: ")
        
        cr.execute("""
            SELECT AdminNo, Sname, Age, ClassSec, Allergies FROM records 
            WHERE Allergies LIKE %s
        """, (f"%{allergy}%",))
        records = cr.fetchall()
        
        if records:
            print(f"\n--- Students with '{allergy}' Allergy ---")
            print(f"{'AdminNo':<10} {'Name':<25} {'Age':<5} {'Class':<10} {'Allergies':<30}")
            print("-" * 85)
            for record in records:
                print(f"{record[0]:<10} {record[1]:<25} {record[2]:<5} {record[3]:<10} {record[4]:<30}")
        else:
            print(f"No students found with '{allergy}' allergy.")
        
        cr.close()
        conn.close()
    except sql.Error as e:
        print(f"Database error: {e}")

def export_to_csv():
    """Export all records to CSV file"""
    try:
        conn = create_connection()
        cr = conn.cursor()
        
        cr.execute("SELECT * FROM records")
        records = cr.fetchall()
        
        if not records:
            print("No records to export.")
            return
        
        filename = f"medical_records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = [
                'AdminNo', 'StudentName', 'Sex', 'MotherName', 'FatherName', 'Age', 
                'ClassSection', 'DateOfBirth', 'BloodGroup', 'Height', 'Weight', 'Allergies',
                'Tetanus', 'TetanusDate', 'Cholera', 'CholeraDate', 'Typhoid', 'TyphoidDate',
                'HepA', 'HepADate', 'HepB', 'HepBDate', 'ChickenPox', 'ChickenPoxDate',
                'Measles', 'MeaslesDate', 'COVID', 'COVIDDate', 'OtherInfo'
            ]
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            writer.writerows(records)
        
        print(f"Records exported successfully to {filename}")
        cr.close()
        conn.close()
    except sql.Error as e:
        print(f"Database error: {e}")
    except IOError as e:
        print(f"File error: {e}")

def admin_dash():
    """Admin Dashboard"""
    while True:
        print("\n--- Admin Dashboard ---")
        print("1. View User Records")
        print("2. Sort User Records")
        print("3. Update User Record")
        print("4. Delete User Record")
        print("5. Vaccination Alerts")
        print("6. Search by Allergy")
        print("7. Export Records to CSV")
        print("8. Exit")
        choice = user_input("Enter your choice: ", int)
        
        if choice == 1:
            view_user_records()
        elif choice == 2:
            sort_user_records()
        elif choice == 3:
            update_user_record()
        elif choice == 4:
            delete_user_record()
        elif choice == 5:
            vaccination_alerts()
        elif choice == 6:
            search_allergy()
        elif choice == 7:
            export_to_csv()
        elif choice == 8:
            print("Exiting admin dashboard...")
            break
        else:
            print("Invalid choice. Please try again.")


def losersign_in():
    print("\nSigning in as Student")
    admit_no = user_input("\nEnter Admin No.: ", int)
    s_name = user_input("Enter Student Name: ")
    
    try:
        conn = create_connection()
        cr = conn.cursor()
        cr.execute("SELECT * FROM users WHERE AdminNo = %s AND Sname = %s", (admit_no, s_name))
        result = cr.fetchone()
        
        if result:
            print("Sign-in successful.\n")
            
            while True:
                print("\nWhat would you like to do?")
                print("1. View your records")
                print("2. Exit")
                choice = user_input("Enter your choice: ", int)
                
                if choice == 1:
                    cr.execute("SELECT * FROM records WHERE AdminNo = %s AND Sname = %s", (admit_no, s_name))
                    records = cr.fetchone()
                    if records:
                        print("\nStudent Records:")
                        print("Admin No.: {}".format(records[0]))
                        print("Student Name: {}".format(records[1]))
                        print("Sex: {}".format(records[2]))
                        print("Mother's Name: {}".format(records[3]))
                        print("Father's Name: {}".format(records[4]))
                        print("Age: {}".format(records[5]))
                        print("Class & Sec: {}".format(records[6]))
                        print("Date of Birth: {}".format(records[7]))
                        print("Blood Group: {}".format(records[8]))
                        print("Height: {}".format(records[9]))
                        print("Weight: {}".format(records[10]))
                        print("Allergies: {}".format(records[11]))
                        
                        # Calculate and display BMI
                        if records[9] and records[10]:
                            bmi, status = calculate_bmi(records[9], records[10])
                            print(f"BMI: {bmi} ({status})")
                    else:
                        print("No records found for this student.")
                elif choice == 2:
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Invalid credentials. Sign-in failed.")
        
        cr.close()
        conn.close()
    except sql.Error as e:
        print(f"Database error: {e}")

print("\t\tWelcome to the Student Medical Record Management System!\t\t")
create_table()
while True:
    print("\n1. Sign up")
    print("2. Sign in")
    print("3. Exit")
    choice = user_input("Enter your choice: ", int)

    if choice == 1:
        sign_up()
    elif choice == 2:
        sign_user=user_input("\n1. Sign in as Student\n2. Sign in as Administrator\n3. Exit\nEnter your choice: ", int)
        if sign_user==1:
            losersign_in()
        elif sign_user==2:
            adminsign_in()
        elif sign_user==3:
            print("Returning to main menu . . .")
            continue
        else:
            print("Invalid choice. Please try again.")
    elif choice == 3:
        print("Exiting...\n")
        break
    else:
        print("Invalid choice. Please try again.")
