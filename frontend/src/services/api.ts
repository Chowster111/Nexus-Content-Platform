import axios from 'axios'
import { ResultItem } from '../App'

const API_BASE = '/api'
export interface SourceAnalytics {
  sources: [string, number][]
}

export interface CategoryAnalytics {
  categories: [string, number][]
}
export async function searchArticles(query: string): Promise<ResultItem[]> {
  const res = await axios.get(`${API_BASE}/search/articles`, {
    params: { q: query },
  })
  return res.data.results || []
}

export async function recommendArticles(query: string, userId?: string): Promise<ResultItem[]> {
  const params: Record<string, string> = { query, top_k: '5' }
  if (userId) params.user_id = userId

  const res = await axios.get(`${API_BASE}/find/recommend`, {
    params,
  })
  return res.data || []
}


export async function fetchSourceAnalytics(limit = 5): Promise<[string, number][]> {
  const res = await axios.get(`${API_BASE}/analytics/blogs-by-source/${limit}`)
  return res.data.sources || []
}

export async function fetchCategoryAnalytics(): Promise<[string, number][]> {
  const res = await axios.get(`${API_BASE}/analytics/category-count`)
  return res.data.categories || []
}
