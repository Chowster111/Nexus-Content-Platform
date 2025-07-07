# Engineering Blog Recommender

**A production-ready, AI-powered content recommendation system that discovers, classifies, tags, embeds, and delivers over 10,000 articles from world-leading engineering blogs.**  
Built for real-time semantic search, personalized recommendations, and developer insights — with scalable architecture, robust error handling, and modern observability baked in.

---

## Why This Project Exists

Engineering blogs hold deep technical knowledge that is often hard to search and surface intelligently.  
This system acts as an **AI-driven semantic layer** for engineering content, providing:

- Fast, relevant recommendations powered by state-of-the-art embeddings  
- A frictionless swipe-to-like UX to personalize results  
- Insights into what technologies and categories are trending  
- Open APIs for future integrations (Slack bots, newsletters, RSS feeds)

---

## Highlights — What’s Under the Hood

- **Full-stack TypeScript & Python** — React + Vite frontend, FastAPI backend, Supabase Postgres.
- **Semantic Search** — Uses BAAI BGE embeddings + cosine similarity for relevance ranking.
- **Automatic Tagging** — KeyBERT and BART summarization pipeline for category extraction.
- **User Likes & Auth** — Supabase Auth, storing likes/dislikes to drive personalization.
- **Swipe Mode** — Mobile-inspired, Tinder-like swipe-to-like experience.
- **Observability** — Grafana dashboards, Prometheus metrics, structured logging.
- **Robustness** — Exponential backoff, retry logic on all critical paths, Sentry error tracking.
- **Scalable I/O** — Nginx reverse proxy and Docker Compose orchestration for dev/prod.
- **Edge-Caching Friendly** — Responses for analytics endpoints support CDN caching.

---

## Screenshots

| Home | Search Results | Swipe Mode |
|------|----------------|-------------|
| ![Home](screenshots/homePage.png) | ![Results](screenshots/homeScroll.png) | ![Swipe](screenshots/homeSwipe.png) |

---

## Full Feature Set

- **Semantic Search** — Vector embeddings for natural language queries.  
- **Personalized Recommendations** — Recommender logic considers user likes.  
- **Swipe-to-Like UI** — Save relevant content with a simple swipe gesture.  
- **Auth-Aware UI** — Only saves likes for authenticated users.  
- **Super-Granular Logging** — Tracks retries, errors, user actions.  
- **Observability** — Metrics exported via Prometheus, visualized in Grafana.  
- **Healthchecks** — Startup and DB connectivity checks for readiness probes.  
- **Retry with Exponential Backoff** — For all Supabase inserts and critical calls.  
- **Sentry on Frontend** — Automatic JS error tracking, release version tagging.  
- **Edge-Ready Analytics** — Cached popular sources/tags for fast rendering.

---

## Technologies Used

| Layer             | Tech Stack                                                                                                 |
|-------------------|------------------------------------------------------------------------------------------------------------|
| **Frontend**      | React, Vite, TypeScript, Framer Motion, CSS Modules, `react-loading-skeleton`, Supabase Auth, Sentry SDK   |
| **Backend**       | FastAPI, Python 3.11+, Supabase (Postgres), Hugging Face Transformers, KeyBERT, BART Summarization         |
| **Scrapers**      | Python, Selenium, BeautifulSoup                                                                            |
| **Observability** | Prometheus, Grafana, Python Logging, Sentry                                                                |
| **Infrastructure**| Docker Compose, Nginx reverse proxy/load balancing, .env-based secrets                                     |
| **Testing**       | Pytest, HTTPX for integration tests, Ruff for linting                                                      |

---

## Key Models

- `BAAI/bge-base-en-v1.5` — Sentence embeddings for similarity.
- `KeyBERT` — Keyword extraction for better tagging.
- `facebook/bart-large-cnn` — Summarization for concise article abstracts.

---

## API Endpoints

| Endpoint                    | Description                                                          |
|-----------------------------|----------------------------------------------------------------------|
| `/api/search/articles`      | Semantic search over all embedded articles                           |
| `/api/find/recommend`       | Returns recommendations based on query + user likes                  |
| `/api/user/likes`           | Stores user likes/dislikes                                           |
| `/api/analytics/blogs-by-source/{limit}` | Most frequent sources, for analytics page                    |
| `/api/analytics/category-count` | Article distribution by category                                   |
| `/api/scrape/{source}`      | Trigger scraper for a single source (Netflix, Airbnb, Uber, Stripe) |
| `/health`                   | Healthcheck for readiness & Supabase DB status                       |
| `/metrics`                  | Prometheus-compatible metrics export                                 |

---

## Observability & Reliability

**Prometheus** scrapes `/metrics` endpoint for request counts, latency, DB calls.  
**Grafana** dashboards visualize uptime, error rates, and query throughput.  
**Structured Logging** includes timestamps, trace context, retry attempts.  
**Retry + Exponential Backoff** prevents cascading failures on transient errors.  
**Sentry Frontend Integration** captures JavaScript runtime issues for fast debugging.

---

## Project Structure

