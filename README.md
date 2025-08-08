# EBC Intel Radar

This repository contains a full stack application that monitors entertainment news, events and competitor insights for Encore Beach Club in Las Vegas. It scrapes news from multiple sources, processes the results with AI, stores them in a database and exposes them via a REST API and modern web dashboard.

## Project structure

```
.
├── backend
│   ├── app
│   │   ├── __init__.py
│   │   ├── api.py
│   │   ├── celery_app.py
│   │   ├── db.py
│   │   ├── main.py
│   │   ├── models.py
│   │
db.py
│   │   └── ...
│   │
│   └── celery
│       ├── __init__.py
│       └── tasks.py
│
├── frontend
│   ├── pages
│   │   ├── _app.js
│   │   └── index.js
│   │
│   ├── styles
│   │   └── globals.css
│   │
│   ├── Dockerfile
│   │   next.config.js
│   │   package.json
│
├── docker-compose.yml
└── .env.example
```

### Services

- **Backend** – A FastAPI application that serves the REST endpoints, exposes the news database and starts Celery tasks.
- **Celery worker** – Processes tasks such as fetching news from the Perigon API, summarising them with OpenAI and sending Slack notifications.
- **Database** – Postgres stores news items and other metadata.
- **Redis** – Used as the broker and result backend for Celery.
- **Frontend** – A Next.js application that displays the dashboard and allows refreshing news.

## Getting started

1. Clone the repository:

```bash
git clone https://github.com/LOV3RBOY/up-to-date.git
cd up-to-date
```

2. Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Update the variables for your database, Celery broker, Perigon API key, OpenAI API key and Slack webhook.

3. Build and start the services with Docker Compose:

```bash
docker compose up --build
```

The backend will be available at `http://localhost:8000` and the frontend dashboard at `http://localhost:3000`.

4. To fetch new articles, click the “Refresh News” button in the dashboard or call the `/refresh` endpoint.

## License

This project is provided as-is for demonstration purposes.
