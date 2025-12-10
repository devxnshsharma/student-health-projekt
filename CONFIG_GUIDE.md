# Configuration Guide

## Environment Setup

### 1. Copy Environment Template
```bash
cp .env.example .env
```

### 2. Configure Database Connection
Edit `.env` with your MySQL credentials:

```bash
# .env file
DB_HOST=localhost          # MySQL host
DB_USER=root              # MySQL username
DB_PASSWORD=your_pass123  # MySQL password
DB_NAME=MedRep            # Database name
```

### 3. Create MySQL Database
```bash
mysql -u root -p
mysql> CREATE DATABASE MedRep;
mysql> EXIT;
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run Application
```bash
python main.py
```

## Admin Setup

### Create Initial Admin Account
```python
# Run in Python shell or create setup script
from models import AdminAuth

# Create admin user
AdminAuth.create_admin(
    username='admin',
    password='SecurePassword123!',
    full_name='System Administrator',
    email='admin@example.com',
    role='SuperAdmin'
)
```

### Login
- Username: admin
- Password: SecurePassword123!

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | MySQL server address | localhost |
| `DB_USER` | MySQL username | root |
| `DB_PASSWORD` | MySQL password | (required) |
| `DB_NAME` | Database name | MedRep |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING/ERROR) | INFO |
| `LOG_FILE` | Log file location | logs/app.log |
| `ADMIN_OTP_SECRET` | OTP for admin (demo only) | 0001 |

## Security Best Practices

✓ Store `.env` in `.gitignore` - Never commit credentials
✓ Use strong passwords (min 8 characters, mixed case, numbers, symbols)
✓ Rotate credentials regularly
✓ Use HTTPS in production
✓ Restrict database user permissions
✓ Enable MySQL binary logging for audit trail
✓ Regular backups of database

## Database User Permissions

For production, create a restricted MySQL user:

```sql
CREATE USER 'medrep'@'localhost' IDENTIFIED BY 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON MedRep.* TO 'medrep'@'localhost';
FLUSH PRIVILEGES;
```

Then update `.env`:
```
DB_USER=medrep
DB_PASSWORD=secure_password
```

## Troubleshooting

### Connection Error
```
Error: Access denied for user 'root'@'localhost'
```
- Verify MySQL is running
- Check username/password in `.env`
- Ensure database exists: `SHOW DATABASES;`

### Import Error
```
No module named 'pymysql'
```
- Run: `pip install -r requirements.txt`

### Database Not Found
```
Error: Unknown database 'MedRep'
```
- Create database: `CREATE DATABASE MedRep;`

### Permission Denied
```
Error: Access denied for user
```
- Verify user has correct permissions (GRANT statement above)

## Docker Setup (Optional)

```dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

```bash
# Build image
docker build -t medrep .

# Run container with MySQL link
docker run -e DB_HOST=mysql_host -e DB_PASSWORD=pass medrep
```

## Production Checklist

- [ ] Update database credentials in `.env`
- [ ] Set `LOG_LEVEL=WARNING` for production
- [ ] Configure MySQL for automatic backups
- [ ] Enable binary logging
- [ ] Use environment-specific `.env` files
- [ ] Implement HTTPS/SSL
- [ ] Set up monitoring and alerts
- [ ] Regular security audits
- [ ] Implement 2FA
- [ ] Setup log aggregation

## Support

For configuration issues:
1. Check logs in `logs/` directory
2. Verify all credentials in `.env`
3. Ensure MySQL service is running
4. Run: `pytest test_health.py` to verify setup
