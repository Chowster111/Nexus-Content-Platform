# Engineering Blog Recommender API Documentation

## Overview

The Engineering Blog Recommender API is a modern, AI-powered REST API for discovering and recommending high-quality engineering articles from top tech companies. Built with FastAPI, it provides semantic search, personalized recommendations, and comprehensive article management capabilities.


## Authentication

Most endpoints require authentication using Supabase Auth. Include your access token in the Authorization header:

```
Authorization: Bearer <your-access-token>
```

### Getting an Access Token

1. **Sign Up**: `POST /auth/signup`
2. **Sign In**: `POST /auth/signin`

## Rate Limiting

- **Search**: 100 requests/minute
- **Recommendations**: 50 requests/minute  
- **Articles**: 200 requests/minute
- **Scraping**: 10 requests/minute (admin only)
- **Analytics**: 30 requests/minute

## Error Handling

All endpoints return consistent error responses:

```json
{
  "error": "Error message",
  "status_code": 400,
  "details": "Additional error context"
}
```

### Common HTTP Status Codes

- `200` - Success
- `400` - Bad Request (invalid parameters)
- `401` - Unauthorized (missing/invalid token)
- `404` - Not Found
- `429` - Rate Limited
- `500` - Internal Server Error

---

## Endpoints

### 🔍 Search

#### GET /search/articles

Search articles using semantic similarity with BGE embeddings.

**Parameters:**
- `q` (string, required): Search query (1-500 characters)

**Example Request:**
```bash
curl -X GET "https://api.engineeringblogrecommender.com/search/articles?q=machine%20learning%20deployment" \
  -H "Authorization: Bearer <token>"
```

**Example Response:**
```json
{
  "results": [
    {
      "title": "Deploying Machine Learning Models at Scale",
      "url": "https://netflix.com/tech-blog/ml-deployment",
      "published_date": "2024-01-15",
      "content": "How Netflix deploys ML models in production...",
      "source": "netflix",
      "tags": ["machine-learning", "deployment", "scalability"],
      "category": "Machine Learning",
      "summary": "A comprehensive guide to deploying ML models..."
    }
  ],
  "error": null
}
```

**Features:**
- Semantic similarity using BGE embeddings
- Automatic ranking by relevance score
- Support for natural language queries
- Returns top 10 most relevant articles

---

### 🎯 Recommendations

#### GET /find/recommend

Get personalized article recommendations based on query and user preferences.

**Parameters:**
- `query` (string, optional): Natural language query for recommendations
- `top_k` (integer, optional): Number of recommendations (1-50, default: 5)
- `user_id` (string, optional): User ID for personalization

**Example Request:**
```bash
curl -X GET "https://api.engineeringblogrecommender.com/find/recommend?query=scalable%20architecture&top_k=10&user_id=user123" \
  -H "Authorization: Bearer <token>"
```

**Example Response:**
```json
{
  "articles": [
    {
      "title": "Building Scalable Microservices",
      "url": "https://netflix.com/tech-blog/scalable-microservices",
      "published_date": "2024-01-15",
      "source": "netflix",
      "category": "Architecture",
      "tags": ["microservices", "scalability", "architecture"],
      "summary": "How Netflix built their scalable microservices architecture...",
      "similarity_score": 0.92
    }
  ],
  "error": null
}
```

**Features:**
- AI-powered recommendations using semantic similarity
- User preference learning from likes/dislikes
- Content-based and collaborative filtering
- Diversity boost for varied suggestions

---

### 📰 Articles

#### GET /articles/

Retrieve all articles with comprehensive metadata.

**Example Request:**
```bash
curl -X GET "https://api.engineeringblogrecommender.com/articles/" \
  -H "Authorization: Bearer <token>"
```

**Example Response:**
```json
[
  {
    "id": "article-123",
    "title": "Building Scalable Microservices",
    "url": "https://netflix.com/tech-blog/scalable-microservices",
    "published_date": "2024-01-15",
    "content": "Full article content...",
    "source": "netflix",
    "category": "Architecture",
    "tags": ["microservices", "scalability", "architecture"],
    "summary": "How Netflix built their scalable microservices architecture..."
  }
]
```