```

.
├── backend/
│   ├── engine/                # Embedding + recommender logic
│   ├── routes/                # Search, recommend, likes, analytics endpoints
│   ├── utils/                 # Retry decorators, logging config, healthcheck
│   ├── main.py                # FastAPI app instance
│   ├── logging\_config.py
│   └── tests/                 # Pytest unit & integration tests
│
├── frontend/
│   ├── components/            # Reusable UI blocks (Search, Recommend, AnalyticsBox)
│   ├── pages/                 # Page routing (Home, future pages)
│   ├── services/              # API & likes client with Sentry integration
│   ├── styles/                # CSS Modules for isolated styling
│   ├── App.tsx                # Root wrapper
│   ├── main.tsx               # Vite entrypoint
│
├── scrapers/                  # Site-specific scrapers
│   ├── netflix.py
│   ├── airbnb.py
│   └── ...
│
├── db/                        # Supabase Postgres client
│   └── supabase\_client.py
│
├── nginx/                     # Nginx reverse proxy config
├── docker-compose.yml
├── .env                       # Secrets for Supabase & HF tokens
└── README.md

````

## Backend Stack: FastAPI + Supabase + PostgreSQL
The backend is built using FastAPI, a modern Python web framework known for its speed, async support, and developer-friendly automatic OpenAPI docs.

All structured data — including articles, embeddings metadata, user likes, and auth records — is stored in a PostgreSQL database hosted via Supabase, which acts as a backend-as-a-service with instant REST endpoints, row-level security, and authentication.

This design means:

- Strong typing and validation for all API endpoints via Pydantic models.

- Serverless auth & storage — Supabase handles user sessions, JWTs, and real-time updates.

- Scalable Postgres — Flexible SQL database with vector extension support if needed.

Together, FastAPI + Supabase + PostgreSQL keep the backend fast, type-safe, and ready to scale — without sacrificing observability, retries, or robust error handling.

---

## Local Setup

1. **Clone the repo**

```bash
git clone https://github.com/yourusername/engineering-blog-recommender.git
cd engineering-blog-recommender
````

2. **Create `.env`**

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-key
HF_API_TOKEN=your-huggingface-token
SENTRY_DSN=https://YOUR_SENTRY_DSN
```

3.  **Run Docker Compose**

```bash
docker-compose up --build
```

* Backend → `http://localhost:8000`
* Frontend → `http://localhost:3000`
* Prometheus → `/metrics`
* Grafana → `http://localhost:3001` (default login: `admin`)

---

## Testing

- **Unit tests** — Core utils, recommender logic
- **Integration tests** — Search, recommend, likes, analytics endpoints
- **Linting** — `ruff` for Python, Prettier for JS/TS

```bash
pytest backend/tests
```

---

## Example Queries

```bash
curl 'http://localhost:8000/find/recommend?query=GraphQL'
curl 'http://localhost:8000/search/articles?q=Machine+Learning'
```

---

## Infrastructure — What We Use and Why

Our deployment stack balances local development simplicity with production-ready patterns.

| Layer            | What We Use                                          | Why We Use It                                                                      | Trade-offs                                                   |
|------------------|------------------------------------------------------|-------------------------------------------------------------------------------------|--------------------------------------------------------------|
| **Containers**   | Docker, Docker Compose                               | Consistent local dev, reproducible builds.                                         | Docker Compose for dev; ECS Fargate or K8s for production.   |
| **Registry**     | AWS ECR                                              | Private, secure image storage, IAM-based access.                                   | Slightly more setup than Docker Hub; tighter integration.    |
| **Orchestration**| ECS with Fargate                                     | Serverless containers, no VM maintenance, scales automatically.                    | Higher per-unit cost vs. EC2; lower ops overhead.            |
| **Serverless**   | AWS Lambda                                           | Runs scrapers/batch jobs without idle costs.                                       | Runtime limits; move to ECS if jobs grow too large.          |
| **Networking**   | VPC, public subnets, Internet Gateway, ALB           | Isolated, routable network; ALB handles traffic and routing.                       | Uses public subnets for dev; private subnets recommended for prod. |
| **Secrets**      | .env for local; IAM roles; Terraform outputs         | Keeps secrets out of code; uses IAM for container/ECR auth.                        | Upgrade to AWS Secrets Manager for production.               |
| **State**        | Terraform S3 backend + DynamoDB lock (optional)      | Shared, consistent state across team; prevents conflicting applies.                | Local state fine for solo dev; remote state recommended for teams. |
| **Observability**| Prometheus, Grafana, Sentry, structured logging      | Monitors query throughput, errors, retries, user actions.                          | Adds containers to dev; use managed observability in prod.   |

### How It Fits Together
- **`docker-compose.yml`** runs backend, frontend, scrapers, Nginx reverse proxy, and Prometheus locally.
- **Nginx** routes API calls, serves static frontend, and exposes metrics.
- **Terraform** provisions all AWS resources in modular pieces: VPC, ECR, ECS/Fargate, ALB, Lambda.
- **State** is stored remotely (S3 + DynamoDB) to avoid accidental overwrites when multiple team members apply infra changes.

**Key Trade-off:** We use public subnets and simpler IAM for dev speed; production should add private subnets, stricter secrets handling, and automated pipelines.

This setup keeps your AI-powered recommender infrastructure modular, observable, and scalable with minimal extra operational burden.


---

## What’s Next

* Caching layers for heavy analytics endpoints.
* Edge deployment using CDN edge functions.
* New pages scaffolded under `src/pages/` with React Router for future features.
* Better role-based auth and multi-user dashboards.

---

## Status

![Lint Status](https://img.shields.io/badge/lint-passing-brightgreen)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![License](https://img.shields.io/github/license/yourusername/engineering-blog-recommender)

---

## Author

Built by **Arijit Chowdhury**
Full-stack engineer | AI systems | Scalable backend | Observability-first mindset

---

**Clone. Run. Observe. Ship.**
Production-grade AI infra for engineering content discovery.
