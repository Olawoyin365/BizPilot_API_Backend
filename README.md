# 🚀 BizPilot - Multi-Tenant Business Management Platform

<div align="center">

[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![DRF](https://img.shields.io/badge/DRF-3.14+-red.svg)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Empowering Small and Medium Businesses with Modern Digital Solutions**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [API Reference](#-api-endpoints) • [Contributing](#-contributing)

</div>

---

## 📖 Table of Contents

- [About The Project](#-about-the-project)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Architecture](#-architecture)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Initial Setup](#initial-setup)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Multi-Tenancy](#-multi-tenancy-explained)
- [Industry Modules](#-industry-modules)
- [Usage Examples](#-usage-examples)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact & Support](#-contact--support)

---

## 🎯 About The Project

**BizPilot** is a comprehensive multi-tenant SaaS platform designed specifically for small and medium-sized businesses in emerging markets. Think of it as "Salesforce for SMBs" - providing enterprise-grade business management tools at an accessible scale.

### The Problem We're Solving

Many small businesses still rely on:
- 📓 Paper notebooks for customer records
- 📱 WhatsApp for order management
- 🧮 Manual Excel sheets for inventory
- 🤔 Memory-based task tracking

This leads to:
- Lost customer information
- Missed orders and deadlines
- Inventory discrepancies
- Poor business insights
- Difficulty scaling operations

### Our Solution

BizPilot provides industry-specific digital solutions that are:
- ✅ **Easy to Use** - Designed for non-technical users
- ✅ **Affordable** - Built for SMB budgets
- ✅ **Offline-First** - Works with unreliable internet
- ✅ **Mobile-Ready** - API-first architecture
- ✅ **Scalable** - Grows with your business

---

## ✨ Key Features

### 🏢 Multi-Tenancy
- **Complete Data Isolation** - Each business's data is 100% separate
- **Automatic Business Scoping** - All queries filtered by business
- **Secure by Design** - Business A cannot access Business B's data
- **Scalable Architecture** - Support thousands of businesses on one platform

### 🔐 Authentication & Security
- **JWT Authentication** - Secure token-based auth
- **Email-Based Login** - User-friendly authentication
- **Role-Based Access** - Business owners vs staff members
- **Password Security** - Django's robust password hashing

### 🏭 Industry-Specific Modules

#### 1. **Retail & E-Commerce** 🛍️
- Product catalog management
- Category organization
- Real-time inventory tracking
- Stock alerts (low stock, out of stock)
- Complete inventory history
- Automatic stock updates on sales
- Price management
- SKU tracking

#### 2. **Tailoring & Fashion** ✂️
- Customer measurement storage
- Multiple garment types support
- Task/order management
- Due date tracking
- Status workflow (Not Started → In Progress → Fitting → Completed → Delivered)
- Overdue alerts
- Payment tracking

#### 3. **Education** 📚 *(Coming Soon)*
- Student management
- Course scheduling
- Attendance tracking
- Grade management

### 👥 Customer Management
- Centralized customer database
- Shared across all industry modules
- Contact information (name, phone, email, address)
- Customer history tracking
- Quick phone number search
- Notes and preferences

### 📊 API Features
- **RESTful Design** - Standard HTTP methods
- **Pagination** - Efficient data loading (20 items/page)
- **Search & Filtering** - Find what you need quickly
- **Ordering** - Sort by any field
- **Comprehensive Responses** - All data you need in one request

---

## 🛠 Technology Stack

### Backend
- **[Django 4.2+](https://www.djangoproject.com/)** - High-level Python web framework
- **[Django REST Framework](https://www.django-rest-framework.org/)** - Powerful API toolkit
- **[SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/)** - JWT authentication
- **[Python 3.8+](https://www.python.org/)** - Programming language

### Database
- **SQLite** - Development (included)
- **PostgreSQL** - Production (recommended)

### Additional Libraries
- **django-cors-headers** - CORS support
- **django-countries** - Country field support
- **Pillow** - Image processing

### Frontend (Planned)
- React / Vue.js / React Native

---

## 🏗 Architecture

### Multi-Tenancy Pattern

```
┌─────────────────────────────────────────────────────────┐
│                    BizPilot Platform                    │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐  ┌───────▼────────┐  ┌──────▼─────────┐
│   Business A   │  │   Business B   │  │   Business C   │
│   (Retail)     │  │   (Tailoring)  │  │   (Education)  │
└────────────────┘  └────────────────┘  └────────────────┘
        │                   │                   │
    ┌───┴───┐           ┌───┴───┐           ┌───┴───┐
    │Customers│         │Customers│         │Customers│
    │Products │         │Measurements│      │Students │
    │Inventory│         │Tasks    │         │Courses  │
    └─────────┘         └─────────┘         └─────────┘

Each business is completely isolated - no data sharing
```

### Request Flow

```
1. User Login
   ↓
2. JWT Token Generated
   ↓
3. API Request with Token
   ↓
4. Token Validation
   ↓
5. Extract User's Business
   ↓
6. Auto-Filter Query by Business
   ↓
7. Return Business-Scoped Data
```

### Core Components

1. **Core App** - Shared utilities
   - `BusinessQuerySetMixin` - Auto-filters by business
   - `BusinessCreateMixin` - Auto-assigns business on create
   - Permission classes

2. **Account App** - Authentication
   - Business registration
   - User management
   - JWT tokens

3. **Industry App** - Business types
   - Industry definitions
   - Category templates (optional)

4. **Customer App** - Shared customers
   - Cross-industry customer records

5. **Industry-Specific Apps**
   - Retail, Tailoring, Education (future)

---

## 🚀 Getting Started

### Prerequisites

```bash
# Python 3.8 or higher
python --version

# pip (Python package manager)
pip --version

# Git (for cloning)
git --version
```

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/bizpilot.git
cd bizpilot
```

#### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Environment Configuration

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

# For production PostgreSQL:
# DATABASE_URL=postgres://user:password@localhost:5432/bizpilot
```

#### 5. Database Setup

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
```

#### 6. Create Initial Data

```bash
# Start the server
python manage.py runserver

# Open browser to http://127.0.0.1:8000/admin/
# Login with superuser credentials
# Create industries: Retail, Tailoring, Education
```

#### 7. Test the API

```bash
# Server should be running at
http://127.0.0.1:8000/

# API endpoints available at
http://127.0.0.1:8000/api/

# Admin panel at
http://127.0.0.1:8000/admin/
```

---

## 📁 Project Structure

```
bizpilot/
│
├── BizPilot/                      # Main project configuration
│   ├── __init__.py
│   ├── settings.py               # Django settings
│   ├── urls.py                   # Main URL routing
│   ├── wsgi.py                   # WSGI config
│   └── asgi.py                   # ASGI config
│
├── apps/                         # All Django apps
│   │
│   ├── core/                     # Shared utilities
│   │   ├── mixins.py            # Business-scoped mixins
│   │   ├── permissions.py       # Custom permissions
│   │   └── apps.py
│   │
│   ├── account/                  # Authentication & Business
│   │   ├── models.py            # Business, CustomUser
│   │   ├── serializers.py       # Auth serializers
│   │   ├── views.py             # Auth endpoints
│   │   ├── urls.py              # Auth routes
│   │   ├── admin.py             # Admin config
│   │   └── apps.py
│   │
│   ├── industry/                 # Industry types
│   │   ├── models.py            # Industry, CategoryTemplate
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── apps.py
│   │
│   ├── customer/                 # Customer management
│   │   ├── models.py            # Customer
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── apps.py
│   │
│   ├── retail/                   # Retail features
│   │   ├── models.py            # Category, Product, InventoryHistory
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── apps.py
│   │
│   └── tailoring/                # Tailoring features
│       ├── models.py            # Measurement, Task
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       ├── admin.py
│       └── apps.py
│
├── media/                        # User uploads
├── static/                       # Static files
├── db.sqlite3                    # Development database
├── manage.py                     # Django management
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 🔌 API Endpoints

### Base URL: `http://127.0.0.1:8000/api/`

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/account/register/` | Register new business | ❌ |
| POST | `/account/login/` | User login | ❌ |
| POST | `/token/refresh/` | Refresh access token | ❌ |
| GET | `/account/profile/` | Get user profile | ✅ |
| GET | `/account/business/` | Get business details | ✅ |

### Industries

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/industries/` | List all industries | ❌ |
| GET | `/industries/{id}/` | Get industry details | ❌ |

### Customers

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/customers/` | List customers | ✅ |
| POST | `/customers/` | Create customer | ✅ |
| GET | `/customers/{id}/` | Get customer details | ✅ |
| PUT/PATCH | `/customers/{id}/` | Update customer | ✅ |
| DELETE | `/customers/{id}/` | Delete customer | ✅ |
| GET | `/customers/search_by_phone/?phone=XXX` | Quick phone search | ✅ |

### Retail

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/retail/categories/` | List categories | ✅ |
| POST | `/retail/categories/` | Create category | ✅ |
| GET | `/retail/products/` | List products | ✅ |
| POST | `/retail/products/` | Create product | ✅ |
| GET | `/retail/products/low_stock/` | Low stock products | ✅ |
| GET | `/retail/products/out_of_stock/` | Out of stock products | ✅ |
| POST | `/retail/products/{id}/update_inventory/` | Update stock | ✅ |
| GET | `/retail/inventory-history/` | View inventory changes | ✅ |

### Tailoring

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/tailoring/measurements/` | List measurements | ✅ |
| POST | `/tailoring/measurements/` | Create measurement | ✅ |
| GET | `/tailoring/measurements/by_customer/{id}/` | Customer measurements | ✅ |
| GET | `/tailoring/tasks/` | List tasks | ✅ |
| POST | `/tailoring/tasks/` | Create task | ✅ |
| GET | `/tailoring/tasks/today/` | Today's tasks | ✅ |
| GET | `/tailoring/tasks/overdue/` | Overdue tasks | ✅ |
| GET | `/tailoring/tasks/upcoming/` | Upcoming tasks | ✅ |
| POST | `/tailoring/tasks/{id}/update_status/` | Update task status | ✅ |

---

## 🔒 Multi-Tenancy Explained

### How It Works

Every piece of data in BizPilot belongs to a **Business**. The system automatically ensures businesses can only see their own data.

### Implementation

#### 1. Database Level
```python
# Every model has a business foreign key
class Customer(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    # ...
```

#### 2. Automatic Filtering
```python
# BusinessQuerySetMixin automatically filters
class CustomerViewSet(BusinessQuerySetMixin, viewsets.ModelViewSet):
    queryset = Customer.objects.all()  # Will be filtered by business
```

#### 3. Automatic Assignment
```python
# BusinessCreateMixin automatically sets business
class CustomerViewSet(BusinessCreateMixin, viewsets.ModelViewSet):
    # When creating customer, business is auto-assigned
```

### Security Guarantees

✅ **Business A** cannot see **Business B**'s customers  
✅ **Business A** cannot modify **Business B**'s products  
✅ **Business A** cannot access **Business B**'s measurements  
✅ All queries automatically scoped to authenticated user's business  
✅ Validation prevents cross-business references  

---

## 🏭 Industry Modules

### Retail Module Features

**Perfect for:**
- Stores
- Supermarkets
- Pharmacies
- Electronics shops
- Fashion retailers

**Capabilities:**
- Product catalog with categories
- Real-time inventory tracking
- Stock alerts (low/out of stock)
- Complete inventory audit trail
- Price management
- SKU tracking
- Search by name/SKU/category

### Tailoring Module Features

**Perfect for:**
- Tailors
- Fashion designers
- Alteration services
- Custom clothing makers

**Capabilities:**
- Customer measurement storage
- Multiple garment types
- Task/order management
- Due date tracking
- Status workflow
- Overdue alerts
- Payment tracking
- Quick customer lookup

---

## 💡 Usage Examples

### Example 1: Register a Business

```bash
POST /api/account/register/
Content-Type: application/json

{
    "store_name": "Fashion Hub",
    "email": "owner@fashionhub.com",
    "phone": "+1234567890",
    "country": "US",
    "industry": 2,
    "username": "fashionhub_owner",
    "password": "SecurePass123!",
    "password2": "SecurePass123!"
}
```

**Response:**
```json
{
    "message": "Business registered successfully",
    "business": { /* business details */ },
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    },
    "user": { /* user details */ }
}
```

### Example 2: Create a Customer

```bash
POST /api/customers/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "name": "John Doe",
    "phone": "+1987654321",
    "email": "john@example.com",
    "address": "123 Main St, City"
}
```

### Example 3: Add Product to Inventory

```bash
POST /api/retail/products/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "category": 1,
    "name": "Blue T-Shirt",
    "description": "100% cotton",
    "price": "19.99",
    "stock_quantity": 50,
    "low_stock_threshold": 10,
    "sku": "TSHIRT-BLUE-001"
}
```

### Example 4: Store Customer Measurements

```bash
POST /api/tailoring/measurements/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "customer": 1,
    "garment_type": "MENS_SHIRT",
    "chest": "40.5",
    "waist": "34.0",
    "shoulder": "17.5",
    "sleeve_length": "24.0",
    "date_taken": "2024-12-19",
    "notes": "Prefers slim fit"
}
```

---

## 🧪 Testing

### Run System Check

```bash
python manage.py check
```

### Create Test Data

```bash
# Using Django shell
python manage.py shell

>>> from apps.industry.models import Industry
>>> Industry.objects.create(name="Retail", description="Retail businesses")
>>> Industry.objects.create(name="Tailoring", description="Tailoring services")
```

### Manual API Testing

Use tools like:
- **Postman** - https://www.postman.com/
- **Insomnia** - https://insomnia.rest/
- **cURL** - Command line
- **httpie** - Command line

### Unit Tests (Coming Soon)

```bash
python manage.py test
```

---

## 🚢 Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in settings
- [ ] Configure PostgreSQL database
- [ ] Set up proper `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up static file serving (WhiteNoise or CDN)
- [ ] Configure media file storage (S3 or similar)
- [ ] Set up HTTPS/SSL
- [ ] Configure email backend
- [ ] Set up monitoring (Sentry, etc.)
- [ ] Configure CORS for production domains
- [ ] Set up backup strategy

### Deployment Platforms

**Recommended:**
- **Heroku** - Easy deployment
- **DigitalOcean App Platform** - Simple and affordable
- **Railway** - Modern platform
- **AWS Elastic Beanstalk** - Scalable
- **Google Cloud Run** - Containerized

### Docker Deployment (Coming Soon)

```bash
docker build -t bizpilot .
docker run -p 8000:8000 bizpilot
```

---

## 🗺 Roadmap

### Version 1.0 (Current)
- ✅ Multi-tenant architecture
- ✅ JWT authentication
- ✅ Retail module
- ✅ Tailoring module
- ✅ Customer management

### Version 1.1 (Q1 2025)
- [ ] Education module
- [ ] Email notifications
- [ ] Category templates per industry
- [ ] Advanced search filters
- [ ] Export data (CSV/Excel)

### Version 2.0 (Q2 2025)
- [ ] Dashboard with analytics
- [ ] Reporting system
- [ ] Payment integration (Stripe/PayPal)
- [ ] SMS notifications
- [ ] Multi-language support
- [ ] Mobile app (React Native)

### Version 3.0 (Q3 2025)
- [ ] Customer portal
- [ ] Online ordering
- [ ] Appointment scheduling
- [ ] Advanced role management
- [ ] WhatsApp integration
- [ ] Invoice generation

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute

1. **Report Bugs** - Open an issue
2. **Suggest Features** - Start a discussion
3. **Submit Pull Requests** - Fix bugs or add features
4. **Improve Documentation** - Help others understand
5. **Write Tests** - Increase code coverage

### Development Process

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Add docstrings to all functions/classes
- Write meaningful commit messages
- Add tests for new features
- Update documentation

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Contact & Support

### Project Maintainer
- **Name:** [Your Name]
- **Email:** your.email@example.com
- **GitHub:** [@yourusername](https://github.com/yourusername)

### Get Help
- 📧 **Email Support:** support@bizpilot.com
- 💬 **Community Forum:** [Coming Soon]
- 🐛 **Bug Reports:** [GitHub Issues](https://github.com/yourusername/bizpilot/issues)
- 💡 **Feature Requests:** [GitHub Discussions](https://github.com/yourusername/bizpilot/discussions)

### Links
- **Documentation:** [Full Docs](docs/)
- **API Reference:** [API Docs](docs/api-reference.md)
- **Website:** https://bizpilot.com (Coming Soon)

---

## 🙏 Acknowledgments

- Django and Django REST Framework teams
- All open-source contributors
- Beta testers and early adopters
- Small business owners who inspired this project

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/bizpilot?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/bizpilot?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/bizpilot)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/bizpilot)

---

<div align="center">

**Made with ❤️ for Small Businesses Everywhere**

⭐ Star us on GitHub — it helps!

[Report Bug](https://github.com/yourusername/bizpilot/issues) • [Request Feature](https://github.com/yourusername/bizpilot/issues)

</div>
