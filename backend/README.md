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

## API Documentation

### 📚 Comprehensive API Documentation

This project includes extensive API documentation following modern best practices:

- **[Complete API Reference](API.md)** - Detailed endpoint documentation with examples
- **Interactive Swagger UI** - Available at `/docs` when running the server
- **OpenAPI Specification** - Auto-generated from FastAPI route decorators
- **Code Examples** - Python, JavaScript, and cURL examples for all endpoints

### 🎯 Key Documentation Features

- **Inline Documentation** - All endpoints have comprehensive docstrings and examples
- **Request/Response Examples** - Real-world usage examples for every endpoint
- **Error Handling** - Detailed error scenarios and status codes
- **Authentication Guide** - Complete auth flow with token management
- **Rate Limiting** - Clear limits and best practices
- **SDK Examples** - Ready-to-use code snippets in multiple languages

### 🚀 Quick Start with API

```bash
# Start the server
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# View interactive documentation
open http://localhost:8000/docs

# View API reference
open http://localhost:8000/redoc
```

### 📖 Documentation Structure

- **API.md** - Complete API reference with all endpoints
- **README.md** - Project overview and setup instructions
- **DEPLOYMENT.md** - Production deployment and monitoring guide
- **Inline Docs** - FastAPI route decorators with detailed descriptions

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
├── API.md                  # Complete API documentation
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

**📖 For complete API documentation, see [API.md](API.md)**

---

## Observability and Reliability

* **Retry logic:** All critical operations (Supabase writes, scraping jobs) use exponential backoff and retries.
* **Structured logging:** Detailed request, error, and performance logs with correlation IDs.
* **Health checks:** Automated DB status and API readiness checks, with Prometheus-friendly output.
* **Prometheus and Grafana:** Visual dashboards for request latency, DB query times, and API health.
* **Load balancing:** Ready for Nginx reverse proxy and scale-out container deployments.

---

## Type Validation and Error Handling

The backend implements comprehensive **runtime type validation** using Pydantic models to ensure data integrity and provide detailed error reporting.

### Runtime Validation Strategy

* **API Response Validation:** All endpoints validate response models before returning data
* **Database Data Validation:** Articles, users, and other entities are validated when loaded from DB
* **Scraper Data Validation:** Scraped articles are validated before database insertion
* **Embedding Validation:** Vector embeddings are checked for correct dimensions and data types

### Error Handling Features

* **Detailed Error Logging:** Validation errors include the problematic data and specific field issues
* **Graceful Degradation:** Invalid data is logged and skipped rather than crashing the API
* **Structured Error Responses:** API endpoints return consistent error formats with context
* **Partial Success Handling:** When some items fail validation, valid items are still returned

### Example Validation Flow

```python
# When loading articles from database
articles = []
errors = []
for article in db_response.data:
    try:
        articles.append(ArticleResponse(**article))  # Runtime validation
    except ValidationError as ve:
        logger.error(f"Validation error for article: {article} | {ve}")
        errors.append({"article": article, "error": str(ve)})

# Return valid articles with error count in response
return RecommendationResponse(
    articles=articles, 
    error=f"{len(errors)} articles failed validation" if errors else None
)
```

### Benefits

* **Catches Real Data Issues:** Validates actual runtime data from DB, APIs, scrapers
* **Prevents Runtime Crashes:** Malformed data is handled gracefully
* **Improves Debugging:** Detailed error context helps identify data problems
* **Ensures API Consistency:** All responses match expected schemas
* **Minimal Performance Impact:** Validation overhead is typically <1ms per item

### Validation Coverage

| Component | Validation Target | Error Handling |
|-----------|------------------|----------------|
| **API Controllers** | Response models (ArticleResponse, SearchResult, etc.) | Log errors, return partial results |
| **Recommender Engine** | Article data and recommendation output | Skip invalid articles, log issues |
| **Scrapers** | Scraped article structure | Skip invalid articles, continue scraping |
| **Database Layer** | Query results and data types | Log validation errors, handle gracefully |
| **Health Checks** | System status responses | Validate health check output structure |

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
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`.

5. **View API Documentation**

   - Interactive docs: `http://localhost:8000/docs`
   - ReDoc docs: `http://localhost:8000/redoc`
   - Complete reference: See [API.md](API.md)

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