# Inventory Management System

## Overview

A Flask-based web application for managing inventory across multiple warehouses. The system tracks products, storage locations, and product movements between locations. Built as a hiring test project, it provides CRUD operations for inventory management and generates balance reports showing current stock levels by location.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **Flask**: Lightweight Python web framework chosen for rapid development and simplicity
- **SQLAlchemy**: ORM for database operations, providing abstraction layer over raw SQL
- **Flask-WTF**: Form handling and validation with CSRF protection

### Database Design
- **Three-table schema**: Products, Locations, and ProductMovements
- **String-based primary keys**: Allows for human-readable identifiers (e.g., "PROD001", "WH-A")
- **Flexible movement tracking**: Supports incoming stock (only to_location), outgoing stock (only from_location), and transfers (both locations)
- **Automatic timestamps**: ProductMovement records include creation timestamps

### Frontend Architecture
- **Server-side rendering**: Traditional web app using Jinja2 templates
- **Bootstrap CSS**: Responsive UI framework for clean, professional appearance
- **Template inheritance**: Base template with navigation shared across all pages

### Form Handling
- **WTForms integration**: Structured form validation and rendering
- **Dynamic dropdowns**: Location and product selects populated from database
- **CSRF protection**: Built-in security against cross-site request forgery

### Application Structure
- **Modular design**: Separate files for models, forms, routes, and database configuration
- **Blueprint-style routing**: Routes registered through a central function
- **Environment-based configuration**: Database URL and secret key from environment variables

### Data Flow
1. **CRUD Operations**: Full create, read, update, delete for all entities
2. **Movement tracking**: Records all inventory transfers with timestamps
3. **Balance calculation**: Aggregates movements to show current stock levels
4. **Referential integrity**: Foreign key relationships maintain data consistency

### Reporting System
- **Balance report**: Shows current inventory by product and location
- **Movement history**: Tracks all inventory changes over time
- **Aggregate calculations**: Sums incoming and outgoing quantities per location

## External Dependencies

### Python Packages
- **Flask**: Web framework
- **Flask-SQLAlchemy**: Database ORM
- **Flask-WTF**: Form handling and validation
- **WTForms**: Form field definitions and validators

### Frontend Libraries
- **Bootstrap 5.1.3**: CSS framework via CDN
- **Bootstrap JavaScript**: Interactive components and utilities

### Database
- **SQLAlchemy-compatible database**: Currently configured for any SQLAlchemy-supported database via DATABASE_URL environment variable
- **Connection pooling**: Configured with pool recycling and pre-ping for reliability

### Environment Variables
- **DATABASE_URL**: Database connection string
- **FLASK_SECRET_KEY**: Session encryption key (falls back to default for development)

### Development Tools
- **Built-in Flask development server**: Hot reloading enabled for development
- **Debug mode**: Error tracebacks and auto-reload during development