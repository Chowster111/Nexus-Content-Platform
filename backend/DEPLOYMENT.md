# Deployment Guide - Engineering Blog Recommender

This guide covers deployment considerations for the Engineering Blog Recommender backend, with specific focus on type validation and error handling in production environments.

## Runtime Validation in Production

### Validation Strategy

The backend implements comprehensive runtime validation that becomes especially important in production:

- **Data Integrity**: Validates all data from external sources (scrapers, APIs, databases)
- **Error Isolation**: Prevents single bad data point from crashing entire API
- **Debugging Support**: Detailed error logs help identify data quality issues
- **Graceful Degradation**: Returns partial results when some data is invalid

### Production Monitoring

#### Validation Error Metrics

Monitor these metrics in production:

```bash
# Check validation error rates
grep "Validation error" /var/log/app.log | wc -l

# Monitor specific validation failures
grep "Validation error for article" /var/log/app.log

# Track scraper validation issues
grep "Validation error for scraped article" /var/log/app.log
```

#### Alerting Thresholds

Set up alerts for:
- Validation error rate > 5% of total requests
- Scraper validation failures > 10% of scraped articles
- Database validation errors > 1% of queries

### Error Handling Best Practices

#### 1. Logging Strategy

```python
# Good: Detailed error context
logger.error(f"Validation error for article: {article} | {ve}")

# Better: Include request context
logger.error(f"Validation error for article in request {request_id}: {article} | {ve}")
```

#### 2. Error Response Format

All API endpoints return consistent error formats:

```json
{
  "articles": [...],
  "error": "3 articles failed validation"
}
```

#### 3. Partial Success Handling

When some items fail validation:
- Log the errors with context
- Return valid items
- Include error count in response
- Don't fail the entire request

### Database Considerations

#### Data Quality Monitoring

```sql
-- Check for articles with missing required fields
SELECT COUNT(*) FROM articles WHERE title IS NULL OR url IS NULL;

-- Find articles with invalid tag formats
SELECT * FROM articles WHERE tags IS NOT NULL AND jsonb_typeof(tags) != 'array';

-- Monitor embedding quality
SELECT COUNT(*) FROM articles WHERE embedding IS NULL OR array_length(embedding, 1) != 768;
```

#### Migration Safety

When updating models:
1. Add new fields as optional first
2. Validate existing data before making fields required
3. Use database constraints for critical fields
4. Monitor validation errors during migrations

### Scraper Error Handling

#### Validation Pipeline

```python
# Each scraped article goes through validation
try:
    ScrapedArticle(**article_data)
    # Proceed with database insertion
except ValidationError as ve:
    logger.error(f"Scraped article validation failed: {ve}")
    # Skip invalid article, continue scraping
```

#### Scraper Monitoring

Monitor scraper health:
- Validation success rate per source
- Articles skipped due to validation errors
- Embedding generation failures
- Database insertion errors

### Performance Considerations

#### Validation Overhead

- Pydantic validation: ~0.1-1ms per model
- Embedding validation: ~0.5ms per vector
- Total validation overhead: <5% of request time

#### Optimization Strategies

1. **Lazy Validation**: Only validate when needed
2. **Caching**: Cache validated models when possible
3. **Batch Processing**: Validate in batches for bulk operations
4. **Async Validation**: Use async validation for I/O bound operations

### Troubleshooting Guide

#### Common Validation Errors

1. **Missing Required Fields**
   ```
   ValidationError: 1 validation error for ArticleResponse
   title: field required
   ```

2. **Type Mismatches**
   ```
   ValidationError: 1 validation error for ArticleResponse
   tags: value is not a valid list
   ```

3. **Embedding Issues**
   ```
   ValidationError: 1 validation error for Article
   embedding: value is not a valid list
   ```

#### Debugging Steps

1. Check the raw data causing validation errors
2. Verify database schema matches model expectations
3. Review scraper output for data quality issues
4. Monitor embedding generation process
5. Check for data type conversions in database queries

### Health Check Integration

The health check endpoint validates its own response:

```python
# Health check validates response structure
try:
    HealthCheckResponse(**result)
except ValidationError as ve:
    logger.error(f"Health check validation failed: {ve}")
    raise HTTPException(status_code=500, detail="Health check validation error")
```

### Production Checklist

- [ ] Monitor validation error rates
- [ ] Set up alerts for validation failures
- [ ] Review scraper data quality regularly
- [ ] Validate database migrations
- [ ] Test error handling under load
- [ ] Document validation error patterns
- [ ] Set up logging aggregation for validation errors
- [ ] Configure error reporting to monitoring systems

### Monitoring Dashboard

Create a Grafana dashboard with:
- Validation error rate over time
- Error types breakdown (missing fields, type mismatches, etc.)
- Per-endpoint validation success rates
- Scraper validation health
- Database data quality metrics

This comprehensive validation strategy ensures your API remains robust and debuggable in production environments. 