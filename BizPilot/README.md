# BizPilot - Multi-Tenant Business Management Platform

## Overview
BizPilot is a multi-tenant SaaS platform designed to help small and medium-sized businesses modernize their operations. Similar to Salesforce or Microsoft 365, but tailored for local businesses across different industries.

## Version 1.0 Features
- **Multi-tenancy**: Complete data isolation between businesses
- **Industry-Specific Apps**:
  - **Retail**: E-commerce and inventory management
  - **Tailoring**: Measurement storage and task management
  - **Education**: (Coming soon)

## Technology Stack
- **Backend**: Django 4.2+
- **API**: Django REST Framework
- **Authentication**: JWT (SimpleJWT)
- **Database**: MySQL 

## Project Structure
```
bizpilot/
├── apps/
│   ├── account/          # User authentication & business registration
│   ├── industry/         # Industry types management
│   ├── customer/         # Customer management (shared)
│   ├── core/            # Shared utilities and mixins
│   ├── retail/          # Retail-specific features
│   └── tailoring/       # Tailoring-specific features
├── bizpilot/            # Main project settings
├── media/               # Uploaded files
├── static/              # Static files
├── requirements.txt
└── manage.py
```

## Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd bizpilot
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
Create a `.env` file in the project root:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

### 5. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create superuser
```bash
python manage.py createsuperuser
```

### 7. Run development server
```bash
python manage.py runserver
```

## API Documentation

### Authentication Endpoints
- `POST /api/account/register/` - Business registration
- `POST /api/account/login/` - Login (returns JWT tokens)
- `POST /api/account/token/refresh/` - Refresh access token

### Customer Endpoints
- `GET /api/customers/` - List all customers (scoped to business)
- `POST /api/customers/` - Create new customer
- `GET /api/customers/{id}/` - Get customer details
- `PUT /api/customers/{id}/` - Update customer
- `DELETE /api/customers/{id}/` - Delete customer

### Retail Endpoints
- `GET /api/retail/categories/` - List categories
- `POST /api/retail/categories/` - Create category
- `GET /api/retail/products/` - List products
- `POST /api/retail/products/` - Create product
- `GET /api/retail/products/search/?q=query` - Search products
- `GET /api/retail/inventory-history/` - View inventory changes

### Tailoring Endpoints
- `GET /api/tailoring/measurements/` - List measurements
- `POST /api/tailoring/measurements/` - Create measurement
- `GET /api/tailoring/tasks/` - List tasks
- `POST /api/tailoring/tasks/` - Create task
- `PATCH /api/tailoring/tasks/{id}/` - Update task status

## Key Features

### Multi-Tenancy
All data is automatically scoped to the authenticated user's business. This is enforced at the database level using:
1. Foreign key relationships to the Business model
2. Automatic filtering in querysets via mixins
3. Validation in serializers to prevent cross-business data access

### Authentication
- JWT-based authentication
- Email-based login
- Business owners can create staff accounts
- Role-based permissions (owner vs staff)

### Data Isolation
- Each business only sees their own data
- Customers are scoped to businesses
- Products, measurements, and tasks are business-specific
- No cross-contamination of data between businesses

## Testing
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.account
python manage.py test apps.retail
```

## Deployment Checklist
- [ ] Set DEBUG=False
- [ ] Configure production database (PostgreSQL)
- [ ] Set up static file serving
- [ ] Configure CORS settings
- [ ] Set up media file storage
- [ ] Configure email backend
- [ ] Set up SSL/HTTPS
- [ ] Configure allowed hosts

## Security Features
- JWT authentication with refresh tokens
- Password hashing with Django's default PBKDF2
- Business-level data isolation
- Permission-based access control
- CORS protection
- SQL injection protection (Django ORM)

## Future Enhancements (v2.0+)
- [ ] Education industry module
- [ ] Advanced reporting and analytics
- [ ] Email notifications
- [ ] Mobile app support
- [ ] Payment integration
- [ ] Multi-language support
- [ ] Advanced role management

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
[License Here]

## Support
For issues and questions, please open an issue on GitHub or contact support@bizpilot.com
