# 🧠 Engineering Blog Recommender

This is a full-stack system that **gathers, classifies, tags, embeds, and recommends** 10,000+ articles from top engineering blogs like Netflix, Airbnb, Uber, and more.

You can:
- 🔍 **Search** and semantically explore blog posts  
- 🤖 **Receive AI-powered recommendations**  
- 📰 **Preview summaries**, visit links, and even swipe through results  
- ❤️ **Like, dislike, and favorite** articles to improve recommendations  

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
- **TypeScript** + **Vite**
- **Framer Motion** for animations
- **CSS Modules** for scoped styling
- **`react-loading-skeleton`** for async placeholders
- **Swipe Mode**: Tinder-style swipe-to-like UX
- **Toggle UI**: Seamlessly switch between search and recommendation views

### Features
| Feature        | Description                                    |
|----------------|------------------------------------------------|
| 🖼️ Card UI     | Displays articles with title, tags, source, etc. |
| 🔄 Swipe Mode  | One-at-a-time card interface with like/dislike |
| 🧠 Smart Summaries | Articles show clean summaries via AI       |
| 🎛️ Toggleable Mode | Switch between list or swipe view         |

---

## 🚀 Backend Features

| Feature                         | Description                                                                 |
|--------------------------------|-----------------------------------------------------------------------------|
| ✅ Blog Scraper                | Scrapes engineering blogs via Selenium and BeautifulSoup                   |
| 🧠 Semantic Classification     | Categorizes articles using BGE embeddings + cosine similarity               |
| 🏷️ Automatic Tagging          | Extracts relevant tags using KeyBERT                                        |
| 🔐 Supabase Integration        | Stores article metadata, embeddings, and content in a hosted Postgres DB   |
| 🔍 Search                      | Search articles by keyword, tag, or source                                  |
| 🤖 Recommendations            | Suggest similar articles based on sentence-transformer embeddings           |
| 📊 Analytics API               | Provides trending tags, top sources, and category counts                    |
| 🌐 FastAPI Backend             | Clean, modular API endpoints                                                |

---

## 🧩 Project Structure

```

.
├── scrapers/                   # Scraper logic per blog
│   ├── netflix.py
│   ├── airbnb.py
│   └── ...
├── frontend/                   # React app (Vite + TS)
│   ├── components/
│   ├── styles/
│   └── App.tsx
├── db/
│   └── supabase\_client.py
├── routers/
│   ├── search.py
│   ├── recommend.py
│   └── analytics.py
├── utils/
│   ├── embedding\_utils.py
│   └── constants.py
├── main.py
└── requirements.txt

````

---

## 🛠️ Setup

### 1. Clone

```bash
git clone https://github.com/yourusername/engineering-blog-recommender.git
cd engineering-blog-recommender
````

### 2. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Set Environment

Create a `.env` or export:

```env
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
HF_API_TOKEN=your-huggingface-token
```

### 5. Run Backend

```bash
uvicorn main:app --reload
```

---

## 🔌 API Endpoints

| Endpoint               | Description                            |
| ---------------------- | -------------------------------------- |
| `/scrape/netflix`      | Scrapes Netflix Engineering blog       |
| `/recommend?title=...` | Recommends similar articles            |
| `/search?q=...`        | Searches articles by keyword           |
| `/most-common-tags`    | Most frequent tags across all articles |
| `/category-count`      | Distribution of articles by category   |

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
