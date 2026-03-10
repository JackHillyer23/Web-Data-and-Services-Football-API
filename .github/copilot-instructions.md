# AI Agent Instructions for Football Analytics API

## Project Overview

This is a Django REST Framework API for football analytics, featuring teams, players, matches, and player performance statistics. It uses DRF's ViewSet/Router pattern for automatic CRUD endpoints and drf-yasg for API documentation (Swagger/ReDoc).

## Architecture & Data Model

**Core Components:**
- `api/models.py`: Four interconnected models using Django ORM:
  - `Team` (name, league, country) - root entity
  - `Player` (ForeignKey to Team) - team roster
  - `Match` (home_team, away_team ForeignKeys with related_names for reverse queries)
  - `PlayerMatchStats` (ForeignKey to both Player and Match) - performance metrics per match

**Design Pattern:**
All views (`api/views.py`) use `ModelViewSet` which auto-generates GET/POST/PUT/DELETE/PATCH endpoints. Serializers are simple `ModelSerializer` using `fields = '__all__'`.

**URL Routing:**
- `api/urls.py`: Uses `DefaultRouter` to register ViewSets → auto-generates `/api/{teams,players,matches,stats}/` endpoints
- `football_api/urls.py`: Main config includes admin, api routes, and Swagger/ReDoc documentation at `/swagger/` and `/redoc/`

## Development Workflows

**Start the server:**
```bash
cd football_api
python manage.py runserver
```

**Database migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Access API:**
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
- Admin: http://localhost:8000/admin/

**Testing:** Currently empty tests file. Use Django's TestCase or DRF's APITestCase for endpoint testing.

## Key Patterns & Conventions

1. **Serializer Pattern:** All serializers use `fields = '__all__'` - when extending functionality, explicitly list fields instead to maintain backward compatibility.

2. **Related Data:** Match model uses `related_name` attributes (`home_matches`, `away_matches`) for efficient reverse queries. Update serializers if you need nested data (e.g., team details within matches).

3. **ViewSet Permissions:** No custom permissions currently configured - all endpoints allow unauthenticated access. Add `permission_classes` to ViewSets if needed.

4. **Foreign Key Behavior:** Models use `on_delete=models.CASCADE` - deleting a team removes all associated players and their match statistics.

## Critical File Locations

- Models & business logic: `football_api/api/models.py`
- Endpoint handlers: `football_api/api/views.py`
- API schema: `football_api/api/serializers.py`
- Route registration: `football_api/api/urls.py` (app level) and `football_api/football_api/urls.py` (project level)
- Configuration: `football_api/football_api/settings.py` (includes REST_FRAMEWORK and INSTALLED_APPS)

## Common Tasks

**Add a new model:**
1. Define in `api/models.py`
2. Create `ModelSerializer` in `api/serializers.py`
3. Create `ViewSet` in `api/views.py`
4. Register in `api/urls.py` with `router.register()`
5. Run migrations

**Extend an endpoint:** ViewSets support custom actions via `@action()` decorator - document in docstrings for Swagger.

**Add validation:** Implement `validate_*` or `validate()` methods in serializers for field/object-level validation.

## Dependencies

- Django 5.2.12, djangorestframework 3.16.1 (REST API)
- drf-yasg 1.21.15 (Swagger/ReDoc documentation)
- SQLite default database
- pandas, numpy (data processing tools available)
