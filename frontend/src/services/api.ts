import axios from 'axios'
import * as Sentry from '@sentry/react'
import { ResultItem } from '../pages/Home'

const API_BASE = '/api'

export interface SourceAnalytics {
  sources: [string, number][]
}

export interface CategoryAnalytics {
  categories: [string, number][]
}

export async function searchArticles(query: string): Promise<ResultItem[]> {
  try {
    const res = await axios.get(`${API_BASE}/search/articles`, {
      params: { q: query },
    })
    return res.data.results || []
  } catch (error) {
    console.error('❌ Error in searchArticles:', error)
    Sentry.captureException(error)
    throw error
  }
}

export async function recommendArticles(query: string, userId?: string): Promise<ResultItem[]> {
  try {
    const params: Record<string, string> = { query, top_k: '5' }
    if (userId) params.user_id = userId

    const res = await axios.get(`${API_BASE}/find/recommend`, {
      params,
    })
    return res.data || []
  } catch (error) {
    console.error('❌ Error in recommendArticles:', error)
    Sentry.captureException(error)
    throw error
  }
}

export async function fetchSourceAnalytics(limit = 5): Promise<[string, number][]> {
  try {
    const res = await axios.get(`${API_BASE}/analytics/blogs-by-source/${limit}`)
    return res.data.sources || []
  } catch (error) {
    console.error('❌ Error in fetchSourceAnalytics:', error)
    Sentry.captureException(error)
    throw error
  }
}

export async function fetchCategoryAnalytics(): Promise<[string, number][]> {
  try {
    const res = await axios.get(`${API_BASE}/analytics/category-count`)
    return res.data.categories || []
  } catch (error) {
    console.error('❌ Error in fetchCategoryAnalytics:', error)
    Sentry.captureException(error)
    throw error
  }
}
