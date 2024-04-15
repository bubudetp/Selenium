"use client"

import React, { useEffect, useState } from 'react';
import { useRouter, useSearchParams, usePathname } from 'next/navigation';
import "../../globals.css"
import Header from '../../components/Header';
import VideoPlayer from '../../components/VideoPlayer';

function Anime() {
  const [anime, setAnime] = useState(null);
  const [error, setError] = useState(null);
  const [selectedEpisode, setSelectedEpisode] = useState('');
  const [selectedSeason, setSelectedSeason] = useState('1');
  const [selectedSeasonEpisodes, setSelectedSeasonEpisodes] = useState([]);

  const pathname = usePathname();
  const AnimeName = pathname ? pathname.substring(10) : "/Mashle";

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

  useEffect(() => {
    if (anime) {
      const seasonEpisodes = anime[selectedSeason] || {};
      setSelectedSeasonEpisodes(Object.values(seasonEpisodes));
    }
  }, [anime, selectedSeason]);

  useEffect(() => {
    if (selectedSeasonEpisodes.length > 0) {
      setSelectedEpisode(selectedSeasonEpisodes[0]);
    }
  }, [selectedSeasonEpisodes]);

  if (error) return <div>Error fetching data: {error}</div>;
  if (!anime) return <div>Loading...</div>;

  return (
    <div>
      <Header />
      <div className="bg-custom-beige h-screen">
        <VideoPlayer
          anime={anime}
          selectedSeason={selectedSeason}
          selectedEpisode={selectedEpisode}
          setSelectedEpisode={setSelectedEpisode}
          setSelectedSeason={setSelectedSeason}
          selectedSeasonEpisodes={selectedSeasonEpisodes}
        />
      </div>
    </div>
  );
}

export default Anime;