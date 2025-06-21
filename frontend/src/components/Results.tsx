import React from 'react'
import styles from '../styles/Results.module.css'
import { ResultItem } from '../App'
import { motion } from 'framer-motion'
import { formatDistanceToNow, format } from 'date-fns'
import Skeleton from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'


interface Props {
  results: ResultItem[]
  loading: boolean
  error: string | null
}

const Results: React.FC<Props> = ({ results, loading, error }) => {
  const formatDate = (isoDate?: string) => {
    if (!isoDate || isoDate == "None") return ''
    try {
      const date = new Date(isoDate)
      const diff = Date.now() - date.getTime()

      // If newer than ~1.5 months, show "3 days ago"
      if (diff < 45 * 24 * 60 * 60 * 1000) {
        return `${formatDistanceToNow(date)} ago`
      }

      // Else fallback to something short and readable
      return format(date, 'MMM yyyy')
    } catch {
      return ''
    }
  }

  if (loading) {
    return (
      <div className={styles.loading}>
        <div className={styles.spinner}></div>
        <div>Loading...</div>
      </div>
    )
  }

  if (error) {
    return <div className={styles.error}>{error}</div>
  }

  if (!results.length) return null

  return (
    <div className={styles.results}>
      {results.map((result, index) => (
        <motion.a
          key={index}
          href={result.url || '#'}
          target="_blank"
          rel="noopener noreferrer"
          className={styles.resultItem}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.05, duration: 0.4, ease: 'easeOut' }}
        >
          <div className={styles.resultTitle}>{result.title}</div>
          <div className={styles.resultSource}>{result.source}</div>

          {result.category && (
            <div className={styles.resultCategory}>{result.category}</div>
          )}

          {result.tags && (
            <div className={styles.resultTags}>
              {String(result.tags)
                .split(',')
                .map((tag, i) => (
                  <span className={styles.tag} key={i}>
                    {tag.trim()}
                  </span>
                ))}
            </div>
          )}

          {result.published_date && (
            <div className={styles.resultDate}>{formatDate(result.published_date)}</div>
          )}

          <div className={styles.resultSummary}>{result.summary}</div>
        </motion.a>
      ))}
    </div>
  )
}

export default Results
