import React from 'react'

// components

import Header from './components/Header'

// styles

import styles from '../styles/Homepage.module.css'

function Home() {
  return (
    <div className={styles.homepage_container}>
      <Header />
    </div>
  )
}

export default Home
