# Web-Data-and-Services-Football-API

## Overview

This project is a RESTful API built using Django and Django REST Framework.  
The API provides access to football data including teams, matches, players, and player statistics.

The system imports data from CSV files and exposes it through API endpoints that return JSON responses.  
A simple frontend interface is also included to demonstrate interaction with the API.

---

## Features

- REST API for football data
- Data import from CSV datasets
- Endpoints for Teams, Matches, Players and Stats
- Filtering support for queries
- Pagination for large datasets
- Django Admin interface for database management
- Simple frontend interface for interacting with the API

---

## Technologies Used

- Python
- Django
- Django REST Framework
- SQLite (default Django database)
- JavaScript (for frontend interaction)
- HTML

---

## Project Structure
football_api/
│
├── football_api/ # Django project configuration
│
├── api/ # Main application
│ ├── models.py
│ ├── views.py
│ ├── serializers.py
│ ├── import_data.py
│ ├── urls.py
│ ├── admin.py
│ └── data/ # CSV datasets
│
├── manage.py
└── README.md

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

Example endpoints:
/api/teams/
/api/matches/
/api/players/
/api/stats/


Example queries:

/api/matches/?team=Arsenal
/api/players/?team_id=3

Responses are returned in JSON format.

## Example Response


{
"id": 1,
"name": "Arsenal",
"league": "Premier League",
"country": "England"
}


---

## Future Improvements

Possible improvements include:

- Advanced filtering options
- Authentication for API access
- Expanded datasets
- Interactive frontend dashboard
- Data visualisation for player statistics

---

## Author

Jack Hillyer

University coursework project for Web Data and Services.
