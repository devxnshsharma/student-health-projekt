# Deployment & Getting Started Guide

## ⚡ 5-Minute Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure database
cp .env.example .env
# Edit .env with your MySQL credentials

# 3. Run interactive setup
python setup.py

# 4. Start application
python main.py
```

## 📋 Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8 or newer
- ✅ MySQL 5.7 or newer running
- ✅ pip package manager
- ✅ Write access to project directory

Verify with:
```bash
python --version        # Should be 3.8+
mysql --version         # Should be 5.7+
pip --version           # Should be 20.0+
```

## 🔧 Step-by-Step Installation

### 1. Create MySQL Database
```bash
mysql -u root -p
# Enter your MySQL password

mysql> CREATE DATABASE MedRep;
mysql> EXIT;
```

### 2. Install Python Dependencies
```bash
cd projekt
pip install -r requirements.txt
```

This installs:
- PyMySQL (database driver)
- bcrypt (password hashing)
- python-dotenv (configuration)
- pytest (testing)

### 3. Configure Environment
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=MedRep
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
ADMIN_OTP_SECRET=0001
```

### 4. Initialize Application
```bash
python setup.py
```

This script will:
- ✓ Verify MySQL connection
- ✓ Create database tables
- ✓ Create initial admin account
- ✓ Test the setup

### 5. Launch Application
```bash
python main.py
```

## 🎯 First-Time Usage

After starting the app:

1. **Main Menu** appears with 4 options:
   - 1. Student Registration
   - 2. Student Login
   - 3. Admin Login
   - 4. Exit

2. **Admin Login:**
   - Username: (what you entered in setup.py)
   - Password: (what you entered in setup.py)

3. **Admin Dashboard** features:
   - View/Sort/Update/Delete records
   - Run reports
   - View audit logs
   - Manage vaccinations

4. **Student Registration:**
   - Enter personal details
   - Medical information
   - Vaccination history
   - System auto-validates

## 📚 Documentation Guide

| Document | Purpose | Read When |
|----------|---------|-----------|
| README.md | Quick overview | Starting |
| SETUP_GUIDE.md | Comprehensive guide | Need details |
| CONFIG_GUIDE.md | Configuration help | Setup issues |
| API_REFERENCE.md | Code examples | Developing |
| IMPLEMENTATION_SUMMARY.md | Feature list | Evaluating |
| FILES_MANIFEST.md | File overview | Exploring project |

## 🧪 Testing

Run all tests:
```bash
pytest test_health.py -v
```

Expected output:
```
test_health.py::TestBMICalculation::test_bmi_normal PASSED
test_health.py::TestBMICalculation::test_bmi_underweight PASSED
...
======== 12 passed in 0.25s ========
```

## 📊 Verify Installation

Check that everything works:

```python
# test_connection.py
from db import create_connection, create_tables

print("Testing database connection...")
try:
    conn = create_connection()
    print("✓ Connected to MySQL")
    create_tables()
    print("✓ Tables created successfully")
    conn.close()
    print("\n✓ Installation successful!")
except Exception as e:
    print(f"✗ Error: {e}")
```

Run it:
```bash
python test_connection.py
```

## 🔐 Security Verification

- [ ] .env file has correct credentials
- [ ] .env is in .gitignore (never commit)
- [ ] MySQL user has limited permissions
- [ ] Database backups configured
- [ ] Logs directory is writable
- [ ] Admin password is strong

## 🚀 Running in Production

For production deployment:

1. Use environment-specific .env file
2. Set LOG_LEVEL=WARNING
3. Configure database backups
4. Restrict database user permissions
5. Use HTTPS if adding web frontend
6. Enable MySQL binary logging
7. Setup monitoring and alerts

See CONFIG_GUIDE.md for production checklist.

## 🆘 Troubleshooting

### "Connection refused" error
```
Problem: Can't connect to MySQL
Solution: 
  - Verify MySQL is running: sudo systemctl status mysql
  - Check credentials in .env
  - Ensure database exists: mysql -u root -p -e "SHOW DATABASES;"
```

