import axios from 'axios'
import { ResultItem } from '../App'

const API_BASE = 'http://localhost:8000' // backend base

export async function searchArticles(query: string): Promise<ResultItem[]> {
  const res = await axios.get(`${API_BASE}/search/articles`, {
    params: { q: query }
  })
  return res.data.results || [] // your backend returns `{ results: [...] }`
}

export async function recommendArticles(query: string): Promise<ResultItem[]> {
  const res = await axios.get(`${API_BASE}/find/recommend`, {
    params: { query, top_k: 5 }
  })
  return res.data || [] // your backend returns the list directly
}
