import React from 'react'
import styles from '../styles/SwipeToggle.module.css'

interface SwipeToggleProps {
  enabled: boolean
  onToggle: (val: boolean) => void
}

const SwipeToggle: React.FC<SwipeToggleProps> = ({ enabled, onToggle }) => {
  return (
    <div className={styles.toggleWrapper} onClick={() => onToggle(!enabled)}>
      <div className={`${styles.toggleTrack} ${enabled ? styles.enabled : ''}`}>
        <div className={styles.toggleThumb} />
      </div>
      <span className={styles.toggleLabel}>{enabled ? 'Swipe' : 'List'}</span>
    </div>
  )
}

export default SwipeToggle
