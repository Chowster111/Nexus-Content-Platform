# 🧠 Engineering Blog Recommender

This is a full-stack system that **gathers classifies, tags, embeds, and recommends** 10,000 + articles from top engineering blogs like Netflix, Airbnb, Uber, and more. You are then able to get recommendations and recieve previews/summaries of each blog based on what you choose. You are able to like, dislike and favourite, improving the quality or recommendations you get.

It powers:
- 📰 A growing archive of tech blog posts  
- 🔍 Search + semantic understanding  
- 🤖 AI-powered personalized recommendations  
- 📊 Developer-focused analytics

---

## 🚀 Features

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
├── scrapers/
│   ├── netflix.py
│   ├── airbnb.py
│   ├── uber.py
│   └── ...
│
├── db/
│   └── supabase\_client.py
│
├── routers/
│   ├── search.py
│   ├── recommend.py
│   └── analytics.py
│
├── utils/
│   ├── embedding\_utils.py
│   └── constants.py
│
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

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment

Create a `.env` or configure your Supabase URL and key:

```env
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
```

### 4. Run API

```bash
uvicorn main:app --reload
```

---

## 🔌 Key Endpoints

| Endpoint                 | Description                            |
| ------------------------ | -------------------------------------- |
| `/scrape/netflix`        | Scrapes Netflix Engineering blog       |
| `/scrape/airbnb`         | Scrapes Airbnb Engineering blog        |
| `/scrape/uber`           | Scrapes Uber Engineering blog          |
| `/recommend?title=...`   | Recommends similar articles            |
| `/search?q=...`          | Searches articles by keyword           |
| `/blogs-by-source`       | Shows top sources by article count     |
| `/most-common-tags`      | Most frequent tags across all articles |
| `/category-count`        | Distribution of articles by category   |
| `/trending-tags?period=` | Trending tags this week/month/year     |

---

## 🤖 Models Used

* [`BAAI/bge-base-en-v1.5`](https://huggingface.co/BAAI/bge-base-en-v1.5) for deep sentence embeddings
* [`KeyBERT`](https://github.com/MaartenGr/KeyBERT) for tag extraction
* Cosine similarity for category classification & recommendations

---

## 🧪 Testing

```bash
curl http://localhost:8000/recommend?title=How+we+scaled+our+API
curl http://localhost:8000/search?q=GraphQL
curl http://localhost:8000/trending-tags?period=month
```

---

## 📦 Roadmap Ideas

* [ ] Full-content scraping for deeper semantic understanding
* [ ] User profiles + personalized suggestions
* [ ] Weekly newsletter with trending blog posts
* [ ] Frontend dashboard (Streamlit or React)
* [ ] Embedding index optimization (FAISS or HNSW)

---

## 📚 Data Sources

* [Netflix Tech Blog](https://netflixtechblog.com/)
* [Airbnb Engineering](https://medium.com/airbnb-engineering)
* [Uber Engineering](https://www.uber.com/blog/engineering/)

---

## 🧑‍💻 Author

Built with 💻 and ☕ by **Arijit Chowdhury**
