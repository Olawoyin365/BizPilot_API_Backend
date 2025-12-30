# BizPilot - Multi-Tenant Business Management API

## Project Overview

BizPilot is a Django REST Framework-based API that provides multi-tenant business management solutions for small and medium businesses. This API supports multiple industry verticals including Retail, Tailoring, and Education (coming soon).

---

## Quick Start

### 1. Activate Virtual Environment

```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 2. Run Development Server

```bash
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000/`

### 3. Access Admin Panel

```bash
http://127.0.0.1:8000/admin/
```

Login with superuser credentials.

---

## Project Structure

```
BizPilot/
├── BizPilot/                 # Main project settings
│   ├── settings.py          # Django configuration
│   └── urls.py              # Main URL routing
│
├── apps/                     # All application modules
│   ├── core/                # Shared utilities (mixins, permissions)
│   ├── account/             # Authentication & business registration
│   ├── industry/            # Industry types management
│   ├── customer/            # Customer management (shared)
│   ├── retail/              # Retail/inventory features
│   └── tailoring/           # Tailoring/measurement features
│
├── media/                    # User uploaded files
├── static/                   # Static files (CSS, JS, images)
├── db.sqlite3               # SQLite database (development)
├── manage.py                # Django management commands
└── requirements.txt         # Python dependencies
```

---

## Available Management Commands

### Database Operations

```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Reset database (delete db.sqlite3 first)
python manage.py migrate --run-syncdb
```

### User Management

```bash
# Create superuser for admin access
python manage.py createsuperuser

# Change user password
python manage.py changepassword <username>
```

### Development

```bash
# Run development server
python manage.py runserver

# Run on different port
python manage.py runserver 8080

# Make server accessible to network
python manage.py runserver 0.0.0.0:8000

# Open Django shell
python manage.py shell

# Check for project issues
python manage.py check
```

### Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.account
python manage.py test apps.retail

# Run with verbosity
python manage.py test --verbosity=2
```

---

## API Endpoints Summary

### Authentication
- `POST /api/account/register/` - Register business
- `POST /api/account/login/` - User login
- `POST /api/token/refresh/` - Refresh JWT token
- `GET /api/account/profile/` - Get user profile
- `GET /api/account/business/` - Get business details

### Industries
- `GET /api/industries/` - List available industries

### Customers
- `GET /api/customers/` - List customers
- `POST /api/customers/` - Create customer
- `GET /api/customers/{id}/` - Customer details
- `PUT/PATCH /api/customers/{id}/` - Update customer
- `DELETE /api/customers/{id}/` - Delete customer

### Retail Module
- `GET /api/retail/categories/` - List categories
- `POST /api/retail/categories/` - Create category
- `GET /api/retail/products/` - List products
- `POST /api/retail/products/` - Create product
- `GET /api/retail/products/low_stock/` - Low stock alerts
- `POST /api/retail/products/{id}/update_inventory/` - Update stock
- `GET /api/retail/inventory-history/` - View inventory changes

### Tailoring Module
- `GET /api/tailoring/measurements/` - List measurements
- `POST /api/tailoring/measurements/` - Create measurement
- `GET /api/tailoring/tasks/` - List tasks
- `POST /api/tailoring/tasks/` - Create task
- `GET /api/tailoring/tasks/today/` - Today's tasks
- `GET /api/tailoring/tasks/overdue/` - Overdue tasks

*See `docs/api-reference.md` for complete API documentation.*

---

## Environment Variables

Create a `.env` file in the project root (optional):

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## Database Schema

### Core Models

**Business** - Tenant model
- store_name, email, phone, country
- industry (FK to Industry)
- owner (FK to CustomUser)

**CustomUser** - Extended user model
- email (used for login), username, phone
- business (FK to Business)
- is_business_owner, is_staff_member

**Industry** - Business types
- name, description, is_active

**Customer** - Shared customer model
- business (FK), name, email, phone, address

### Retail Models

**Category** - Product categories
- business (FK), name, description

**Product** - Inventory items
- business (FK), category (FK)
- name, description, price, stock_quantity
- low_stock_threshold, sku, image

**InventoryHistory** - Audit trail
- product (FK), user (FK)
- change_type, quantity_change
- previous_quantity, new_quantity

### Tailoring Models

**Measurement** - Customer measurements
- business (FK), customer (FK)
- garment_type, measurements (chest, waist, etc.)
- date_taken, notes

**Task** - Tailoring orders
- business (FK), customer (FK), measurement (FK)
- garment_type, description, due_date
- status, price, paid

---

## Multi-Tenancy Implementation

### How It Works

1. **Business Foreign Key**: Every model has `business = models.ForeignKey(Business)`
2. **Automatic Filtering**: `BusinessQuerySetMixin` filters all queries by authenticated user's business
3. **Automatic Assignment**: `BusinessCreateMixin` sets business on object creation
4. **Security**: Cross-business data access is prevented at the database query level

### Core Mixins (apps/core/mixins.py)

```python
# Auto-filter queries by business
class BusinessQuerySetMixin:
    def get_queryset(self):
        return super().get_queryset().filter(business=self.request.user.business)

# Auto-assign business on create
class BusinessCreateMixin:
    def perform_create(self, serializer):
        serializer.save(business=self.request.user.business)
```

### Usage in Views

```python
from apps.core.mixins import BusinessQuerySetMixin, BusinessCreateMixin

class CustomerViewSet(BusinessQuerySetMixin, BusinessCreateMixin, viewsets.ModelViewSet):
    queryset = Customer.objects.all()  # Automatically filtered by business
    serializer_class = CustomerSerializer
```

