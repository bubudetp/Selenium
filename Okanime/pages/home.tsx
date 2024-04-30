"use client"
import React from 'react'

// components

import Header from './components/Header'

// styles

import styles from '../styles/Homepage.module.css'
import { useGlobalContext } from '../context/global'
import Link from 'next/link'

function Home() {
  const {popularAnime, isSearch} = useGlobalContext()
  const conditionalRender = () => {
    if(!isSearch){
      console.log(popularAnime)
      return popularAnime.map((anime) => {
        console.log(anime)
        // return <Link href={`${anime.mal_id}`} key={anime.mal_id}>
          {/* <img src={anime.images.jpg.large_image_url} alt="" /> */}
        {/* </Link> */}
      })
    }
  }
  return (
    <div className={styles.homepage_container}>
      <Header />
      <div className="pop-anime">
        {/* {conditionalRender()} */}
      </div>
    </div>
  )
}

export default Home
