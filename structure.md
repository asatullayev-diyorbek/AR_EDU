# Backend Structure

Bu hujjat `backend` ilovasi uchun toʻliq tuzilma va API maʼlumotlarini tavsiflaydi.

## Umumiy overview

- Platforma: Django 5 + Django REST Framework
- Maʼlumotlar bazasi: SQLite (dev), PostgreSQL (prod)
- Administrator interfeysi: `django-unfold`
- REST javob formati: `code`, `message`, `data`
- `backend` ichida asosiy ilovalar:
  - `core`
  - `devices`
  - `education`
  - `config`

## Fayl strukturasining asosiy qismlari

```
backend/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── exceptions.py
│   ├── pagination.py
│   └── utils/response.py
├── devices/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── education/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── requirements.txt
└── structure.md
```

## Konfiguratsiya

### `config/settings/base.py`

- `INSTALLED_APPS`:
  - `unfold`, `unfold.contrib.filters`, `unfold.contrib.forms`
  - default Django ilovalari
  - `rest_framework`, `corsheaders`, `django_filters`
  - lokal ilovalar: `core`, `devices`, `education`
- `MIDDLEWARE`:
  - `SecurityMiddleware`
  - `CorsMiddleware`
  - `SessionMiddleware`, `CommonMiddleware`, `CsrfViewMiddleware`, `AuthenticationMiddleware`, `MessageMiddleware`, `XFrameOptionsMiddleware`
- `REST_FRAMEWORK`:
  - `DEFAULT_PAGINATION_CLASS`: `core.pagination.StandardResultsPagination`
  - `PAGE_SIZE`: 20
  - filter backendlar: `DjangoFilterBackend`, `SearchFilter`, `OrderingFilter`
  - renderer: faqat `JSONRenderer` (devda `BrowsableAPIRenderer` ham qoʻshiladi)
  - parserlar: `JSONParser`, `MultiPartParser`, `FormParser`
  - `EXCEPTION_HANDLER`: `core.exceptions.custom_exception_handler`
- `CORS`:
  - devda barcha originlar ruxsat etilgan
  - asosiy `base.py`da `CORS_ALLOWED_ORIGINS` roʻyxati
- `STATIC_ROOT`, `MEDIA_ROOT`, `STATIC_URL`, `MEDIA_URL`

### `config/settings/dev.py`

- `DEBUG = True`
- SQLite (`db.sqlite3`)
- `CORS_ALLOW_ALL_ORIGINS = True`
- Browsable API yoqilgan

### `config/settings/prod.py`

- `DEBUG = False`
- PostgreSQL konfiguratsiyasi
- xavfsizlik parametrlar: `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_HSTS_*`, `X_FRAME_OPTIONS = 'DENY'`
- `STATICFILES_STORAGE` manifest saqlash uchun

### `config/urls.py`

- `/admin/`
- `/api/` ostida `devices.urls` va `education.urls`
- media fayllarini devda `static()` orqali xizmat qilish

## `core` ilovasi

### `core.exceptions.custom_exception_handler`

- DRF standart exception handlerini chaqiradi
- agar DRF javob qaytarilsa, uni:
  - `code`: HTTP status kodi
  - `message`: xabarning birinchi qismi
  - `data`: bo‘sh obyektdan iborat
- agar unhandled exception bo‘lsa, 500 javob yuboradi

### `core.pagination.StandardResultsPagination`

- sahifalashni qoplaydi
- natija strukturasini quyidagicha qaytaradi:
  - `code`: 200
  - `message`: `Success`
  - `data`: `count`, `next`, `previous`, `results`

### `core.utils.response`

- `success_response(data, message, code)`
- `error_response(message, code, data)`
- `paginated_response(...)` (kirgan paginatsiya uchun standard envelope)

## `devices` ilovasi

### Modellar (`devices/models.py`)

#### `Category`
- `name` — `CharField(max_length=120, unique=True)`
- `ordering = ['name']`

#### `Device`
- `category` — `ForeignKey(Category, on_delete=SET_NULL, null=True, blank=True, related_name='devices')`
- `topic` — `ForeignKey('education.Topic', on_delete=SET_NULL, null=True, blank=True, related_name='devices')`
- `name` — `CharField(max_length=200)`
- `short_desc` — `CharField(max_length=300, blank=True)`
- `description` — `TextField(blank=True)`
- `image` — `ImageField(upload_to='devices/', blank=True, null=True)`
- `model_file` — `FileField(upload_to='devices/models/', blank=True, null=True)`
- `created_at`, `updated_at`
- `ordering = ['-created_at']`

#### `Node`
- `device` — `ForeignKey(Device, on_delete=CASCADE, related_name='nodes')`
- `name` — `CharField(max_length=200)`
- `description` — `TextField(blank=True)`
- `icon` — `ImageField(upload_to='nodes/icons/', blank=True, null=True)`
- `created_at`
- `ordering = ['name']`

