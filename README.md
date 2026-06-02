# Expense Tracker

This was a personal side project built during the first year of a Bachelor of Engineering in Computer Science at Jyothy Institute of Technology, VTU, Bangalore. It started as a way to track daily spending and grew into a small but complete web app.

## Features

- Add and delete expenses by category
- Monthly budget tracking with a visual progress bar (green under 80%, amber at 80-99%, red when over budget)
- Category and monthly spending reports
- Category filter on the home page
- Input validation on all form submissions

## Tech Stack

| Technology | Purpose |
| --- | --- |
| Python | Language |
| Flask | Web framework |
| SQLAlchemy | ORM and database access |
| SQLite | Database |
| pandas | Report aggregation |
| Bootstrap 5 | Frontend styling |

## Setup

```bash
git clone https://github.com/achalnm/Expense-Tracker-Using-Flask-and-SQLAlchemy.git
cd Expense-Tracker-Using-Flask-and-SQLAlchemy
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt
flask run
```

Open `http://127.0.0.1:5000` in your browser. The database is created automatically on first run.

## Running Tests

```bash
python tests.py
```

## Project Notes

This was originally a quick personal tool for tracking daily expenses. It was later cleaned up with proper input validation, budget tracking, a reporting page, and tests as a learning exercise in Flask and SQLAlchemy.
