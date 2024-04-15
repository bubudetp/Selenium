import React, { useState, useEffect } from 'react'

function VideoPlayer({ anime, selectedSeason, selectedEpisode, setSelectedEpisode, setSelectedSeason, selectedSeasonEpisodes }) {
  const [src, setSrc] = useState([]);
  const [firstEpisode, setFirstEpisode] = useState('');

  useEffect(() => {
    if (selectedSeasonEpisodes) {
        setSelectedEpisode(1);
        }
  }, [])

  useEffect(() => {
    if (selectedSeasonEpisodes) {
      let videoUrls = selectedSeasonEpisodes.map(episode => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(episode, 'text/html');
        const iframe = doc.querySelector('iframe');
        return iframe ? iframe.getAttribute('src') : null;
      }).filter(url => url !== null);
      setSrc(videoUrls);
      setFirstEpisode(videoUrls[0]);
    }
  }, [selectedSeasonEpisodes])

  const handleEpisodeChange = (e) => {
    setSelectedEpisode(e.target.value);
    console.log(selectedSeasonEpisodes[0])
  }

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
                  Episode {index + 1}
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
              <iframe className="w-full h-full" src={selectedEpisode} allowFullScreen></iframe>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default VideoPlayer