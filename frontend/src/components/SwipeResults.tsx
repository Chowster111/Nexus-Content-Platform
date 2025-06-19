// src/components/SwipeResults.tsx
import React, { useState } from 'react'
import styles from '../styles/SwipeResults.module.css'
import { ResultItem } from '../App'
import { motion, AnimatePresence } from 'framer-motion'
import { formatDistanceToNow, format } from 'date-fns'

interface Props {
  results: ResultItem[]
}

const SwipeResults: React.FC<Props> = ({ results }) => {
  const [index, setIndex] = useState(0)

  const handleSwipe = () => {
    if (index < results.length - 1) {
      setIndex(index + 1)
    } else {
      setIndex(results.length) // done
    }
  }

  const formatDate = (isoDate?: string) => {
    if (!isoDate) return ''
    const date = new Date(isoDate)
    const diff = Date.now() - date.getTime()
    return diff < 45 * 24 * 60 * 60 * 1000
      ? `${formatDistanceToNow(date)} ago`
      : format(date, 'MMM yyyy')
  }

  if (!results.length) return null
  if (index >= results.length) return <div className={styles.done}>🎉 You’ve seen all articles!</div>

  const result = results[index]

  return (
    <div className={styles.swipeWrapper}>
      <AnimatePresence>
        <motion.div
          key={index}
          className={styles.card}
          initial={{ x: 300, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          exit={{ x: -300, opacity: 0 }}
          transition={{ duration: 0.3 }}
          drag="x"
          dragConstraints={{ left: 0, right: 0 }}
          dragElastic={0.6}
          onDragEnd={(event, info) => {
            if (Math.abs(info.offset.x) > 100) {
              handleSwipe()
            }
          }}
        >
          <a href={result.url || '#'} target="_blank" rel="noopener noreferrer" className={styles.link}>
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
          </a>

          <div className={styles.buttons}>
            <button disabled className={styles.dislike}>👎</button>
            <button disabled className={styles.like}>👍</button>
          </div>
        </motion.div>
      </AnimatePresence>
    </div>
  )
}

export default SwipeResults
