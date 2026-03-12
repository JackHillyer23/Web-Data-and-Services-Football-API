# Web-Data-and-Services-Football-API

## Overview

This project is a RESTful API built using Django and Django REST Framework.  
The API provides access to football data including teams, matches, players, and player statistics.

The system imports data from CSV files and exposes it through API endpoints that return JSON responses.  
A simple frontend interface is also included to demonstrate interaction with the API.

## Features

- REST API for football data
- Data import from CSV datasets
- Endpoints for Teams, Matches, Players and Stats
- Filtering support for queries
- Pagination for large datasets
- Django Admin interface for database management
- Simple frontend interface for interacting with the API

## Technologies Used

- Python
- Django
- Django REST Framework
- SQLite (default Django database)
- JavaScript (for frontend interaction)
- HTML

## Dataset

The project uses publicly available football datasets containing match results from the top European leagues.

Data includes:
- Teams
- Match results
- Player information
- Player statistics

CSV files are imported into the database using a custom Python script.

---

## Installation

Clone the repository:git clone https://github.com/JackHillyer23/Web-Data-and-Services-Football-API

Navigate to the project: cd Web-Data-and-Services-Football-API


Create and activate a virtual environment:
python -m venv venv
venv\Scripts\activate


Install dependencies: pip install -r requirements.txt


Apply migrations: python manage.py migrate

## Importing Data

The dataset is imported using a custom script:
python -m api.import_data
This reads the CSV files and populates the database.

## Running the API

Start the Django server: python manage.py runserver


The API will run at: http://127.0.0.1:8000/

## API Endpoints

GET /api/teams/  
POST /api/teams/  

GET /api/teams/{id}/  
PATCH /api/teams/{id}/  
DELETE /api/teams/{id}/  

Example filters:

/api/teams/?league=Premier League  
/api/teams/?country=Spain

All API endpoints support full CRUD functionality:

- Teams, Players, Matches, Stats can be **created, read, updated, deleted**.
- Filtering, search, and ordering supported on most endpoints.

---

## API Documentation

This project includes automatically generated API documentation via Swagger.
Football API Documentation.pdf

## Frontend Usage

The project includes a simple frontend interface for browsing football data:

- Open `frontend/index.html` in a browser.
- Features:
  - Collapsible sections for Teams, Players, Matches, Stats.
  - Live search for Teams and Players.
  - Styled tables with readable fields (e.g., team names, scores).

## Future Improvements

Possible improvements include:

- Advanced filtering options
- Authentication for API access
- Expanded datasets
- Data visualisation for player statistics

---

## Author

Jack Hillyer

University coursework project for Web Data and Services.
