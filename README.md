# E-Commerce Platform for Women's Beauty Products

Welcome to the future of beauty shopping! Our platform is designed to revolutionize the way customers discover, explore, and purchase skincare, makeup, hair care, and other beauty essentials.

## Live Link
🔗 [Beauty Shop E-Commerce Website](https://beauty-shop-ecomm-website.onrender.com/)

---

## System Features

### User and Admin Authentication
- Users and admins can sign up and log in.
- Admins have access to a dedicated dashboard for managing products and customers.

### Admin CRUD Operations
- Admins can create, read, update, and delete (CRUD) products and customer details.
- Admins can view and update order status.

### User Cart Management
- Users can view products, add items to their cart, and remove items as needed.

### Search Functionality
- Users can search for products using the search bar.
- Filter functionality is available in the shop section.

### Stock Management
- Admins can manage product stock levels through the admin dashboard.

### Wishlist Feature
- Customers can save items to their wishlist for later purchases.


### Secure Product Payment via M-Pesa
- **STK Push API** (for mobile payments)
- **C2B API** (for manual payments via Paybill/Till Number)
- **Transaction Status API** (to verify successful payments)

---

## Technologies Used

### Backend Technologies
- **Flask** - Lightweight web framework
- **Flask-Login** - User authentication and session management
- **Flask-Migrate** - Database migration handling
- **Flask-SQLAlchemy** - ORM for database interactions
- **Flask-WTF** - Form validation and handling
- **Werkzeug** - Security and utility functions

### Database
- **PostgreSQL** - Relational database management system
- **SQLAlchemy** - ORM for database abstraction
- **Psycopg2-binary** - PostgreSQL adapter for Python

### Frontend Technologies
- **Jinja2** - Templating engine for dynamic HTML rendering

### Payment Integration
- **Intasend-Python** - Payment gateway integration for transactions

### Web Server & Deployment
- **Gunicorn** - WSGI HTTP server for running the Flask app
- **Greenlet** - Concurrency library for efficient request handling

### Utilities & Security
- **Python-dotenv** - Environment variable management
- **Requests** - Handling API requests
- **Certifi** - SSL certificate validation
- **MarkupSafe** - Preventing XSS attacks
- **Itsdangerous** - Handling cryptographic signing
- **WTForms** - Form validation and management
- **Click** - Command-line utilities

---

### Development Setup

1. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up the Database**:
   - Run the following command to initialize the database:
     ```bash
     flask db upgrade
     ```

4. **Run the Application**:
   - Use either of the following commands:
     ```bash
     flask run
     ```
     **OR**
     ```bash
     python3 main.py  # Allows for auto-refresh to view changes
     ```
   - The app will be available at `http://127.0.0.1:5000/`.

---
### *Future Updates*

### Reviews and Ratings
- Users can leave reviews on products after making a purchase.

### Reporting Service
- Functionality: Generates analytical reports.
- Features: Provides insights on sales trends, customer behavior, and inventory management

### Order Cancellation Functionality 
- Ability of users to cancel orders.


## About
This e-commerce platform specializes in beauty and cosmetic products, providing users with a seamless shopping experience, secure transactions, and easy navigation. Built with Flask, it supports authentication, product management, and smooth payment integration.

For more details, refer to the project documentation.


