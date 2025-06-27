# Engineering Blog Recommender

This is a full-stack AI system that gathers, classifies, tags, embeds, and recommends over 10,000 articles from leading engineering blogs including Netflix, Airbnb, Uber, Stripe, and more.

### Features

* Semantic search and exploration of engineering articles
* AI-powered article recommendations
* Content preview and swipe-to-like interface
* User authentication and per-user like tracking
* Recommendations personalized using user likes
* Observability stack with Grafana and Prometheus for real-time metrics
* Robust logging and error handling across backend services
* Exponential backoff and retry logic on all critical API/database calls
* Production-grade health check endpoint with external service validation

---

## Screenshots

### Homepage

![Homepage Screenshot](screenshots/homePage.png)

### Results

![Homesearch Screenshot](screenshots/homeScroll.png)

### Swipe Mode

![Swipe Mode](screenshots/homeSwipe.png)

---

## Frontend (React + TypeScript)

The frontend is a modern React app built with:

* TypeScript + Vite
* Framer Motion for animations
* CSS Modules for scoped styling
* `react-loading-skeleton` for async placeholders
* Swipe Mode: Tinder-style swipe-to-like experience
* Toggle UI: Switch between search and personalized recommendation views
* Auth-aware UI: Likes are tied to authenticated users

---

## Backend Features

| Feature                      | Description                                                               |
| ---------------------------- | ------------------------------------------------------------------------- |
| Blog Scraper                 | Collects articles using Selenium and BeautifulSoup                        |
| Semantic Classification      | Uses BGE embeddings + cosine similarity to classify articles              |
| Automatic Tagging            | Uses KeyBERT to extract relevant tags                                     |
| Supabase Integration         | Stores article metadata, embeddings, and user likes in hosted Postgres DB |
| Search                       | Search articles by keyword, tag, or source                                |
| Personalized Recommendations | Suggests similar articles using user likes and embeddings                 |
| Analytics API                | Provides trending tags, top sources, and article category statistics      |
| User Auth Integration        | Full authentication flow with Supabase Auth                               |
| Likes Persistence            | Stores user-specific like/dislike data for future personalization         |
| FastAPI Backend              | Modular, production-ready Python API framework                            |
| Logging                      | Super-granular request and error logging using structured Python logging  |
| Healthcheck Endpoint         | Startup, database, and latency verification with Prometheus-friendly output |
| Retry Logic                  | Exponential backoff and retry on failures (e.g. database insertions)      |
| Observability                | Built-in Prometheus metrics endpoint with a Grafana dashboard             |
| Load Balancing               | Used Nginx for load balancing when deployed onto docker and AWS           |


---

## Project Structure

```

.
├── backend/                   # FastAPI backend
│   ├── engine/                # Recommender system logic
│   ├── routes/                # API route handlers
│   ├── utils/                 # Logging, retry, healthcheck, observability
│   ├── tests/                 # Unit, integration, and deployment tests
│   ├── main.py
│   └── logging\_config.py
│
├── frontend/                  # React frontend (Vite + TypeScript)
│   ├── components/
│   ├── styles/
│   └── App.tsx
│
├── db/
│   └── supabase\_client.py
│
├── scrapers/
│   ├── netflix.py
│   └── ...
│
├── docker-compose.yml
├── .env
└── README.md

````

---

## Setup (Docker)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/engineering-blog-recommender.git
cd engineering-blog-recommender
````

### 2. Create `.env` File

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-key
HF_API_TOKEN=your-huggingface-token
```

Place this `.env` file in the root directory.

### 3. Run with Docker Compose

```bash
docker-compose up --build
```

This will:

* Start the FastAPI backend at `http://localhost:8000`
* Serve the React frontend at `http://localhost:3000` (proxying API calls)
* Enable Prometheus metrics at `/metrics`
* Connect to Supabase and HuggingFace via your `.env` credentials
* Expose Grafana dashboard at `http://localhost:3001` for observability

---

## API Endpoints

| Endpoint                    | Description                             |
| --------------------------- | --------------------------------------- |
| `/api/scrape/netflix`       | Scrapes Netflix Engineering blog        |
| `/api/recommend`            | Recommends similar articles             |
| `/api/search/articles`      | Searches articles by keyword            |
| `/api/user/likes`           | Stores likes/dislikes for a user        |
| `/api/analytics/tags`       | Returns most frequent tags              |
| `/api/analytics/categories` | Returns distribution by category        |
| `/health`                   | Full healthcheck for service + database |
| `/metrics`                  | Prometheus metrics endpoint             |

---

## Models Used

* `BAAI/bge-base-en-v1.5` — Sentence embeddings for semantic similarity
* `KeyBERT` — Keyword/tag extraction
* `facebook/bart-large-cnn` — Summarization model via inference API

---

## Example Queries

```bash
curl http://localhost:8000/find/recommend?query=GraphQL
curl http://localhost:8000/search/articles?q=Machine+Learning
```

---

## Testing Infrastructure

| Test Type         | Coverage Area                                  |
| ----------------- | ---------------------------------------------- |
| Linting           | Code formatting using Ruff                     |
| Unit Tests        | Utility functions, schema validation           |
| Integration Tests | API endpoints (auth, likes, search, recommend) |
| Deployment Tests  | Smoke tests to verify deployed API health      |
| Test Frameworks   | Pytest + HTTPX                                 |

All tests are located under `backend/tests/`.

---

## Observability and Reliability

This project includes a complete observability stack for production-grade monitoring and diagnostics.

* **Grafana Dashboard** — Visualize API health, request latency, and user traffic patterns
* **Prometheus Exporter** — Exposes metrics at `/metrics` compatible with Prometheus scrapers
* **Structured Logging** — Logs include detailed request context, errors, and retry attempts
* **Healthcheck Endpoint** — Checks DB connectivity and API readiness
* **Retry and Backoff** — All critical operations (e.g. likes, Supabase writes) use automatic retries with exponential backoff to reduce failure rates

---

## Data Sources

* [Netflix Tech Blog](https://netflixtechblog.com/)
* [Airbnb Engineering](https://medium.com/airbnb-engineering)
* [Uber Engineering](https://www.uber.com/blog/engineering/)
* [Stripe Engineering](https://stripe.com/blog)
* [Tinder Engineering](https://medium.com/tinder)

---

## Status

![Lint Status](https://img.shields.io/badge/lint-passing-brightgreen)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](https://github.com/yourusername/engineering-blog-recommender/actions)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://hub.docker.com/repository/docker/yourusername/engineering-blog-recommender)
[![License](https://img.shields.io/github/license/yourusername/engineering-blog-recommender)](LICENSE)

---

## Author

Built by Arijit Chowdhury — Full-stack developer with experience in AI systems, scalable infrastructure, and end-to-end product delivery.

