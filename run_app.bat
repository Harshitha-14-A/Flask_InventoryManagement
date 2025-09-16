@echo off
REM Set MySQL connection details here
set DATABASE_URL=mysql+pymysql://root:Root12345@localhost/inventory_management
REM Optional: set Flask secret key
set FLASK_SECRET_KEY=your_secret_key_here

REM Run the Flask app
python main.py
