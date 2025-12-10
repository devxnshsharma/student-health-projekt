# Student Medical Record Management System (Python + MySQL)

A terminal-based Student Medical Record Management System built with Python and MySQL.  
It allows schools to store, search, and manage students' medical records, including basic demographics, physical metrics (height, weight, BMI), allergies, and vaccination history.

## Tech Stack

- **Language:** Python 3.x  
- **Database:** MySQL  
- **Client:** Command-line interface (CLI)  
- **Libraries:**
  - `pymysql` for MySQL connectivity
  - `csv` for export
  - `datetime` for date and vaccination alerts
  

### 1. Prerequisites
- Python 3.8+
- MySQL 5.7+
- pip package manager

### 2. Installation
```bash
# Clone/navigate to project directory
cd projekt

# Install dependencies
pip install -r requirements.txt

# Create MySQL database
mysql -u root -p -e "CREATE DATABASE MedRep;"

# Configure environment
cp .env.example .env
# Edit .env with your database credentials
```

### 3. Run Application
```bash
python main.py
```

# Features

- Student registration with:
  - Personal details (name, sex, age, class/section, date of birth, blood group)
  - Physical records (height, weight, automatic BMI calculation and status)
  - Allergy information
  - Detailed vaccination history (Tetanus, Cholera, Typhoid, Hepatitis A/B, Chickenpox, Measles, COVID)

- Role-based access:
  - **Student** can sign in and view own records.
  - **Administrator** can:
    - View and search records (by AdminNo, name, class/section)
    - Sort records (name, age, class, blood group)
    - Update records (height, weight, class, allergies, vaccination status, notes)
    - Delete records (with confirmation)
    - Search by allergy
    - Generate vaccination alerts (e.g., Tetanus booster due, missing HepB/COVID)
    - Export all records to CSV

- Data storage:
  - MySQL database using PyMySQL
  - Separate `users` and `records` tables
  - Parameterized queries for safer database operations

## Project Structure

```
projekt/
├── main.py              # Application entry point
├── db.py                # Database operations
├── models.py            # Data models (CRUD)
├── ui.py                # CLI interface
├── utils.py             # Utility functions
├── reports.py           # Analytics module
├── logger_config.py     # Logging setup
├── test_health.py       # Unit tests
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment config
└── SETUP_GUIDE.md       # Detailed setup instructions
```

## Configuration

### Environment Variables (.env)
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=MedRep
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### Create Initial Admin
Run once after setup:
```python
from models import AdminAuth
AdminAuth.create_admin('admin', 'password123', 'Admin Name', 'admin@example.com')
```


The application will automatically create the required tables if they do not exist.

## Usage

### Main Menu

When the program starts, you can:

- **Sign up** – Register a new student and create a full medical record.
- **Sign in** – Choose to sign in as:
- Student
- Administrator
- **Exit** – Close the application.

### Student Sign-In

- Enter your Admin No. and name.
- View your personal and medical details, including BMI.

### Administrator Dashboard

After successful admin authentication, you can:

1. **View User Records** – View all records or search by AdminNo, name, or class/section.
2. **Sort User Records** – Sort by name, age, class, or blood group.
3. **Update User Record** – Modify height, weight, class, allergies, vaccination status, or other notes.
4. **Delete User Record** – Remove a student’s record (with confirmation).
5. **Vaccination Alerts** – List students who are:
- Due for Tetanus booster (5+ years since last dose)
- Missing Hepatitis B vaccination
- Missing critical vaccinations (HepB, COVID, Measles)
6. **Search by Allergy** – Find students with a given allergy keyword.
7. **Export Records to CSV** – Export all records to a timestamped CSV file.
8. **Exit** – Exit the admin dashboard.

## Security Notes

- All database operations use parameterized queries to reduce risk of SQL injection.
- In the current version, admin credentials are stored in the source file for demonstration.
- For production use:
- Move secrets and DB credentials to environment variables.
- Store admin users and hashed passwords in the database.
- Add proper authentication and authorization checks.

## Possible Improvements

- Refactor into modules (`db.py`, `models.py`, `utils.py`, etc.).
- Add unit tests for core logic (BMI calculation, validation, alert computations).
- Encrypt sensitive fields and implement proper password hashing.
- Build a simple web UI (Flask/FastAPI) on top of the same database schema.
- Add role management for school nurse, class teacher, etc.

## Author

- Devansh Sharma
- GitHub: [@devxnshsharma](https://github.com/devxnshsharma)
