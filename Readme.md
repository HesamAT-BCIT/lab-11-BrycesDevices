[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Wcc6KCy9)
## Overview

In this lab, you will containerize your Flask application using Docker and enhance it with structured logging.

You will practice:

1. Writing a Dockerfile for a Python Flask application
2. Creating docker-compose.yml for orchestrating services
3. Adding structured logging to application code paths

The goal is to make your app deployment-ready for this lab with containerization and observability.

---

## Quick Setup (One-Time)

1. Ensure Docker Desktop is installed and running:
   - Download from https://www.docker.com/products/docker-desktop
   - Verify with: `docker --version`

2. Make sure your project runs locally before containerizing.

---

## Task 1: Create a Dockerfile

Create a `Dockerfile` in the project root to containerize your Flask application.

### Requirements

1. Use Python 3.11 as the base image
2. Set a working directory (e.g., `/app`)
3. Copy `requirements.txt` and install dependencies
4. Copy all application code
5. Expose port 5000
6. Set the command to run the Flask app

### Suggested Dockerfile structure

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

### Tips

- Use `.dockerignore` to exclude unnecessary files (e.g., `.venv/`, `__pycache__/`, `.git/`)
- Consider using `gunicorn` for production instead of the Flask development server

---

## Task 2: Create docker-compose.yml

Create a `docker-compose.yml` file to orchestrate your application.

### Requirements

1. Define a service named `web` for your Flask app
2. Build from the current directory
3. Map port 5000 (host) to 5000 (container)
4. Set environment variables from a `.env` file
5. Configure a volume for code hot-reloading (optional, for development)

### Suggested docker-compose.yml structure

```yaml
version: "3.8"

services:
  web:
    build: .
    ports:
      - "5000:5000"
    env_file:
      - .env
    volumes:
      - .:/app
    environment:
      - FLASK_DEBUG=1
```

### Tips

- Ensure your `.env` file exists with the required variables used by `config.py`/Firebase setup
- Consider adding a `.env.example` so required keys are explicit and reproducible
- The volumes mapping enables hot-reloading during development

---

## Task 3: Verify Docker Compose

Run your containerized application and verify it works correctly.

### Steps

1. Build and start the containers:
   ```bash
   docker compose up --build
   ```
   If your Docker installation uses the legacy command, use:
   ```bash
   docker-compose up --build
   ```

2. Verify the application is accessible at `http://localhost:5000`

3. Test at least one endpoint (e.g., the dashboard or health check)

4. Stop the containers with `Ctrl+C` or:
   ```bash
   docker compose down
   ```
   (Legacy: `docker-compose down`)

### Success Criteria

- `docker compose up --build` (or legacy `docker-compose up --build`) completes without errors
- The Flask app starts and responds to requests
- No container crashes or immediate exits

---

## Task 4: Add Structured Logging

Enhance your application with structured logging (JSON format) to at least one code path.

### Requirements

1. Use Python's `logging` module with a structured format
2. Add logging to at least one meaningful code path (e.g., API endpoint, authentication flow)
3. Include contextual information (timestamps, log level, module name, message)

### Suggested implementation

Create or update a logging configuration in your application:

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(log_entry)

# Configure logging
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logging.root.addHandler(handler)
logging.root.setLevel(logging.INFO)
```

### Where to add logging

Choose at least one of the following:

1. **API endpoints** - Log incoming requests with method, path, and response status
2. **Authentication flow** - Log successful/failed authentication attempts
3. **Profile operations** - Log CRUD operations on user profiles
4. **Error handlers** - Log exceptions with stack traces

### Example usage in a route

```python
import logging
logger = logging.getLogger(__name__)

@bp.route("/api/data", methods=["POST"])
def handle_data():
    logger.info("Received data request", extra={"method": "POST", "path": "/api/data"})
    # ... process request ...
    logger.info("Data processed successfully")
    return {"status": "success"}
```

---

## Deliverables

Complete and submit the following files/artifacts:

```
Dockerfile                    # Container definition for Flask app
docker-compose.yml            # Docker Compose orchestration file
.dockerignore                 # Files to exclude from Docker build

utils/logging_config.py       # (Or similar) Structured logging configuration
blueprints/*/routes.py        # Updated with logging statements
```

Docker proof (include in your submission):
- Screenshot of `docker compose up --build` output showing successful startup (or legacy `docker-compose up --build`)
- Screenshot of your app running in browser at localhost:5000

---

## Success Criteria

1. Dockerfile builds successfully without errors:
   ```bash
   docker build -t flask-app .
   ```

2. Docker Compose starts the application:
   ```bash
   docker compose up --build
   ```

3. Application is accessible and functional at `http://localhost:5000`

4. Structured logging is implemented and produces JSON-formatted log output

5. Submission includes Docker proof

---

## Rubric

Each criterion is scored out of 5 points.

### 1. Dockerfile - /5

- Level 5 (5): Dockerfile follows best practices with proper base image, dependency installation, and optimized layers. Includes .dockerignore.
- Level 4 (4): Dockerfile builds successfully with minor optimization opportunities.
- Level 3 (3): Dockerfile builds but has issues (large image size, missing optimizations).
- Level 2 (2): Dockerfile builds with errors or requires fixes.
- Level 1 (1): Dockerfile has major errors or fails to build.

### 2. Docker Compose - /5

- Level 5 (5): docker-compose.yml properly configures the service with ports, environment variables, and volumes for development.
- Level 4 (4): docker-compose.yml works correctly with minor configuration gaps.
- Level 3 (3): Basic docker-compose exists with some configuration issues.
- Level 2 (2): docker-compose has significant issues but partially works.
- Level 1 (1): docker-compose.yml is missing or non-functional.

### 3. Structured Logging - /5

- Level 5 (5): JSON-formatted logging implemented in at least one meaningful code path with contextual information (timestamp, level, module, message, and request context where relevant).
- Level 4 (4): Structured logging works in at least one code path with proper formatting but with minor context gaps.
- Level 3 (3): Logging exists with some structure but missing context.
- Level 2 (2): Basic logging exists but lacks structure or context.
- Level 1 (1): No meaningful logging implementation.

### 4. Documentation and Proof - /5

- Level 5 (5): Clear screenshots of Docker startup and running app with all required elements.
- Level 4 (4): Most proof artifacts included with minor gaps.
- Level 3 (3): Proof provided but some elements missing.
- Level 2 (2): Partial proof provided; several required elements missing.
- Level 1 (1): Little or no proof of successful execution.

**Total Score: /20**
