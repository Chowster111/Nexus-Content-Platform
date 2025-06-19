import React from 'react'
import styles from '../styles/ToggleSwitch.module.css'
import { Tab } from '../App'

interface Props {
  activeTab: Tab
  onChange: (tab: Tab) => void
}

const ToggleSwitch: React.FC<Props> = ({ activeTab, onChange }) => {
  return (
    <div className={styles.toggleContainer}>
      <div className={styles.toggleInner}>
        <div
          className={`${styles.slider} ${
            activeTab === 'recommend' ? styles.right : ''
          }`}
        />
        <button
          className={`${styles.toggleOption} ${
            activeTab === 'search' ? styles.active : ''
          }`}
          onClick={() => onChange('search')}
        >
          Search
        </button>
        <button
          className={`${styles.toggleOption} ${
            activeTab === 'recommend' ? styles.active : ''
          }`}
          onClick={() => onChange('recommend')}
        >
          Recommend
        </button>
      </div>
    </div>
  )
}

export default ToggleSwitch
