# Flask Inventory Management System

A comprehensive inventory management system built with Flask, featuring real-time stock tracking, movement management, and balance reporting.

## Features

### Core Functionality
- **Home Page**:
![alt text](image.png)
- **Product Management**: Add, edit, view, and delete products
![alt text](image-1.png)
- **Location Management**: Manage warehouse locations and storage areas
![alt text](image-2.png)
- **Movement Tracking**: Record product movements in, out, and between locations
![alt text](image-3.png)
- **Real-time Balance Tracking**: Automatic stock balance calculation and validation
![alt text](image-4.png)
- **Balance Reporting**: Comprehensive inventory reports with current stock levels
![alt text](image-5.png)

### Advanced Features
- **Stock Validation**: Prevents overselling with real-time stock checks
- **Automatic Balance Updates**: Stock levels update automatically with each movement
- **Movement History**: Complete audit trail of all inventory movements
- **API Endpoints**: RESTful API for integration with other systems
- **Responsive Design**: Modern, mobile-friendly user interface

## Technical Requirements

### Dependencies
- Python 3.8+
- Flask 2.3.3
- Flask-SQLAlchemy 3.0.5
- Flask-WTF 1.1.1
- PyMySQL 1.1.0
- MySQL database

### Database Schema
- **Products**: Store product information
- **Locations**: Manage warehouse/storage locations
- **Product Movements**: Track all inventory movements
- **Product Balances**: Real-time stock balance tracking

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Flask_InventoryManagement
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**
   - Create a MySQL database named `inventory_management`
   - Update database connection in `main.py` or set environment variable:
     ```bash
     export DATABASE_URL="mysql+pymysql://username:password@localhost/inventory_management"
     ```

4. **Run the application**
   ```bash
   python main.py
   ```
   Or use the batch file on Windows:
   ```bash
   run_app.bat
   ```

5. **Access the application**
   - Web Interface: http://localhost:5000
   - API Documentation: See API Endpoints section below

## Usage Guide

### Getting Started
1. **Add Products**: Create your product catalog with unique IDs and descriptions
2. **Set up Locations**: Define your warehouse locations and storage areas
3. **Record Movements**: Track inventory movements to maintain accurate stock levels

### Movement Types
- **Incoming Stock**: Leave "From Location" empty, specify "To Location"
- **Outgoing Stock**: Specify "From Location", leave "To Location" empty
- **Transfers**: Specify both "From Location" and "To Location"

### Stock Validation
The system automatically validates stock availability:
- Prevents negative stock levels
- Shows current balance before movements
- Provides clear error messages for insufficient stock



