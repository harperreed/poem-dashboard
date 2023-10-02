# Poem Dashboard

Poem Dashboard is a Flask application that generates and displays poems based on current world news headlines and weather information. The poems are generated using the OpenAI GPT-3.5-turbo model and are updated every hour. The application provides a simple web interface for viewing the generated poems.

## Features

- Real-time poem updates via SocketIO.
- Scheduled poem generation using APScheduler.
- Data fetching from external RSS feeds and weather APIs.
- Containerized deployment using Docker and Docker Compose.

## Prerequisites

- Python 3.10
- Docker and Docker Compose

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/poem-dashboard.git
    cd poem-dashboard
    ```

2. Create a virtual environment and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

## Running the Application

### Locally

1. Start the application:
    ```bash
    python main.py
    ```

2. Open your web browser and navigate to `http://localhost:5000` to view the application.

### Using Docker

1. Build and start the Docker containers:
    ```bash
    docker-compose up --build
    ```

2. Open your web browser and navigate to `http://localhost:5000` to view the application.

## Database Migrations

To create a new migration after changing the database models:

```bash
python your_script.py db migrate -m "Description of migration"
python your_script.py db upgrade
```

## Contributing

If you would like to contribute to this project, please fork the repository, create a new branch for your work, and submit a pull request.
