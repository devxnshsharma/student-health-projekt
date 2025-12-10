"""
Main application entry point
"""
import logging
import sys
from logger_config import setup_logger
from db import create_tables
from ui import CLI

# Setup logger
logger = setup_logger()

def main():
    """Main application"""
    try:
        logger.info("Application starting...")
        
        # Create database tables
        create_tables()
        
        # Initialize CLI
        cli = CLI()
        cli.main_menu()
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        print("\nApplication terminated.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
