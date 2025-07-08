## Quickstart Guide

This guide will help you set up the Engineering Blog Recommender system locally using Docker Compose, configure Supabase, and provide the necessary environment variables for both backend and frontend.

---

## Queries (Supabase Setup)

1. **Create a Supabase Project**
   - Go to [Supabase](https://supabase.com/) and create a new project.
   - Note your `SUPABASE_URL` and `SUPABASE_KEY` (service role or anon key as needed).

2. **Set Up Database Schema**
   - In the Supabase dashboard, use the SQL editor to run the schema creation queries for your tables (articles, likes, etc.).
   - Example:
     ```sql
     -- Articles table
     create table articles (
       id uuid primary key default uuid_generate_v4(),
       title text,
       url text,
       published_date timestamp with time zone,
       content text,
       source text,
       tags text[],
       category text,
       inserted_at timestamp with time zone default timezone('utc'::text, now()),
       embedding double precision[],
       summary text
     );

     -- Likes table
     create table likes (
       id uuid primary key default uuid_generate_v4(),
       user_id uuid,
       article_url text,
       timestamp timestamp without time zone default now(),
       liked boolean
     );
     ```
   - (Add or adjust fields as needed for your use case.)

3. **Enable Auth**
   - In the Supabase dashboard, enable email/password authentication under the Auth settings.

---

## Docker Compose

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/engineeringBlogRecSystem.git
   cd engineeringBlogRecSystem
   ```

2. **Create Environment Files**
   - In the project root, create a `.env` file for backend keys:
     ```
     SUPABASE_URL=your-supabase-url
     SUPABASE_KEY=your-supabase-service-role-key
     HF_API_TOKEN=your-huggingface-api-token
     ```
   - In `frontend/`, create a `.env` file:
     ```
     VITE_SUPABASE_URL=your-supabase-url
     VITE_SUPABASE_ANON_KEY=your-supabase-anon-key
     VITE_SENTRY_DSN=your-sentry-dsn (optional)
     ```

3. **Run Docker Compose**
   ```bash
   docker-compose up --build
   ```
   - This will start the backend (FastAPI), frontend (React), Prometheus, and Grafana.
   - Backend: [http://localhost:8000](http://localhost:8000)
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Prometheus: [http://localhost:9090](http://localhost:9090)
   - Grafana: [http://localhost:3001](http://localhost:3001)

---

## Keys

- **Backend (`.env` in project root or backend/):**
  - `SUPABASE_URL` – Your Supabase project URL
  - `SUPABASE_KEY` – Supabase service role key (for backend access)
  - `HF_API_TOKEN` – HuggingFace API token (for embeddings)

- **Frontend (`frontend/.env`):**
  - `VITE_SUPABASE_URL` – Your Supabase project URL
  - `VITE_SUPABASE_ANON_KEY` – Supabase anon/public key (for frontend auth)
  - `VITE_SENTRY_DSN` – (Optional) Sentry DSN for error tracking

