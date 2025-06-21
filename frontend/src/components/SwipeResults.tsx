import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import styles from '../styles/SwipeResults.module.css'
import { ResultItem } from '../App'

interface Props {
  results: ResultItem[]
}

const SwipeResults: React.FC<Props> = ({ results }) => {
  const [index, setIndex] = useState(0)
  const [direction, setDirection] = useState<'left' | 'right'>('right')

  const handleNext = (dir: 'left' | 'right') => {
    setDirection(dir)
    setTimeout(() => {
      setIndex((prev) => prev + 1)
    }, 300)
  }

  const formatDate = (dateStr?: string): string => {
    if (!dateStr || dateStr == "None") return ''
    const date = new Date(dateStr)
    return date.toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
  }

  if (index >= results.length) {
    return <div className={styles.done}></div>
  }

  const item = results[index]

  return (
    <div className={styles.swipeWrapper}>
      <AnimatePresence mode="wait">
        <motion.div
          key={item.title + index}
          className={styles.card}
          initial={{ opacity: 0, x: direction === 'left' ? 100 : -100 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: direction === 'left' ? -100 : 100 }}
          transition={{ duration: 0.3 }}
        >
          <a
            href={item.url || '#'}
            target="_blank"
            rel="noopener noreferrer"
            className={styles.link}
          >
            <div className={styles.resultTitle}>{item.title}</div>
            <div className={styles.resultSource}>{item.source}</div>

            {item.category && (
              <div className={styles.resultCategory}>{item.category}</div>
            )}

            {item.tags && (
              <div className={styles.resultTags}>
                {String(item.tags)
                  .split(',')
                  .map((tag, i) => (
                    <div className={styles.tag} key={i}>
                      {tag.trim()}
                    </div>
                  ))}
              </div>
            )}

            <div className={styles.resultSummary}>
            {(item.summary || '').replace(/^"(.*)"$/, '$1').trim()}
          </div>


            {item.published_date && (
              <div className={styles.resultDateWrapper}>
                <span className={styles.resultDate}>
                  {formatDate(item.published_date)}
                </span>
              </div>
            )}
          </a>

          <div className={styles.buttons}>
            <button
              className={styles.dislike}
              onClick={() => handleNext('left')}
            >
              ✖
            </button>
            <button
              className={styles.like}
              onClick={() => handleNext('right')}
            >
              ✔
            </button>
          </div>
        </motion.div>
      </AnimatePresence>
    </div>
  )
}

export default SwipeResults