#### GET /articles/tags/{tag}

Get articles filtered by a specific tag.

**Parameters:**
- `tag` (path): Tag to filter by
- `sort` (query, optional): Sort order ("latest" or "oldest", default: "latest")

**Example Request:**
```bash
curl -X GET "https://api.engineeringblogrecommender.com/articles/tags/machine-learning?sort=latest" \
  -H "Authorization: Bearer <token>"
```

#### GET /articles/filter

Filter articles by multiple tags.

**Parameters:**
- `tags` (query, required): List of tags to filter by
- `sort` (query, optional): Sort order ("latest" or "oldest", default: "latest")

**Example Request:**
```bash
curl -X GET "https://api.engineeringblogrecommender.com/articles/filter?tags=machine-learning&tags=python&sort=latest" \
  -H "Authorization: Bearer <token>"
```

#### GET /articles/all-tags

Get all available tags with usage counts.

**Example Request:**
```bash
curl -X GET "https://api.engineeringblogrecommender.com/articles/all-tags" \
  -H "Authorization: Bearer <token>"
```

**Example Response:**
```json
[
  {"tag": "machine-learning", "count": 45},
  {"tag": "python", "count": 32},
  {"tag": "architecture", "count": 28}
]
```

#### GET /articles/by-category/{category}

Get articles by category.

**Parameters:**
- `category` (path): Category to filter by
- `sort` (query, optional): Sort order ("latest" or "oldest", default: "latest")

**Available Categories:**
- Architecture
- Machine Learning
- Frontend
- Backend
- DevOps
- Database
- Security
- Performance
- Testing
- Mobile

**Example Request:**
```bash
curl -X GET "https://api.engineeringblogrecommender.com/articles/by-category/architecture?sort=latest" \
  -H "Authorization: Bearer <token>"
```

#### GET /articles/by-source/{source}

Get articles by source.

**Parameters:**
- `source` (path): Source to filter by
- `sort` (query, optional): Sort order ("latest" or "oldest", default: "latest")

**Available Sources:**
- netflix: Netflix Engineering Blog
- airbnb: Airbnb Engineering & Data Science
- uber: Uber Engineering
- stripe: Stripe Engineering
- tinder: Tinder Engineering
- doordash: DoorDash Engineering
- slack: Slack Engineering
- notion: Notion Engineering
- meta: Meta Engineering
- robinhood: Robinhood Engineering

**Example Request:**
```bash
curl -X GET "https://api.engineeringblogrecommender.com/articles/by-source/netflix?sort=latest" \
  -H "Authorization: Bearer <token>"
```

#### GET /articles/{article_id}

Get a single article by ID.

**Parameters:**
- `article_id` (path): Unique article identifier

**Example Request:**
```bash
curl -X GET "https://api.engineeringblogrecommender.com/articles/article-123" \
  -H "Authorization: Bearer <token>"
```

---

### 🔐 Authentication

#### POST /auth/signup

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Example Request:**
```bash
curl -X POST "https://api.engineeringblogrecommender.com/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepassword123"}'
```

**Example Response:**
```json
{
  "user": {
    "id": "user-123",
    "email": "user@example.com"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### POST /auth/signin

Sign in with existing credentials.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Example Request:**
```bash
curl -X POST "https://api.engineeringblogrecommender.com/auth/signin" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepassword123"}'
```

---

### 👤 User Preferences

#### POST /user/likes

Save user likes and dislikes for articles to enable personalized recommendations.

**Request Body:**
```json
{
  "user_id": "user-123",
  "likes": [
    {
      "article_id": "article-456",
      "url": "https://netflix.com/tech-blog/article",
      "liked": true
    },
    {
      "article_id": "article-789",
      "url": "https://airbnb.com/engineering/article",
      "liked": false
    }
  ]
}
```

**Example Request:**
```bash
curl -X POST "https://api.engineeringblogrecommender.com/user/likes" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-123",
    "likes": [
      {
        "article_id": "article-456",
        "url": "https://netflix.com/tech-blog/article",
        "liked": true
      }
    ]
  }'