### Serializerlar (`devices/serializers.py`)

#### `CategorySerializer`
- `id`, `name`

#### `TopicRefSerializer`
- `id`, `title`

#### `NodeSerializer`
- `id`, `name`, `description`, `icon`, `created_at`

#### `DeviceListSerializer`
- `category`, `topic`, `name`, `short_desc`, `image`, `created_at`

#### `DeviceDetailSerializer`
- `category`, `topic`, `name`, `short_desc`, `description`, `image`, `model_file`, `nodes`, `created_at`, `updated_at`

### Viewlar (`devices/views.py`)

#### `CategoryViewSet`
- `GET /api/categories/`
- `GET /api/categories/{id}/`
- `search`: `name`
- `ordering`: `name`

#### `DeviceViewSet`
- `GET /api/devices/`
- `GET /api/devices/{id}/`
- filtrlash: `category`, `topic`
- qidiruv: `name`, `short_desc`, `description`, `topic__title`
- ordering: `name`, `created_at`
- detailda `DeviceDetailSerializer` orqali nested `nodes`

#### `NodeViewSet`
- `GET /api/nodes/`
- `GET /api/nodes/{id}/`
- filtrlash: `device`
- qidiruv: `name`, `description`
- ordering: `name`, `created_at`

### URL marshrutlari (`devices/urls.py`)

- `/api/categories/`
- `/api/categories/{id}/`
- `/api/devices/`
- `/api/devices/{id}/`
- `/api/nodes/`
- `/api/nodes/{id}/`

## Auth endpoints

- `/api/auth/register/` — POST: register new user and return token
- `/api/auth/login/` — POST: login existing user and return token

## `education` ilovasi

### Modellar (`education/models.py`)

#### `Course`
- `title` — `CharField(max_length=255)`
- `slug` — `SlugField(max_length=255, unique=True, blank=True)`
- `description` — `TextField(blank=True)`
- `image` — `ImageField(upload_to='education/courses/', blank=True, null=True)`
- `published` — `BooleanField(default=True)`
- `created_at`, `updated_at`
- `save()` metodi slug generatsiyasi uchun

#### `Topic`
- `course` — `ForeignKey(Course, on_delete=CASCADE, related_name='topics')`
- `title` — `CharField(max_length=255)`
- `summary` — `TextField(blank=True)`
- `order` — `PositiveIntegerField(default=0)`
- `created_at`, `updated_at`
- `ordering = ['order', 'title']`

#### `Resource`
- `topic` — `ForeignKey(Topic, on_delete=CASCADE, related_name='resources')`
- `title`, `description`
- `resource_type` — `CharField(choices=[text, image, video, file, link], default='text')`
- `content` — `TextField(blank=True)`
- `image` — `ImageField(upload_to='education/resources/images/', blank=True, null=True)`
- `video_url`, `url` — `URLField`
- `file` — `FileField(upload_to='education/resources/files/', blank=True, null=True)`
- `created_at`, `updated_at`

#### `ResourceNode`
- `resource` — `ForeignKey(Resource, on_delete=CASCADE, related_name='nodes')`
- `name` — `CharField(max_length=255)`
- `description` — `TextField(blank=True)`
- `order` — `PositiveIntegerField(default=0)`
- `created_at`
- `ordering = ['resource', 'order', 'name']`

#### `Quiz`
- `topic` — `ForeignKey(Topic, on_delete=CASCADE, related_name='quizzes')`
- `question` — `CharField(max_length=500)`
- `option_a`, `option_b`, `option_c`, `option_d`
- `correct` — `CharField(max_length=1, choices=[a,b,c,d])`
- `explanation` — `TextField(blank=True)`
- `created_at`

### Serializerlar (`education/serializers.py`)

#### `ResourceNodeSerializer`
- `id`, `name`, `description`, `order`, `created_at`

#### `ResourceSerializer`
- `id`, `title`, `description`, `resource_type`, `content`, `image`, `video_url`, `url`, `file`, `nodes`, `created_at`, `updated_at`

#### `QuizSerializer`
- `id`, `topic`, `question`, `option_a`, `option_b`, `option_c`, `option_d`, `correct`, `explanation`, `created_at`

#### `TopicReferenceSerializer`
- `id`, `title`, `summary`, `order`

#### `TopicDetailSerializer`
- `id`, `title`, `summary`, `order`, `resources`, `quizzes`, `created_at`, `updated_at`

#### `CourseListSerializer`
- `id`, `title`, `slug`, `description`, `image`, `published`, `created_at`, `updated_at`

#### `CourseDetailSerializer`
- `id`, `title`, `slug`, `description`, `image`, `published`, `topics`, `created_at`, `updated_at`

