import React, { useState, useEffect } from 'react'

function VideoPlayer({ anime, firstEpisode, src, setSrc, selectedSeason, selectedEpisode, setSelectedEpisode, setSelectedSeason, selectedSeasonEpisodes }) {


  
  const handleEpisodeChange = (e) => {
    const newEpisodeIndex = e.target.selectedIndex;
    setSelectedEpisode(e.target.value);
    setSrc(prevSrc => {
      const newSrc = [...prevSrc];
      newSrc[selectedSeasonEpisodes.indexOf(e.target.value)] = src[newEpisodeIndex];
      return newSrc;
    });
  };

  const handleSeasonChange = (e) => {
    setSelectedSeason(e.target.value);
  }

  return (
    <div className="flex">
      <div className="relative w-full h-screen flex justify-center items-center text-white">
        <div className="video-container flex flex-col h-30 w-[2000px]">
          <div className="ml-10">
            <select name="" id="" className="w-1/6 rounded h-8 bg-custom-blue" value={selectedEpisode} onChange={handleEpisodeChange}>
              {src.map((videoUrl, index) => (
                <option key={index} value={videoUrl}>
                  EPISODE {index + 1}
                </option>
              ))}
            </select>
          </div>
          <div className="flex justify-center items-center h-20 gap-5">
            <button name="" id="" className="w-1/6 rounded h-1/2 bg-custom-blue">PREVIOUS EPISODE</button>
            <button name="" id="" className="w-1/6 rounded h-1/2 bg-custom-blue">NEXT EPISODE</button>
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