# 🧠 Engineering Blog Recommender

This is a full-stack system that **gathers, classifies, tags, embeds, and recommends** 10,000+ articles from top engineering blogs like Netflix, Airbnb, Uber, and more.

You can:

* 🔍 **Search** and semantically explore blog posts
* 🤖 **Receive AI-powered recommendations**
* 📰 **Preview summaries**, visit links, and even swipe through results
* ❤️ **Like, dislike, and favorite** articles to improve recommendations

---

## 🖼️ Screenshots

### 🔍 Homepage

![Homepage Screenshot](screenshots/homePage.png)

### 🔍 Results

![Homesearch Screenshot](screenshots/homeScroll.png)

### 🤖 Swipe Mode

![Swipe Mode](screenshots/homeSwipe.png)

---

## ✨ Frontend (React + TypeScript)

The frontend is a modern **React app** built with:

* **TypeScript** + **Vite**
* **Framer Motion** for animations
* **CSS Modules** for scoped styling
* **`react-loading-skeleton`** for async placeholders
* **Swipe Mode**: Tinder-style swipe-to-like UX
* **Toggle UI**: Seamlessly switch between search and recommendation views

---

## 🚀 Backend Features

| Feature                    | Description                                                              |
| -------------------------- | ------------------------------------------------------------------------ |
| ✅ Blog Scraper             | Scrapes engineering blogs via Selenium and BeautifulSoup                 |
| 🧠 Semantic Classification | Categorizes articles using BGE embeddings + cosine similarity            |
| 🏷️ Automatic Tagging      | Extracts relevant tags using KeyBERT                                     |
| 🔐 Supabase Integration    | Stores article metadata, embeddings, and content in a hosted Postgres DB |
| 🔍 Search                  | Search articles by keyword, tag, or source                               |
| 🤖 Recommendations         | Suggest similar articles based on sentence-transformer embeddings        |
| 📊 Analytics API           | Provides trending tags, top sources, and category counts                 |
| 🌐 FastAPI Backend         | Clean, modular API endpoints                                             |

---

## 🧩 Project Structure

```
.
├── backend/                   # FastAPI backend
│   ├── routers/
│   ├── utils/
│   └── main.py
│
├── frontend/                 # React frontend (Vite + TS)
│   ├── components/
│   ├── styles/
│   └── App.tsx
│
├── db/
│   └── supabase_client.py
│
├── scrapers/
│   ├── netflix.py
│   └── ...
│
├── docker-compose.yml
├── .env
└── README.md
```

---

## 🛠️ Setup (Docker)

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/engineering-blog-recommender.git
cd engineering-blog-recommender
```

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

* 🚀 Start the FastAPI backend at `http://localhost:8000`
* 🌐 Serve the React frontend at `http://localhost:3000` (with proxy to `/api/`)
* 🧠 Connect your backend to Supabase and HuggingFace with your `.env` vars

---

## 🔌 API Endpoints

| Endpoint                | Description                            |
| ----------------------- | -------------------------------------- |
| `/api/scrape/netflix`   | Scrapes Netflix Engineering blog       |
| `/api/recommend`        | Recommends similar articles            |
| `/api/search/articles`  | Searches articles by keyword           |
| `/api/most-common-tags` | Most frequent tags across all articles |
| `/api/category-count`   | Distribution of articles by category   |

---

## 🤖 Models Used

* [`BAAI/bge-base-en-v1.5`](https://huggingface.co/BAAI/bge-base-en-v1.5) — Embeddings
* [`KeyBERT`](https://github.com/MaartenGr/KeyBERT) — Tagging
* [`facebook/bart-large-cnn`](https://huggingface.co/facebook/bart-large-cnn) — Summarization via inference API

---

## 🧪 Example Queries

```bash
curl http://localhost:8000/recommend?title=Scaling+our+Data+Infra
curl http://localhost:8000/search?q=GraphQL
```

---

## 📦 Roadmap

* [x] Swipe interface
* [x] Summary fallback UI
* [x] Auto tag extraction
* [ ] Personalized feed per user
* [ ] Embed search (FAISS)
* [ ] Weekly digest emails

---

## 📚 Data Sources

* [Netflix Tech Blog](https://netflixtechblog.com/)
* [Airbnb Engineering](https://medium.com/airbnb-engineering)
* [Uber Engineering](https://www.uber.com/blog/engineering/)
* [Stripe Engineering](https://stripe.com/blog)
* [Tinder Engineering](https://medium.com/tinder)

---

## 🧑‍💻 Author

Built with 💻 and ☕ by **Arijit Chowdhury**