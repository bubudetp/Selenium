"use client"
import React, { useEffect, useState } from 'react';

function Anime() {
  const [anime, setAnime] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('api/anime')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => setAnime(data))
      .catch(err => setError(err.message));
  }, []);

  if (error) return <div>Error fetching data: {error}</div>;
  if (!anime) return <div>Loading...</div>;


  return (
    <div>
      {/* Render your data here */}
      <h1>Hello hello {anime.name} {console.log(anime)}</h1>
      {/* <p>{anime.description}</p> */}
      {/* more properties of the anime */}
    </div>
  );
}

export default Anime;