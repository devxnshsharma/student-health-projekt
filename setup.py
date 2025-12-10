#!/usr/bin/env python
"""
Setup script - Initialize application and create initial admin account
Run once after first installation
"""
import sys
import os

def setup_environment():
    """Setup environment and configuration"""
    print("="*60)
    print("Medical Record Management System - Setup")
    print("="*60)
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("\n❌ .env file not found!")
        print("Please copy .env.example to .env and configure your database:")
        print("  cp .env.example .env")
        print("\nEdit .env with your database credentials")
        sys.exit(1)
    
    print("\n✓ .env file found")
    
    # Check if requirements installed
    try:
        import pymysql
        import bcrypt
        import dotenv
        print("✓ All dependencies installed")
    except ImportError as e:
        print(f"\n❌ Missing dependency: {e}")
        print("Install with: pip install -r requirements.txt")
        sys.exit(1)
    
    # Test database connection
    print("\n🔄 Testing database connection...")
    try:
        from db import create_connection, create_tables
        conn = create_connection()
        print("✓ Database connection successful")
        
        # Create tables
        print("🔄 Creating database tables...")
        create_tables()
        print("✓ Database tables created")
        
        conn.close()
    except Exception as e:
        print(f"\n❌ Database error: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure MySQL is running")
        print("2. Check database credentials in .env")
        print("3. Verify database exists: CREATE DATABASE MedRep;")
        sys.exit(1)
    
    # Create initial admin
    print("\n🔄 Creating initial admin account...")
    print("-" * 60)
    
    from models import AdminAuth
    
    username = input("Enter admin username (default: admin): ").strip() or "admin"
    password = input("Enter admin password: ").strip()
    fullname = input("Enter admin full name: ").strip() or "Administrator"
    email = input("Enter admin email: ").strip() or "admin@example.com"
    
    try:
        success, message = AdminAuth.create_admin(
            username=username,
            password=password,
            full_name=fullname,
            email=email,
            role='SuperAdmin'
        )
        
        if success:
            print(f"\n✓ {message}")
            print("\n" + "="*60)
            print("Setup Complete!")
            print("="*60)
            print(f"\nAdmin Account Details:")
            print(f"  Username: {username}")
            print(f"  Role: SuperAdmin")
            print(f"\nYou can now run: python main.py")
            print("="*60)
        else:
            print(f"\n❌ Error: {message}")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error creating admin: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        setup_environment()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
        sys.exit(0)
