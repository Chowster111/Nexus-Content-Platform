import { ResultItem } from '../App'

export const mockSearchResults = (query: string): ResultItem[] => [
  {
    title: `Results for "${query}"`,
    source: 'Web Search',
    tags: 'search, web, information',
    summary: `Here are some relevant results for your search query about ${query}.`,
  },
  {
    title: 'Related Information',
    source: 'Knowledge Base',
    tags: 'knowledge, reference',
    summary: 'Additional context and related information that might be helpful.',
  },
]

export const mockRecommendations = (topic: string): ResultItem[] => [
  {
    title: `Recommendations for "${topic}"`,
    source: 'AI Recommendations',
    tags: 'recommendations, ai, curated',
    summary: `Based on your topic "${topic}", here are some curated recommendations.`,
  },
  {
    title: 'Similar Topics',
    source: 'Content Database',
    tags: 'similar, related, topics',
    summary: 'Other users have found these related topics useful.',
  },
]
