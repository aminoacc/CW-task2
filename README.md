# DTS114TC Software Component

## AI-Powered Meta-Software Development System

This project demonstrates an AI-powered system for meta-software development that automatically generates:
- Flask REST API
- Frontend HTML website with AI-generated image
- UML use case diagrams
- SDLC documentation (requirements, user stories, API endpoints)

---

## Project Structure

```
Task1/
├── notebook.ipynb          # Jupyter Notebook (AI-driven code generation)
├── utils.py                # Utility functions for LLM integration (from Week 10 Practical)

Task2/
├── app/
│   ├── flask/
│   │   ├── main.py         # Flask API application
│   │   ├── index.html      # Frontend HTML page
│   │   └── requirements.txt
│   ├── docker/
│   │   └── Dockerfile
│   └── docker-compose.yml
├── diagrams/
│   ├── use_case_diagram.puml
│   └── use_case_diagram.png
├── tests/
│   └── test_api.py         # Unit tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml       # CI/CD pipeline
└── screenshots/            # Required screenshots
```

---

## Features

### Flask API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/notes` | POST | Add a reading note |
| `/notes` | GET | Get all notes (filter: genre, status, min_rating) |
| `/notes/<id>` | GET | Get specific note |
| `/notes/<id>` | PATCH | Update note (rating, status, quotes) |
| `/notes/<id>` | DELETE | Delete note |
| `/notes/<id>/quotes` | POST | Add a quote to a note |
| `/stats` | GET | Reading statistics |
| `/genres` | GET | Available genres |
| `/search?q=keyword` | GET | Search notes by keyword |
| `/` | GET | Frontend HTML page |

### Frontend Features

- Bootstrap 5 responsive dark theme design
- Book note form with title, author, genre, rating, reading notes
- Real-time statistics dashboard (total books, avg rating, quotes)
- Search and filter by genre
- Delete notes
- **AI-generated SVG image** (open book illustration)

---

## Running the Application

### Local Development

```bash
# Install dependencies
cd Task2/app/flask
pip install -r requirements.txt

# Run Flask API
python main.py
```

Access: http://127.0.0.1:5005

### Docker Deployment

```bash
# Build and run with Docker Compose
cd Task2/app
docker-compose up --build
```

---

## Testing

```bash
# Run unit tests
cd Task2
python -m unittest discover tests
```

All 15 tests pass.

---

## CI/CD Pipeline

The GitHub Actions workflow includes:
1. **Build and Test** - Python setup, dependency install, unit tests
2. **Build Docker Image** - Docker image creation with caching
3. **Deploy** - Manual deployment trigger
4. **Failure Notification** - Auto-create issue on failure

---

## AI-DLC Methodology

This project follows the **AI-Driven Development Lifecycle (AI-DLC)** approach:

1. **Phase 1: Inception** - AI generates problem statements, personas, requirements, user stories
2. **Phase 2: Construction** - AI generates Flask code, HTML, UML diagrams
3. **Phase 3: Operation** - Docker configuration, CI/CD setup

---

## References

- Week 10 Practical - AI-DLC baseline code
- Chapter 10 Lecture - AI-Driven Development Lifecycle methodology
- Flask documentation: https://flask.palletsprojects.com/
- PlantUML: https://plantuml.com/
