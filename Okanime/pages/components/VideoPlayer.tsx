import React, { useState, useEffect } from 'react'

function VideoPlayer({ anime, firstEpisode, src, setSrc, selectedSeason, selectedEpisode, setSelectedEpisode, setSelectedSeason, selectedSeasonEpisodes }) {

  
  const handleEpisodeChange = (e) => {
    const newEpisodeIndex = e.target.selectedIndex;
    setSelectedEpisode(selectedSeasonEpisodes[newEpisodeIndex]);
    setSrc(prevSrc => {
      const newSrc = [...prevSrc];
      newSrc[selectedSeasonEpisodes.indexOf(e.target.value)] = src[newEpisodeIndex];
      return newSrc;
    });

    if(newEpisodeIndex == selectedSeasonEpisodes.length - 1){
      const nextButton = document.getElementById('next_ep');
      const prevButton = document.getElementById('prev_ep');
      prevButton.style.display = 'block';
      nextButton.style.display = 'none';

    }
    else if(newEpisodeIndex == 0){
      const prevButton = document.getElementById('prev_ep');
      const nextButton = document.getElementById('next_ep');
      nextButton.style.display = 'block';
      prevButton.style.display = 'none';
    }
    else if(newEpisodeIndex > 0 && newEpisodeIndex < selectedSeasonEpisodes.length - 1){
      const prevButton = document.getElementById('prev_ep');
      const nextButton = document.getElementById('next_ep');
      nextButton.style.display = 'block';
      prevButton.style.display = 'block';
    }
  };

  const handleSeasonChange = (e) => {
    setSelectedSeason(e.target.value);
  }


  const handleNextEpisodeOnClick = () => {
    const nextButton = document.getElementById('next_ep');
    const prevButton = document.getElementById('prev_ep');
    const currentEpisodeIndex = selectedSeasonEpisodes.indexOf(selectedEpisode);
    const nextEpisodeIndex = currentEpisodeIndex + 1;

    if (nextEpisodeIndex < selectedSeasonEpisodes.length) {
      setSelectedEpisode(selectedSeasonEpisodes[nextEpisodeIndex]);
      const episodeSelector = document.getElementById('episode_selector') as HTMLSelectElement;
      episodeSelector.selectedIndex = nextEpisodeIndex;
      console.log('episodeSelector', episodeSelector.selectedIndex);
    }

    if(nextEpisodeIndex == selectedSeasonEpisodes.length - 1){
      prevButton.style.display = 'block';
      nextButton.style.display = 'none';

    }
    else if(nextEpisodeIndex == 0){
      nextButton.style.display = 'block';
      prevButton.style.display = 'none';
    }
    else if(nextEpisodeIndex > 0 && nextEpisodeIndex < selectedSeasonEpisodes.length - 1){
      nextButton.style.display = 'block';
      prevButton.style.display = 'block';
    }

  };

  const handlePrevEpisodeOnClick = () => {
    const nextButton = document.getElementById('next_ep');
    const prevButton = document.getElementById('prev_ep');
    const currentEpisodeIndex = selectedSeasonEpisodes.indexOf(selectedEpisode);
    const prevEpisodeIndex = currentEpisodeIndex - 1;
    if (prevEpisodeIndex >= 0) {
      setSelectedEpisode(selectedSeasonEpisodes[prevEpisodeIndex]);
      const episodeSelector = document.getElementById('episode_selector') as HTMLSelectElement;
      episodeSelector.selectedIndex = prevEpisodeIndex;
    }

    if(prevEpisodeIndex == selectedSeasonEpisodes.length - 1){
      prevButton.style.display = 'block';
      nextButton.style.display = 'none';

    }
    else if(prevEpisodeIndex == 0){
      nextButton.style.display = 'block';
      prevButton.style.display = 'none';
    }
    else if(prevEpisodeIndex > 0 && prevEpisodeIndex < selectedSeasonEpisodes.length - 1){
      nextButton.style.display = 'block';
      prevButton.style.display = 'block';
    }
  }

  return (
    <div className="flex">
      <div className="relative w-full h-screen flex justify-center items-center text-white">
        <div className="video-container flex flex-col h-30 w-[2000px]">
          <div className="ml-10">
            <select name="" id="episode_selector" className="w-1/6 rounded h-8 bg-custom-blue" value={selectedEpisode} onChange={handleEpisodeChange}>
              {selectedSeasonEpisodes.map((videoUrl, index) => (
                <option key={index} value={videoUrl}>
                  EPISODE {index + 1}
                </option>
              ))}
            </select>
          </div>
          <div className="flex justify-center items-center h-20 gap-5">
            <button name="" id="prev_ep" className="w-1/6 rounded h-1/2 bg-custom-blue" onClick={handlePrevEpisodeOnClick}>PREVIOUS EPISODE</button>
            <button name="" id="next_ep" className="w-1/6 rounded h-1/2 bg-custom-blue" onClick={handleNextEpisodeOnClick}>NEXT EPISODE</button>
          </div>
          <div className="flex justify-center items-center w-auto h-200">
            <div className="w-[1112px] h-[620px]">
            <iframe
              className="w-full h-full"
              src={
                src[selectedSeasonEpisodes.indexOf(selectedEpisode)] ||
                (selectedSeasonEpisodes.length > 0 ? src[0] : "")
              }
              allowFullScreen
            ></iframe>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default VideoPlayer