---

## Authentication Flow

### JWT Token Authentication

1. **Register/Login** → Receive access token (valid 1 hour) and refresh token (valid 7 days)
2. **API Requests** → Include token in header: `Authorization: Bearer <access_token>`
3. **Token Expired** → Use refresh token to get new access token
4. **Refresh Token Expired** → User must login again

### Example Authentication

```bash
# Login
curl -X POST http://127.0.0.1:8000/api/account/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "owner@store.com", "password": "password123"}'

# Use token in requests
curl -X GET http://127.0.0.1:8000/api/customers/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."

# Refresh token
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."}'
```

---

## Common Development Tasks

### Adding a New Industry Module

1. Create new app: `python manage.py startapp modulename apps/modulename`
2. Add to `INSTALLED_APPS` in `settings.py`
3. Create models with `business` foreign key
4. Create serializers, views, URLs
5. Use `BusinessQuerySetMixin` and `BusinessCreateMixin` in views
6. Register models in admin
7. Create and run migrations

### Adding a New Field to Existing Model

1. Add field to model in `models.py`
2. Create migration: `python manage.py makemigrations`
3. Review migration file
4. Apply migration: `python manage.py migrate`
5. Update serializer to include new field
6. Update admin if needed

### Debugging Tips

```bash
# Check for issues before migrations
python manage.py check

# Show SQL for migration
python manage.py sqlmigrate app_name migration_number

# Show current migrations status
python manage.py showmigrations

# Access Django shell for debugging
python manage.py shell
>>> from apps.account.models import Business
>>> Business.objects.all()
```

---

## Testing the API

### Using Django Admin

1. Go to `http://127.0.0.1:8000/admin/`
2. Create industries (Retail, Tailoring)
3. View registered businesses
4. Manage customers, products, etc.

### Using Postman/Insomnia

1. Import the API collection (if available)
2. Set base URL: `http://127.0.0.1:8000/api/`
3. Register a business
4. Copy access token from response
5. Add token to Authorization header for subsequent requests

### Using cURL

See examples in `docs/api-reference.md`

---

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'apps.xxx'`
- **Solution**: Ensure app is in `INSTALLED_APPS` as `'apps.xxx'` not `'xxx'`

**Issue**: `No such table: xxx`
- **Solution**: Run migrations: `python manage.py migrate`

**Issue**: `UNIQUE constraint failed`
- **Solution**: Check for duplicate data. Customer phone must be unique per business.

**Issue**: `Token has expired`
- **Solution**: Use refresh token to get new access token

**Issue**: `Cannot access another business's data`
- **Solution**: This is working as intended! Multi-tenancy is enforced.

### Reset Database

```bash
# WARNING: This deletes all data
# Delete database file
rm db.sqlite3  # Mac/Linux
del db.sqlite3  # Windows

# Recreate database
python manage.py migrate
python manage.py createsuperuser
```

---

## Code Style Guidelines

### Python Code
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to classes and functions
- Keep functions small and focused
- Use type hints where appropriate

### Django Best Practices
- Use Django's built-in features
- Follow DRY (Don't Repeat Yourself)
- Use class-based views for consistency
- Implement proper error handling
- Write database-efficient queries (use select_related/prefetch_related)

### API Design
- Use RESTful conventions
- Return appropriate HTTP status codes
- Provide clear error messages
- Include pagination for list endpoints
- Version your API when making breaking changes

---

## Performance Tips

### Database Optimization
```python
# Use select_related for foreign keys
Product.objects.select_related('business', 'category')

# Use prefetch_related for reverse foreign keys
Business.objects.prefetch_related('products')

# Add database indexes (already in models)
class Meta:
    indexes = [
        models.Index(fields=['business', 'name']),
    ]
```

### Query Optimization
- Avoid N+1 queries
- Use pagination for large datasets
- Cache frequently accessed data
- Use database indexes appropriately

---

## Security Considerations

### Current Implementations
✅ JWT token authentication  
✅ Password hashing (Django default PBKDF2)  
✅ Business-level data isolation  
✅ CORS configuration  
✅ SQL injection protection (Django ORM)  
✅ CSRF protection  

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use HTTPS/SSL
- [ ] Set up proper CORS origins
- [ ] Implement rate limiting
- [ ] Enable security middleware
- [ ] Use environment variables for secrets

---

## Deployment Notes

### Before Deploying

1. Update `settings.py` for production
2. Set up PostgreSQL database
3. Configure static/media file storage
4. Set up email backend
5. Configure logging
6. Set up monitoring
7. Create backup strategy

### Production Settings

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '5432',
    }
}
```

---

## Dependencies

### Core Dependencies
- Django 4.2+
- djangorestframework 3.14+
- djangorestframework-simplejwt 5.3+
- django-cors-headers 4.3+
- django-countries 7.5+
- Pillow 10.1+

### Development Dependencies (add to requirements-dev.txt)
- pytest-django
- black (code formatter)
- flake8 (linting)
- coverage (test coverage)

---

## Resources

### Documentation
- **Django**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **SimpleJWT**: https://django-rest-framework-simplejwt.readthedocs.io/

### Project Documentation
- `docs/setup-guide.md` - Detailed setup instructions
- `docs/api-reference.md` - Complete API documentation
- `docs/implementation-checklist.md` - Development checklist

---

## Support

For questions or issues:
1. Check this README
2. Check documentation in `docs/` folder
3. Review code comments in source files
4. Open an issue on GitHub

---

## License


---

**Last Updated**: December 2025  
**Django Version**: 4.2+  
**Python Version**: 3.8+
