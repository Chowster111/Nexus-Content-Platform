import React from 'react'
import styles from '../styles/App.module.css'

interface AnalyticsBoxProps {
  sources?: [string, number][]
  categories?: [string, number][]
}

const AnalyticsBox: React.FC<AnalyticsBoxProps> = ({ sources, categories }) => {
  const loading = !sources?.length || !categories?.length

  return (
    <div className={styles.analyticsBox}>
      <h2 className={styles.analyticsTitle}>Site Analytics</h2>

      {loading ? (
        <div className={styles.analyticsLoading}>Loading site stats...</div>
      ) : (
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
      )}
    </div>
  )
}

export default AnalyticsBox
