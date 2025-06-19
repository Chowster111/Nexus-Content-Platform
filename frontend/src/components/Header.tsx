// Header.tsx
import React from 'react'
import styles from '../styles/Header.module.css'

const Header = () => {
  return (
    <header className={styles.header}>
      <h1>🧠 Nexus</h1>
      <p className={styles.slogan}>Hub For All Engineering Leadership</p>
    </header>
  )
}

export default Header
