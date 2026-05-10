# Smart MR Backend

Production-ready Django REST API for the Smart Home AR/3D learning app.

## Tech Stack

- **Django 5** + **Django REST Framework**
- **SQLite** (dev) / **PostgreSQL** (prod)
- **django-unfold** — modern admin UI
- **django-cors-headers** — CORS support
- **django-filter** — query filtering
- **python-decouple** — environment config

---

## Project Structure

```
smart_mr_backend/
├── config/
│   ├── settings/
│   │   ├── base.py      # shared settings
│   │   ├── dev.py       # SQLite, DEBUG=True, BrowsableAPI
│   │   └── prod.py      # PostgreSQL, DEBUG=False, security headers
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── exceptions.py    # global DRF exception handler
│   ├── pagination.py    # standard paginated envelope
│   └── utils/
│       └── response.py  # success_response / error_response helpers
├── devices/
│   ├── models.py        # Category, Device, Node
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── education/
│   ├── models.py        # Course, Topic, Resource, Quiz
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── manage.py
├── requirements.txt
└── .env
```

---

## Quick Start

```bash
# 1. Create and activate virtualenv
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy and edit env file
cp .env .env.local
# Edit .env — set SECRET_KEY at minimum

# 4. Run migrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Run dev server
python manage.py runserver
```

---

## API Endpoints

All responses follow the standard envelope:

```json
{
  "code": 200,
  "message": "Success",
  "data": { ... }
}
```

### Devices

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/devices/` | List all devices |
| GET | `/api/devices/{id}/` | Device detail with nested nodes |
| GET | `/api/categories/` | List all categories |
| GET | `/api/categories/{id}/` | Category detail |
| GET | `/api/nodes/` | List all nodes |
| GET | `/api/nodes/?device={id}` | Nodes filtered by device |

### Auth

| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/auth/register/` | Register a new user and return token |
| POST | `/api/auth/login/` | Login and return token |

### Education

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/courses/` | List all courses |
| GET | `/api/courses/{id}/` | Course detail with topics |
| GET | `/api/topics/` | List all topics |
| GET | `/api/topics/{id}/` | Topic detail with resources and quizzes |
| GET | `/api/resources/` | List all topic resources |
| GET | `/api/resource-nodes/` | List all resource nodes |
| GET | `/api/quiz/` | List all quiz questions |
| GET | `/api/quiz/{id}/` | Quiz detail |

### Query Parameters (all list endpoints)

| Param | Example | Description |
|-------|---------|-------------|
| `search` | `?search=sensor` | Full-text search |
| `ordering` | `?ordering=-created_at` | Field ordering |
| `page` | `?page=2` | Pagination |
| `page_size` | `?page_size=10` | Items per page (max 100) |
| `category` | `?category=1` | Filter devices by category |
| `device` | `?device=3` | Filter nodes by device |

---

## Example Response

```json
{
  "code": 200,
  "message": "Device fetched successfully",
  "data": {
    "id": 1,
    "category": { "id": 1, "name": "Sensors" },
    "name": "Smart Temperature Sensor",
    "short_desc": "High-precision ambient sensor",
    "description": "Measures temperature and humidity in real time...",
    "image": "/media/devices/sensor.png",
    "nodes": [
      {
        "id": 1,
        "name": "Temperature Node",
        "description": "Measures ambient temperature",
        "icon": null,
        "created_at": "2024-01-15T10:00:00Z"
      }
    ],
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z"
  }
}
```

---

## Admin Panel

Visit `/admin/` — powered by **django-unfold** with:
- Sidebar navigation per app
- Inline Node editing inside Device
- Search & filters on all models
- Purple branded theme

---

## Production Deployment

```bash
# Switch to prod settings
export DJANGO_SETTINGS_MODULE=config.settings.prod

# Set all required env vars (see .env for reference)
# DB_NAME, DB_USER, DB_PASSWORD, SECRET_KEY, ALLOWED_HOSTS ...

python manage.py collectstatic --no-input
python manage.py migrate
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```
