import React, { useState, useRef, useEffect } from 'react'
import styles from './styles/App.module.css'
import { saveUserLikes } from './services/likes'
import ThreeScene from './components/ThreeScene'
import Header from './components/Header'
import ToggleSwitch from './components/ToggleSwitch'
import SearchSection from './components/SearchSection'
import RecommendSection from './components/RecommendSection'
import Results from './components/Results'
import SwipeResults from './components/SwipeResults'
import UserAuth from './components/UserAuth'

import {
  searchArticles,
  recommendArticles,
  fetchCategoryAnalytics,
  fetchSourceAnalytics,
} from './services/api'

import { supabase } from '../lib/supabaseClient'
import type { User } from '@supabase/supabase-js'

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

export interface LikedItem extends ResultItem {
  liked: boolean
}

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('search')
  const [results, setResults] = useState<ResultItem[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [useSwipeMode, setUseSwipeMode] = useState(false)
  const [user, setUser] = useState<User | null>(null)
  const [likes, setLikes] = useState<LikedItem[]>([])
  const [categories, setCats] = useState<[string, number][]>([])
  const [sources, setSources] = useState<[string, number][]>([])

  const handleLike = (item: ResultItem & { liked: boolean }) => {
    setLikes((prev) => [...prev, item])
  }

  const handleSwipeComplete = async () => {
    if (!user) return
    try {
      await saveUserLikes(user.id, likes)
    } catch (err) {
      console.error(err)
    }
  }

  const searchCache = useRef<ResultItem[]>([])
  const recommendCache = useRef<ResultItem[]>([])

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => {
      setUser(data?.session?.user ?? null)
    })

    const { data: listener } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null)
    })

    return () => {
      listener?.subscription.unsubscribe()
    }
  }, [])

useEffect(() => {
  async function loadAnalytics() {
    try {
      console.log('📡 Fetching analytics data...')
      const sourceData = await fetchSourceAnalytics()
      const categoryData = await fetchCategoryAnalytics()
      console.log('✅ Fetched sources:', sourceData)
      console.log('✅ Fetched categories:', categoryData)
      setSources(sourceData)
      setCats(categoryData)
    } catch (e) {
      console.error('❌ Failed to fetch analytics:', e)
    }
  }

  loadAnalytics()
}, [])

  const handleSearch = async (query: string) => {
    if (!query.trim()) return
    setLoading(true)
    setError(null)
    setResults([])

    try {
      const data = await searchArticles(query)
      const mapped: ResultItem[] = data.slice(0, 5).map((item) => ({
        title: item.title,
        source: item.source || 'Unknown',
        tags: Array.isArray(item.tags) ? item.tags.join(', ') : item.tags || '',
        summary: item.summary,
        url: item.url || '#',
        category: item.category || 'General',
        published_date: item.published_date || '',
      }))
      setResults(mapped)
      searchCache.current = mapped
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
    setResults([])

    try {
      const data = await recommendArticles(query)
      const mapped: ResultItem[] = data.slice(0, 10).map((item) => ({
        title: item.title,
        source: item.source || 'Unknown',
        tags: Array.isArray(item.tags) ? item.tags.join(', ') : item.tags || '',
        summary: item.summary,
        url: item.url || '#',
        category: item.category || 'General',
        published_date: item.published_date || '',
      }))
      setResults(mapped)
      recommendCache.current = mapped
    } catch (err) {
      console.error(err)
      setError('Failed to load recommendations.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.app}>
      <UserAuth />
      <ThreeScene />
      <div className={styles.container}>
        <Header />
        <ToggleSwitch
          activeTab={activeTab}
          onChange={(tab) => {
            setActiveTab(tab)
            if (tab === 'search') {
              setResults(searchCache.current)
            } else {
              setResults(recommendCache.current)
            }
          }}
        />

        <div className={styles.content}>
          <div className={styles.toggleWrapper}>
            <span className={styles.toggleLabel}>Swipe Mode</span>
            <div
              className={`${styles.toggle} ${useSwipeMode ? styles.checked : ''}`}
              onClick={() => setUseSwipeMode((prev) => !prev)}
            >
              <div className={styles.thumb} />
            </div>
          </div>

          {activeTab === 'search' ? (
            <SearchSection onSearch={handleSearch} />
          ) : (
            <RecommendSection onRecommend={handleRecommend} />
          )}

          {useSwipeMode ? (
            <SwipeResults
              results={results}
              onLike={handleLike}
              onSwipeComplete={handleSwipeComplete}
              user={user}
            />
          ) : (
            <Results results={results} loading={loading} error={error} />
          )}
        </div>
<div className={styles.analyticsBox}>
  <h2 className={styles.analyticsTitle}>Site Analytics</h2>
  <div className={styles.analyticsRow}>
    <div>
      <h3>Top Sources</h3>
      <table className={styles.analyticsTable}>
        <thead>
          <tr><th>Source</th><th>Articles</th></tr>
        </thead>
        <tbody>
          {sources.map(([source, count]) => (
            <tr key={source}>
              <td>{source}</td>
              <td><strong>{count}</strong></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
    <div>
      <h3>Top Categories</h3>
      <table className={styles.analyticsTable}>
        <thead>
          <tr><th>Category</th><th>Articles</th></tr>
        </thead>
        <tbody>
          {categories.map(([category, count]) => (
            <tr key={category}>
              <td>{category}</td>
              <td><strong>{count}</strong></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
</div>


      </div>
    </div>
  )
}

export default App