#### `TopicSerializer`
- `id`, `course`, `title`, `summary`, `order`, `created_at`, `updated_at`

### Viewlar (`education/views.py`)

#### `BaseReadOnlyViewSet`
- umumiy `list()` va `retrieve()` logikasi
- `filter_backends`: `DjangoFilterBackend`, `SearchFilter`, `OrderingFilter`

#### `CourseViewSet`
- `GET /api/courses/`
- `GET /api/courses/{id}/`
- filtrlar: `published`
- qidiruv: `title`, `description`
- ordering: `title`, `created_at`
- `retrieve` holatida `CourseDetailSerializer`

#### `TopicViewSet`
- `GET /api/topics/`
- `GET /api/topics/{id}/`
- filtrlar: `course`
- qidiruv: `title`, `summary`
- ordering: `order`, `created_at`
- `retrieve` holatida `TopicDetailSerializer`

#### `ResourceViewSet`
- `GET /api/resources/`
- `GET /api/resources/{id}/`
- filtrlar: `topic`, `resource_type`
- qidiruv: `title`, `description`
- ordering: `title`, `created_at`

#### `ResourceNodeViewSet`
- `GET /api/resource-nodes/`
- `GET /api/resource-nodes/{id}/`
- filtrlar: `resource`, `resource__topic`
- qidiruv: `name`, `description`
- ordering: `order`, `name`, `created_at`

#### `QuizViewSet`
- `GET /api/quiz/`
- `GET /api/quiz/{id}/`
- filtrlar: `topic`
- qidiruv: `question`
- ordering: `id`, `created_at`

### URL marshrutlari (`education/urls.py`)

- `/api/courses/`
- `/api/courses/{id}/`
- `/api/topics/`
- `/api/topics/{id}/`
- `/api/resources/`
- `/api/resources/{id}/`
- `/api/resource-nodes/`
- `/api/resource-nodes/{id}/`
- `/api/quiz/`
- `/api/quiz/{id}/`

## Admin konfiguratsiyalari

### `devices/admin.py`
- `CategoryAdmin`, `DeviceAdmin`, `NodeAdmin`
- `Device` adminida `topic` va `model_file` qo‘shilgan
- `Node` adminida `device` uchun `autocomplete_fields`

### `education/admin.py`
- `CourseAdmin` bilan `TopicInline`
- `TopicAdmin` bilan `ResourceInline`, `QuizInline`
- `ResourceAdmin` bilan `ResourceNodeInline`
- `QuizAdmin` standart quiz yaratish formasi

## JSON API javob namunasi

### Standart muvaffaqiyat javobi

```json
{
  "code": 200,
  "message": "Success",
  "data": {...}
}
```

### Paginatsiyali javob

```json
{
  "code": 200,
  "message": "Success",
  "data": {
    "count": 123,
    "next": "...",
    "previous": null,
    "results": [ ... ]
  }
}
```

### `Device` detail namunasi

```json
{
  "code": 200,
  "message": "Device fetched successfully",
  "data": {
    "id": 1,
    "category": {"id": 1, "name": "Sensors"},
    "topic": {"id": 2, "title": "Intro to sensors"},
    "name": "Smart Temperature Sensor",
    "short_desc": "High-precision ambient sensor",
    "description": "Measures temperature and humidity...",
    "image": "/media/devices/sensor.png",
    "model_file": null,
    "nodes": [
      {"id": 1, "name": "Temperature Node", "description": "Measures ambient temperature", "icon": null, "created_at": "2024-01-15T10:00:00Z"}
    ],
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z"
  }
}
```

### `Topic` detail namunasi

```json
{
  "code": 200,
  "message": "Topic fetched successfully",
  "data": {
    "id": 2,
    "title": "Circuit Basics",
    "summary": "Elementary circuits and components",
    "order": 1,
    "resources": [
      {
        "id": 5,
        "title": "Resistor Guide",
        "description": "How resistors work",
        "resource_type": "text",
        "content": "Resistor basics...",
        "image": null,
        "video_url": null,
        "url": null,
        "file": null,
        "nodes": [],
        "created_at": "2024-01-15T10:00:00Z",
        "updated_at": "2024-01-15T10:00:00Z"
      }
    ],
    "quizzes": [
      {
        "id": 1,
        "topic": 2,
        "question": "What is resistance?",
        "option_a": "Voltage",
        "option_b": "Current",
        "option_c": "Opposition to current",
        "option_d": "Power",
        "correct": "c",
        "explanation": "Resistance opposes current flow.",
        "created_at": "2024-01-15T10:00:00Z"
      }
    ],
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z"
  }
}
```

## Yakuniy eslatmalar

- API hamma list va detail endpointlar `code/message/data` formatida qaytaradi.
- `education` bilan `devices` orasida `Topic` orqali bogʻlanish imkoniyati qoʻshilgan.
