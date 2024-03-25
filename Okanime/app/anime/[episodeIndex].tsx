"use client"
import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';

function Anime() {
  const [anime, setAnime] = useState(null);
  const [error, setError] = useState(null);
  const episodeIndex = useParams();


  useEffect(() => {
    fetch('api/anime/${episodeIndex}')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => setAnime(data))
      .catch(err => setError(err.message));
  }, [episodeIndex]);

  if (error) return <div>Error fetching data: {error}</div>;
  if (!anime) return <div>Loading...</div>;

  const doc = new DOMParser().parseFromString(anime, 'text/html');
  const src = doc.querySelector('iframe').getAttribute('src');

  return (
    <div>

      <h1>Hello hello {anime.name}{console.log(anime)}</h1>
      <div><iframe width="640" height="384" src={src} frameborder="0" allowfullscreen></iframe></div>
      {/* <p>{anime.description}</p> */}
      {/* more properties of the anime */}
    </div>
  );
}

export default Anime;