### "Module not found" error
```
Problem: Missing Python package
Solution:
  - Install dependencies: pip install -r requirements.txt
  - Verify installation: pip list | grep -E "PyMySQL|bcrypt|dotenv"
```

### "Access denied" error
```
Problem: Wrong database credentials
Solution:
  - Verify MySQL user exists: mysql -u root -p -e "SELECT user FROM mysql.user;"
  - Update .env with correct credentials
  - Test connection: mysql -u your_user -p -h localhost
```

### "Database does not exist" error
```
Problem: MedRep database not created
Solution:
  - Create it: mysql -u root -p -e "CREATE DATABASE MedRep;"
  - Verify: mysql -u root -p -e "SHOW DATABASES;" | grep MedRep
```

### Tests failing
```
Problem: Unit tests not passing
Solution:
  - Run: pytest test_health.py -v
  - Check error messages
  - Ensure Python 3.8+ with pytest installed
```

## 📝 Common Tasks

### Create Additional Admin
```python
from models import AdminAuth

AdminAuth.create_admin(
    username='john',
    password='SecurePass123!',
    full_name='John Doe',
    email='john@example.com',
    role='Admin'
)
```

### Backup Database
```bash
mysqldump -u root -p MedRep > backup_$(date +%Y%m%d).sql
```

### View Recent Logs
```bash
tail -50 logs/app_*.log
```

### Reset Admin Password (via MySQL)
```bash
# Last resort - change directly in database
mysql -u root -p -e "UPDATE MedRep.admins SET LoginAttempts=0, LockedUntil=NULL WHERE Username='admin';"
```

## 📞 Support Contacts

For issues:
1. Check logs in `logs/` directory
2. Review relevant documentation
3. Verify .env configuration
4. Run `pytest test_health.py -v` to test setup
5. Check database connection with `python test_connection.py`

## 🎓 Learning Path

1. **Start**: README.md
2. **Setup**: CONFIG_GUIDE.md
3. **Use**: SETUP_GUIDE.md
4. **Code**: API_REFERENCE.md
5. **Deploy**: CONFIG_GUIDE.md (Production section)

## ✅ Post-Installation Checklist

- [ ] All dependencies installed
- [ ] .env file configured
- [ ] MySQL database created
- [ ] setup.py ran successfully
- [ ] Admin account created
- [ ] Tests passing (pytest)
- [ ] Application starts (python main.py)
- [ ] Can login as admin
- [ ] Can register student
- [ ] Can view records
- [ ] Logs being created

## Next Steps

1. **Explore Admin Dashboard:**
   - View sample records
   - Try sorting and filtering
   - Check reports

2. **Register Test Student:**
   - Enter sample medical data
   - Verify validation works
   - View generated record

3. **Check Analytics:**
   - View blood group distribution
   - Check vaccination coverage
   - Export sample report

4. **Review Code:**
   - Read API_REFERENCE.md
   - Explore source files
   - Understand architecture

5. **Customize:**
   - Modify validation rules
   - Add new fields
   - Extend reports

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.8 | 3.11+ |
| MySQL | 5.7 | 8.0+ |
| RAM | 512MB | 2GB+ |
| Disk | 100MB | 1GB |
| Network | (local) | 100Mbps+ |

## File Locations After Installation

```
projekt/
├── .env                    # Your configuration (secret)
├── logs/
│   └── app_20241210.log   # Daily logs
├── *.py                    # Python source files
├── *.md                    # Documentation files
└── *.csv                   # Exported reports (as needed)
```

## Performance Tips

- Database runs locally for best performance
- Log files automatically rotate at 10MB
- CSV exports stream data to prevent memory issues
- Parameterized queries prevent SQL errors
- Password hashing adds ~100ms per auth

## Regular Maintenance

- Weekly: Check logs for errors
- Monthly: Review audit logs
- Quarterly: Database backup verification
- Yearly: Update dependencies

---

**You're all set! Start with `python main.py` and enjoy the system!** 🎉
