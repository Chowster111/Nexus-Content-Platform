# Engineering Blog Recommender – Backend

This is the **FastAPI + Supabase** backend for the **Engineering Blog Recommender**, a modern AI-powered system that gathers, classifies, tags, embeds, and recommends high-quality engineering articles from top sources like Netflix, Airbnb, Uber, Stripe, and more.

---

## Overview

The backend handles scraping, semantic embeddings, search and recommendation logic, user authentication, analytics, and observability. It exposes a robust REST API that the React frontend consumes.

This backend uses:

* **FastAPI** for high-performance Python API services.
* **Supabase** as a managed PostgreSQL database and authentication provider.
* **Sentence Transformers** for semantic similarity and embedding generation.
* **KeyBERT** for automatic tag extraction.
* **Prometheus and Grafana** for observability and real-time metrics.
* **Structured Logging** and retry logic with exponential backoff for reliability.

---

## Features

* Blog scraper for multiple sources using Selenium and BeautifulSoup.
* Semantic classification and vector similarity search with BGE embeddings.
* Automatic keyword and tag extraction with KeyBERT.
* REST API for semantic search and personalized recommendations.
* User authentication and session management via Supabase Auth.
* Likes persistence for per-user personalization.
* Health check and metrics endpoints for production readiness.
* Observability stack with Prometheus metrics and Grafana dashboards.
* Robust retry logic with exponential backoff for critical database/API calls.
* Load balancing ready with reverse proxy support via Nginx.

---

## Tech Stack

| Technology                       | Purpose                                                             |
| -------------------------------- | ------------------------------------------------------------------- |
| **FastAPI**                      | Lightweight, asynchronous Python API framework.                     |
| **Supabase (PostgreSQL + Auth)** | Hosted Postgres database, vector store, and secure user management. |
| **Sentence Transformers**        | Generate deep semantic embeddings for similarity search.            |
| **KeyBERT**                      | Extracts relevant keywords for tagging articles.                    |
| **Selenium + BeautifulSoup**     | Web scraping of engineering blogs.                                  |
| **Prometheus**                   | Exposes metrics for monitoring and alerts.                          |
| **Grafana**                      | Visualize API performance, DB latency, and traffic patterns.        |
| **Nginx**                        | Reverse proxy and load balancing for scale-out deployment.          |

---

## Project Structure

```
backend/
├── engine/                 # Recommender system logic
├── routes/                 # API route handlers (articles, analytics, scraper, auth, health, etc.)
├── utils/                  # Logging, retry, embedding helpers
├── db/                     # Supabase client connection
├── tests/                  # Unit, integration, and deployment tests
├── logging_config.py       # Centralized structured logger
├── main.py                 # FastAPI app entry point
└── Dockerfile
```

---

## API Endpoints

| Endpoint               | Description                                                      |
| ---------------------- | ---------------------------------------------------------------- |
| `/api/scrape/*`        | Scrape specific blog sources or all blogs at once.               |
| `/api/search/articles` | Search articles by keyword with semantic similarity.             |
| `/api/find/recommend`  | Get personalized recommendations based on user likes.            |
| `/api/user/likes`      | Save or update user-specific likes.                              |
| `/api/analytics/*`     | Provides site-level usage stats by source and category.          |
| `/auth/signup`         | Create a new user with Supabase Auth.                            |
| `/auth/signin`         | Sign in with Supabase credentials.                               |
| `/health`              | Health check endpoint that verifies DB connectivity and latency. |
| `/metrics`             | Prometheus metrics exporter for Grafana dashboards.              |

---

## Observability and Reliability

* **Retry logic:** All critical operations (Supabase writes, scraping jobs) use exponential backoff and retries.
* **Structured logging:** Detailed request, error, and performance logs with correlation IDs.
* **Health checks:** Automated DB status and API readiness checks, with Prometheus-friendly output.
* **Prometheus and Grafana:** Visual dashboards for request latency, DB query times, and API health.
* **Load balancing:** Ready for Nginx reverse proxy and scale-out container deployments.

---

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/engineering-blog-recommender.git
   cd backend
   ```

2. **Create environment variables**

   ```env
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-supabase-key
   HF_API_TOKEN=your-huggingface-token
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI server**

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`.

---

## Deployment Recommendations

* Run behind **Nginx** as a reverse proxy with SSL termination.
* Use **Docker Compose** for local dev and single-node deployments.
* Use **AWS ECS** or **EKS** for container orchestration and autoscaling.
* Use **AWS Lambda + EventBridge** for periodic scraping jobs if converting scrapers to serverless tasks.
* Store embeddings and metadata in Supabase; vector search is handled in-memory with Sentence Transformers.
* Visualize observability data in **Grafana**, scraping `/metrics` with **Prometheus**.

---

## Testing

* Unit tests, integration tests, and deployment tests with **Pytest** and **HTTPX**.
* Linting with **Ruff** for consistent style.
* Sample test commands in `backend/tests/`.

---

## Author

Arijit Chow