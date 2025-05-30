# Django Payment Gateway

A secure payment processing system with Django and PostgreSQL featuring encrypted card storage, payment validation, and callback integration.

## Key Features  
- 🔐 Encrypted card storage (Fernet)  
- ✅ Luhn algorithm validation  
- 💳 Mock bank system with balance checks  
- 🔄 Callback notifications  
- 🚀 REST API + Web Interface  

## Quick Setup  

### Local Installation  
1. Clone repo & create virtual env:  
   ```bash
   git clone <repo-url> && cd django-payment-system
   python -m venv venv && source venv/bin/activate
   ```

2. Install PostgreSQL:  
   ```bash
   sudo apt install postgresql  # Ubuntu/Debian
   brew install postgresql      # macOS
   ```

3. Configure database:  
   ```sql
   CREATE DATABASE payment_system;
   CREATE USER payment_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE payment_system TO payment_user;
   ```

4. Install dependencies & run:  
   ```bash
   pip install -r requirements.txt
   cp .env.example .env  # Edit with your DB credentials
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py create_test_cards  # Add test payment cards
   python manage.py runserver
   ```


## API Endpoints  
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/payments/` | POST | Create payment |
| `/api/payments/{id}/` | GET | Check status |
| `/payment/{id}/process/` | POST | Submit card details |

**Sample Request:**  
```json
{
  "amount": 100.00,
  "callback_url": "https://your-app.com/callback"
}
```

## Testing  
Use the `create_test_cards` management command to populate the system with test payment cards for development.

## Security  
- Fernet encryption for all card data  
- Automatic HTTPS redirects in production  
- CSRF protection enabled  


