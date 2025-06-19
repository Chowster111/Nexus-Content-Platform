import React, { useState } from 'react'
import styles from '../styles/SearchSection.module.css'

interface Props {
  onSearch: (query: string) => void
}

const SearchSection: React.FC<Props> = ({ onSearch }) => {
  const [query, setQuery] = useState('')

  const handleSubmit = () => {
    onSearch(query)
    setQuery('')
  }

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSubmit()
    }
  }

  return (
    <div className={styles.section}>
      <div className={styles.inputGroup}>
        <label htmlFor="search-input">Search any mind, any blog</label>
        <input
          id="search-input"
          className={styles.inputField}
          type="text"
          placeholder="e.g., GraphQL, microservices, machine learning"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          autoComplete='off'
        />
      </div>
      <button className={styles.btn} onClick={handleSubmit}>Search</button>
    </div>
  )
}

export default SearchSection