```

**Example Response:**
```json
{
  "message": "1 likes saved",
  "liked": true
}
```

**Features:**
- Batch like/dislike saving for multiple articles
- User preference learning for recommendations
- Validation of article data before saving
- Error handling for invalid data
- Real-time preference updates

#### GET /user/likes

Get user's liked articles.

**Example Request:**
```bash
curl -X GET "https://api.engineeringblogrecommender.com/user/likes" \
  -H "Authorization: Bearer <token>"
```

**Example Response:**
```json
{
  "likes": [
    {
      "article_id": "article-123",
      "liked": true,
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ]
}
```

---

### 📊 Analytics

#### GET /analytics/popular-articles

Get most popular articles by engagement.

**Parameters:**
- `limit` (query, optional): Number of articles to return (default: 10)

**Example Request:**
```bash
curl -X GET "https://api.engineeringblogrecommender.com/analytics/popular-articles?limit=20" \
  -H "Authorization: Bearer <token>"
```

**Example Response:**
```json
{
  "articles": [
    {
      "article_id": "article-123",
      "title": "Building Scalable Microservices",
      "likes_count": 150,
      "views_count": 2500,
      "engagement_rate": 0.06
    }
  ]
}
```

#### GET /analytics/source-stats

Get analytics by source.

**Example Request:**
```bash
curl -X GET "https://api.engineeringblogrecommender.com/analytics/source-stats" \
  -H "Authorization: Bearer <token>"
```

**Example Response:**
```json
{
  "sources": [
    {
      "source": "netflix",
      "article_count": 45,
      "total_likes": 1200,
      "avg_engagement": 0.08
    }
  ]
}
```

#### GET /analytics/category-stats

Get analytics by category.

**Example Request:**
```bash
curl -X GET "https://api.engineeringblogrecommender.com/analytics/category-stats" \
  -H "Authorization: Bearer <token>"
```

**Example Response:**
```json
{
  "categories": [
    {
      "category": "Architecture",
      "article_count": 32,
      "total_likes": 850,
      "avg_engagement": 0.07
    }
  ]
}
```

---

### 🕷️ Scraping (Admin Only)

#### POST /scrape/select/{source}

Trigger scraping for a specific engineering blog source.

**Parameters:**
- `source` (path): Source to scrape (netflix, airbnb, uber, stripe, etc.)

**Supported Sources:**
- netflix: Netflix Engineering Blog
- airbnb: Airbnb Engineering & Data Science
- uber: Uber Engineering
- stripe: Stripe Engineering
- tinder: Tinder Engineering
- doordash: DoorDash Engineering
- slack: Slack Engineering
- notion: Notion Engineering
- meta: Meta Engineering
- robinhood: Robinhood Engineering

**Example Request:**
```bash
curl -X POST "https://api.engineeringblogrecommender.com/scrape/select/netflix" \
  -H "Authorization: Bearer <admin-token>"
```

**Example Response:**
```json
{
  "source": "netflix",
  "success": true,
  "articles_count": 15,
  "articles": [
    {
      "title": "Building Scalable Microservices",
      "url": "https://netflix.com/tech-blog/scalable-microservices",
      "published_date": "2024-01-15",
      "content": "How Netflix built their scalable microservices architecture...",
      "source": "netflix",
      "category": "Architecture",
      "tags": ["microservices", "scalability", "architecture"],
      "summary": "A comprehensive guide to building scalable microservices..."
    }
  ],
  "error": null
}
```

**Features:**
- Real-time content scraping from live blogs
- Automatic tag extraction using AI
- Semantic embedding generation
- Duplicate article detection
- Error handling and retry logic
- Progress tracking and status reporting

#### POST /scrape/all

Trigger scraping for all supported engineering blog sources.

**Example Request:**
```bash
curl -X POST "https://api.engineeringblogrecommender.com/scrape/all" \
  -H "Authorization: Bearer <admin-token>"
```

**Example Response:**
```json
{
  "netflix": {
    "source": "netflix",
    "success": true,
    "articles_count": 15,
    "articles": [...],
    "error": null
  },
  "airbnb": {
    "source": "airbnb",
    "success": true,
    "articles_count": 12,
    "articles": [...],
    "error": null
  },
  "uber": {
    "source": "uber",
    "success": false,
    "articles_count": 0,
    "articles": [],
    "error": "Connection timeout"
  }
}
```

**Features:**
- Parallel processing of multiple sources
- Error isolation (individual source failures don't affect others)
- Progress tracking for each source
- Resource management for large-scale operations
- Real-time status updates and monitoring

---

### 🏥 Health

#### GET /health

Get system health status.

**Example Request:**
```bash
curl -X GET "https://api.engineeringblogrecommender.com/health"
```

**Example Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "database": {
    "status": "connected",
    "latency_ms": 15
  },
  "embeddings": {
    "status": "available",
    "model": "BAAI/bge-small-en-v1.5"
  },
  "version": "1.0.0"
}
```

#### GET /metrics

Get Prometheus metrics for monitoring.

**Example Request:**
```bash
curl -X GET "https://api.engineeringblogrecommender.com/metrics"
```

---

## Data Models

### Article Response

```json
{
  "id": "string",
  "title": "string",
  "url": "string",
  "published_date": "date",
  "content": "string",
  "source": "string",
  "category": "string",
  "tags": ["string"],
  "summary": "string"
}
```

### Search Result

```json
{
  "title": "string",
  "url": "string",
  "published_date": "date",
  "content": "string",
  "source": "string",
  "tags": ["string"],
  "category": "string",
  "summary": "string"
}
```

### Recommendation Response

```json
{
  "articles": [
    {
      "title": "string",
      "url": "string",
      "published_date": "date",
      "source": "string",
      "category": "string",
      "tags": ["string"],
      "summary": "string",
      "similarity_score": "float"
    }
  ],
  "error": "string|null"
}
```

### Tag Count

```json
{
  "tag": "string",
  "count": "integer"
}
```

---

## SDKs and Libraries

### Python

```python
import requests

# Search articles
response = requests.get(
    "https://api.engineeringblogrecommender.com/search/articles",
    params={"q": "machine learning deployment"},
    headers={"Authorization": "Bearer <token>"}
)

# Get recommendations
response = requests.get(
    "https://api.engineeringblogrecommender.com/find/recommend",
    params={"query": "scalable architecture", "top_k": 10},
    headers={"Authorization": "Bearer <token>"}
)
```

### JavaScript/TypeScript

```javascript
// Search articles
const response = await fetch(
  'https://api.engineeringblogrecommender.com/search/articles?q=machine%20learning%20deployment',
  {
    headers: {
      'Authorization': 'Bearer <token>'
    }
  }
);

// Get recommendations
const response = await fetch(
  'https://api.engineeringblogrecommender.com/find/recommend?query=scalable%20architecture&top_k=10',
  {
    headers: {
      'Authorization': 'Bearer <token>'
    }
  }
);
```

### cURL

```bash
# Search articles
curl -X GET "https://api.engineeringblogrecommender.com/search/articles?q=machine%20learning%20deployment" \
  -H "Authorization: Bearer <token>"

# Get recommendations
curl -X GET "https://api.engineeringblogrecommender.com/find/recommend?query=scalable%20architecture&top_k=10" \
  -H "Authorization: Bearer <token>"
```

---

## Best Practices

### Authentication
- Always include the Authorization header with your access token
- Store tokens securely and refresh them before expiration
- Use HTTPS for all API calls

### Rate Limiting
- Implement exponential backoff for retries
- Monitor rate limit headers in responses
- Cache responses when appropriate

### Error Handling
- Check HTTP status codes for all responses
- Handle network errors gracefully
- Log errors for debugging

### Performance
- Use pagination for large result sets
- Cache frequently accessed data
- Minimize API calls by batching requests

---

## Support

- **Documentation**: Visit `/docs` for interactive API documentation
- **Issues**: Report bugs and feature requests on GitHub
- **Email**: api@engineeringblogrecommender.com
- **Status**: Check system status at `/health`

---

## Changelog

### v1.0.0 (2024-01-15)
- Initial API release
- Semantic search with BGE embeddings
- Personalized recommendations
- Comprehensive article management
- User authentication and preferences
- Analytics and health monitoring 