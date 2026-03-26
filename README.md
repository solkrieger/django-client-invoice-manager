Django Client & Invoice Manager
A production-ready Django web application for managing clients, invoices, and invoice items with authentication, PDF export, REST API, and PostgreSQL deployment.

🚀 Features
🔐 User authentication (register, login, logout)
👥 Client management (CRUD)
🧾 Invoice management (CRUD)
📦 Invoice item management
🧮 Automatic total calculation
📊 Dashboard with paid/unpaid metrics
🔍 Invoice filtering by status
📄 PDF invoice export
🔌 REST API (Django REST Framework)
🛡 User data isolation (secure per user)
🎨 Bootstrap UI
⚠️ Custom 404 page
☁️ Deployed on Render with PostgreSQL

🛠 Tech Stack
Python 3
Django
Django REST Framework
PostgreSQL
SQLite (development)
Bootstrap 5
Gunicorn
Render

🔐 Security
Authenticated access required for all data
Object-level permission checks (user=request.user)
CSRF protection enabled
Environment variables for secrets

⚙️ Local Setup
git clone https://github.com/solkrieger/django-client-invoice-manager.git
cd django-client-invoice-manager

python -m venv .venv
.venv\Scripts\activate   # Windows

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver

🌍 Environment Variables
Create .env:

DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True

🌐 Live Demo
👉 https://invoice-manager-ivqa.onrender.com/


🔌 API Endpoints
/api/clients/
/api/invoices/

📌 Future Improvements
PDF styling enhancements
Advanced filtering (date range, client)
JWT authentication
Invoice email sending

🧠 What I Learned
Django architecture (models, views, templates)
Database relationships & querysets
Authentication & permissions
Building REST APIs
Generating PDFs
Deploying with PostgreSQL
Debugging production issues
📄 License
This project is for educational and portfolio use.

