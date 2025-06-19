import React, { useState } from 'react'
import styles from '../styles/RecommendSection.module.css'

interface Props {
  onRecommend: (topic: string) => void
}

const RecommendSection: React.FC<Props> = ({ onRecommend }) => {
  const [topic, setTopic] = useState('')

  const handleSubmit = () => {
    onRecommend(topic)
    setTopic('')
  }

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSubmit()
    }
  }

  return (
    <div className={styles.section}>
      <div className={styles.inputGroup}>
        <label htmlFor="recommend-input">Get recommendations from engineering minds</label>
        <input
          id="recommend-input"
          className={styles.inputField}
          type="text"
          placeholder="e.g., How we scaled our API architecture"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          onKeyPress={handleKeyPress}
          autoComplete='off'
        />
      </div>
      <button className={styles.btn} onClick={handleSubmit}>Recommend</button>
    </div>
  )
}

export default RecommendSection
