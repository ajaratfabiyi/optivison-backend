# Optivus Backend

Optivus Backend is a **Django + Django REST Framework** API with Celery task processing, supporting:
- **User authentication** (custom user model, referrals, 2FA, PIN)
- **KYC verification** (document uploads, admin approval)
- **Transactions** (deposits, withdrawals, bonuses)
- **Withdrawal requests** & admin payout handling
- **Dashboard** stats & referral tree
- **Webhook processing** (Stripe & external services)
- Shared **utilities, constants, and exceptions** for consistency

---

## 📂 Project Structure

optivus_backend/
├── manage.py
├── requirements.txt
├── .env.example
├── README.md
├── celery.py
│
├── optivus_backend/ # Project settings & root config
│ ├── init.py
│ ├── settings.py
│ ├── urls.py
│ ├── asgi.py
│ ├── wsgi.py
│
├── users/ # Custom User & auth logic
├── kyc/ # KYC uploads & verification
├── transactions/ # All money movements
├── withdrawals/ # Withdrawal requests
├── dashboard/ # Stats & referral tree
├── admin_panel/ # Admin-only endpoints
├── webhooks/ # Stripe & external service webhooks
└── common/ # Shared utilities & constants

yaml
Copy
Edit

---

## 🛠 Requirements

- Python **3.10+**
- PostgreSQL **13+**
- Redis (for Celery task queue)
- [Pipenv](https://pipenv.pypa.io/) or `venv` (optional, for env management)

---

## ⚙️ Installation

1️⃣ **Clone the repository**
```bash
git clone https://github.com/your-org/optivus_backend.git
cd optivus_backend
2️⃣ Create & activate a virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
3️⃣ Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Set up environment variables

bash
Copy
Edit
cp .env.example .env
# Edit .env with your local settings
5️⃣ Apply database migrations

bash
Copy
Edit
python manage.py migrate
6️⃣ Create a superuser

bash
Copy
Edit
python manage.py createsuperuser
🚀 Running the Project
Development server
bash
Copy
Edit
python manage.py runserver
API will be available at http://127.0.0.1:8000/

Celery worker
bash
Copy
Edit
celery -A optivus_backend worker -l info
Celery beat (for scheduled tasks)
bash
Copy
Edit
celery -A optivus_backend beat -l info
📡 API Endpoints
Auth & Users

POST /api/users/register/

POST /api/users/login/

POST /api/users/verify-2fa/

GET /api/users/me/

KYC

POST /api/kyc/upload/

GET /api/kyc/status/

POST /api/kyc/approve/{id}/ (Admin only)

Transactions

POST /api/transactions/deposit/

POST /api/transactions/withdraw/

GET /api/transactions/history/

Withdrawals

POST /api/withdrawals/request/

GET /api/withdrawals/history/

Dashboard

GET /api/dashboard/summary/

GET /api/dashboard/referrals/

Webhooks

POST /api/webhooks/stripe/

🧪 Running Tests
bash
Copy
Edit
pytest
or using Django's test runner:

bash
Copy
Edit
python manage.py test
🛠 Deployment Notes
Use Gunicorn + Nginx for production

Set DEBUG=False in .env

Run migrations on deploy:

bash
Copy
Edit
python manage.py migrate
Collect static files:

bash
Copy
Edit
python manage.py collectstatic --noinput
Use supervised Celery workers (e.g., with systemd or supervisord)

Configure PostgreSQL backups and Redis persistence for reliability

📜 License
This project is proprietary. All rights reserved.

