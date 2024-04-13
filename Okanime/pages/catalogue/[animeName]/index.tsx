"use client"

import React, { useEffect, useState } from 'react';
import { useRouter, useSearchParams, usePathname } from 'next/navigation';
import styles from '../../../styles/Lecture.module.css';

function Anime() {
  const [anime, setAnime] = useState(null);
  const [error, setError] = useState(null);
  const [selectedEpisode, setSelectedEpisode] = useState('');
  const pathname = usePathname();
  const AnimeName = pathname ? pathname.substring(10) : "/Mashle";

  console.log(AnimeName)
  useEffect(() => {

    fetch(`/api/catalogue${AnimeName}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => setAnime(data))
      .catch(err => setError(err.message));
  }, [AnimeName]);


  if (error) return <div>Error fetching data: {error}</div>;
  if (!anime) return <div>Loading...</div>;

  const doc = new DOMParser().parseFromString(anime, 'text/html');
  let src = [];
  let iframes = doc.querySelectorAll('iframe');

  iframes.forEach(iframe => {
    src.push(iframe.getAttribute('src'));
  })

  let reversedSrc = src.slice();


  const handleEpisodeChange = (e) => {
    setSelectedEpisode(e.target.value);
  }

  return (
    <div className={styles.lecture_container}>
      <div className="dropdown"> 
        <select value={selectedEpisode} onChange={handleEpisodeChange}> 
          {reversedSrc.map((episodeUrl, index) => ( <option key={index} value={episodeUrl}> Episode {reversedSrc.length - index} </option> ))} 
        </select> 
      </div>
      <div><iframe width="640" height="384" src={selectedEpisode || reversedSrc[0]} allowFullScreen></iframe></div>
    </div>
  );
}

export default Anime;