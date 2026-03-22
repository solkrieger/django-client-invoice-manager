Django Client & Invoice Manager

A full-stack Django web application for managing clients, invoices, and invoice items with authentication, dashboard metrics, and secure multi-user data isolation.

🚀 Features

User authentication (register, login, logout)
Client management (CRUD)
Invoice management (CRUD)
Invoice item management (CRUD)
Automatic invoice total calculation
Dashboard with:
Paid / unpaid totals
Recent invoices
Invoice filtering (status)
Secure user data isolation
Custom 404 page
Bootstrap-based UI
Deployed on Render

🛠 Tech Stack

Python 3
Django
PostgreSQL (production)
SQLite (development)
Bootstrap
Gunicorn
Render (deployment)

🔐 Security

All data scoped to authenticated user
Object-level access checks
CSRF protection enabled
No secrets stored in code (env variables)
⚙️ Setup (Local)
git clone https://github.com/solkrieger/django-client-invoice-manager.git
cd django-client-invoice-manager

python -m venv .venv
.venv\Scripts\activate   # Windows

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver

🌍 Environment Variables

Create a .env file:
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True

📊 Usage
Register a new account
Create clients
Create invoices
Add invoice items
View totals and dashboard metrics

🌐 Live Demo

👉 https://invoice-manager-ivqa.onrender.com/

📌 Future Improvements

Export invoice as PDF
REST API (Django REST Framework)
AI invoice item description generator
Advanced filtering (date range, client)
🧠 What I Learned
Django architecture (models, views, templates)
Authentication and permissions
Querysets and relationships
Deployment with PostgreSQL
Debugging production issues
📄 License

This project is for educational and portfolio purposes.
