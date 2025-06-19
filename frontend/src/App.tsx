import React, { useState } from 'react'
import styles from './styles/App.module.css'

import ThreeScene from './components/ThreeScene'
import Header from './components/Header'
import ToggleSwitch from './components/ToggleSwitch'
import SearchSection from './components/SearchSection'
import RecommendSection from './components/RecommendSection'
import Results from './components/Results'

import { searchArticles, recommendArticles } from './services/api'

export type Tab = 'search' | 'recommend'

export interface ResultItem {
  title: string
  source: string
  tags: string[] | string
  category?: string
  summary: string
  url?: string
  published_date?: string
}

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('search')

  // Cache results per tab
  const [searchResults, setSearchResults] = useState<ResultItem[]>([])
  const [recommendResults, setRecommendResults] = useState<ResultItem[]>([])
  const results = activeTab === 'search' ? searchResults : recommendResults

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSearch = async (query: string) => {
    if (!query.trim()) return
    setLoading(true)
    setError(null)
    setSearchResults([])

    try {
      const data = await searchArticles(query)
      const mapped: ResultItem[] = data.slice(0, 5).map((item) => ({
        title: item.title,
        source: item.source || 'Unknown',
        tags: Array.isArray(item.tags) ? item.tags.join(', ') : item.tags || '',
        category: item.category || 'General',
        summary: 'Expand to read more',
        url: item.url || '#',
        published_date: item.published_date || '',
      }))
      setSearchResults(mapped)
    } catch (err) {
      console.error(err)
      setError('Failed to load search results.')
    } finally {
      setLoading(false)
    }
  }

  const handleRecommend = async (query: string) => {
    if (!query.trim()) return
    setLoading(true)
    setError(null)
    setRecommendResults([])

    try {
      const data = await recommendArticles(query)
      const mapped: ResultItem[] = data.slice(0, 5).map((item) => ({
        title: item.title,
        source: item.source || 'Unknown',
        tags: Array.isArray(item.tags) ? item.tags.join(', ') : item.tags || '',
        category: item.category || 'General',
        summary: 'Expand to read more',
        url: item.url || '#',
        published_date: item.published_date || '',
      }))
      setRecommendResults(mapped)
    } catch (err) {
      console.error(err)
      setError('Failed to load recommendations.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.app}>
      <ThreeScene />

      <div className={styles.container}>
        <Header />
        <ToggleSwitch activeTab={activeTab} onChange={setActiveTab} />

        <div className={styles.content}>
          {activeTab === 'search' ? (
            <SearchSection onSearch={handleSearch} />
          ) : (
            <RecommendSection onRecommend={handleRecommend} />
          )}

          <Results results={results} loading={loading} error={error} />
        </div>
      </div>
    </div>
  )
}

export default App
