import torch
from sentence_transformers import SentenceTransformer, util

from db.supabase_client import supabase
from pydantic import ValidationError
from models.article import ArticleResponse

model = SentenceTransformer("BAAI/bge-base-en-v1.5")
device = torch.device("cpu")
model = model.to(device)


def fetch_articles_with_embeddings():
    result = (
        supabase
        .table("articles")
        .select("*")
        .order("published_date", desc=True)
        .execute()
    )
    raw_articles = result.data or []
    print(f"📦 Total fetched: {len(raw_articles)}")

    valid_articles = []
    errors = []
    for article in raw_articles:
        embedding = article.get("embedding")
        if isinstance(embedding, list) and all(isinstance(x, (float, int)) for x in embedding):
            try:
                # Validate as ArticleResponse for structure
                ArticleResponse(**article)
                valid_articles.append(article)
            except ValidationError as ve:
                print(f"❌ Validation error for article: {article} | {ve}")
                errors.append({"article": article, "error": str(ve)})
    if errors:
        print(f"⚠️ Some articles failed validation: {errors}")
    print(f"✅ Valid articles: {len(valid_articles)}")
    return valid_articles


def get_combined_embedding(text: str):
    embedding = model.encode(text, convert_to_tensor=True)
    embedding = embedding.to(device)
    return embedding / embedding.norm(p=2)


def fetch_liked_article_urls(user_id: str):
    result = (
        supabase
        .table("likes")
        .select("article_url, liked")
        .eq("user_id", user_id)
        .execute()
    )
    return [entry["article_url"] for entry in result.data or [] if entry.get("liked")]


def extract_tags_from_articles(articles, urls: list[str]):
    tag_set = set()
    for article in articles:
        if article["url"] in urls:
            tags = article.get("tags", [])
            if isinstance(tags, str):
                tags = tags.split(",")
            for tag in tags:
                tag_set.add(tag.strip())
    return list(tag_set)


def recommend_articles(query: str, top_k: int = 5, user_id: str = None):
    articles = fetch_articles_with_embeddings()
    if not articles:
        print("⚠️ No articles with embeddings found.")
        return []

    if user_id:
        liked_urls = fetch_liked_article_urls(user_id)
        liked_tags = extract_tags_from_articles(articles, liked_urls)
        if liked_tags:
            query = " ".join(liked_tags[:10])
            print(f"🧠 Personalized query: {query}")
        else:
            print("ℹ️ No liked tags found, falling back to original query.")

    query_embedding = get_combined_embedding(query)
    similarities = []

    for article in articles:
        try:
            emb_tensor = torch.tensor(article["embedding"], device=device)
            emb_tensor = emb_tensor / emb_tensor.norm(p=2)
            score = util.cos_sim(query_embedding, emb_tensor).item()
            similarities.append((score, article))
        except Exception as e:
            print(f"❌ Skipping article due to error: {e}")

    similarities.sort(reverse=True, key=lambda x: x[0])
    results = []
    errors = []
    for _, a in similarities[:top_k]:
        try:
            # Validate output structure
            results.append({
            "title": a["title"],
            "url": a["url"],
            "published_date": a["published_date"],
            "source": a.get("source", ""),
            "tags": a.get("tags", []),
            "category": a.get("category", ""),
            "summary": a.get("summary", ""),
            })
            ArticleResponse(**results[-1])
        except ValidationError as ve:
            print(f"❌ Validation error for recommended article: {a} | {ve}")
            errors.append({"article": a, "error": str(ve)})
    if errors:
        print(f"⚠️ Some recommended articles failed validation: {errors}")
    return results
