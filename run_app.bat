@echo off
REM Set MySQL connection details here
set DATABASE_URL=mysql+pymysql://root:Root12345@localhost/inventory_management

REM Run the Flask app
python main.py
