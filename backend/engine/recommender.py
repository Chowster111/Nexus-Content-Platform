from sentence_transformers import SentenceTransformer, util
from db.supabase_client import supabase
import torch

# Load the model (high-performing for retrieval)
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

# Automatically choose GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)


def fetch_articles_with_embeddings():
    print("🧪 Fetching articles with embeddings...")

    result = (
        supabase
        .table("articles")
        .select("*")
        .execute()
    )

    raw_articles = result.data or []
    print(f"📦 Total fetched: {len(raw_articles)}")

    valid_articles = []
    for article in raw_articles:
        embedding = article.get("embedding")
        if isinstance(embedding, list) and all(isinstance(x, (float, int)) for x in embedding):
            valid_articles.append(article)

    print(f"✅ Valid articles: {len(valid_articles)}")
    return valid_articles




def get_combined_embedding(text: str):
    # Normalize the query embedding and move it to the correct device
    embedding = model.encode(text, convert_to_tensor=True)
    embedding = embedding.to(device)
    return embedding / embedding.norm(p=2)


def recommend_articles(query: str, top_k: int = 5):
    print(f"📥 Incoming query: {query}")
    articles = fetch_articles_with_embeddings()
    if not articles:
        print("⚠️ No articles with embeddings found.")
        return []

    query_embedding = get_combined_embedding(query)

    similarities = []
    for article in articles:
        try:
            # Convert and normalize article embedding
            embedding_tensor = torch.tensor(article["embedding"], device=device)
            embedding_tensor = embedding_tensor / embedding_tensor.norm(p=2)

            score = util.cos_sim(query_embedding, embedding_tensor).item()
            similarities.append((score, article))
        except Exception as e:
            print(f"❌ Skipping article due to error: {e}")
            continue

    # Sort articles by similarity score (highest first)
    similarities.sort(reverse=True, key=lambda x: x[0])
    top_results = [
        {
            "title": article["title"],
            "url": article["url"],
            "published_date": article["published_date"],
            "content": article.get("content", ""),
            "source": article.get("source", ""),
            "tags": article.get("tags", []),
            "category": article.get("category", ""),
        }
        for _, article in similarities[:top_k]
    ]

    print(f"✅ Top {top_k} recommendations ready.")
    return top_results
