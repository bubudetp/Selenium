const { MongoClient } = require('mongodb');

const uri = "mongodb+srv://burak:ZeffVnP97WkwgYB4@anime.ftfv2.mongodb.net/";
const client = new MongoClient(uri);

async function run() {
    try {
        await client.connect();
        const database = client.db("Anime");
        const collection = database.collection("AnimeList");

        const query = {name: "Chainsaw Man"}; 
        const cursor = collection.find(query);

        console.log("Found documents:");
        await cursor.forEach(doc => console.log(doc));
    } finally {
        await client.close();
    }
}

run().catch(console.dir);


useEffect(() => {
    fetch('/api/anime')
      .then(res => res.json())
      .then(data => {
        console.log(data); 
      });
  }, []);
  


"use client"
import React, { useEffect, useState } from 'react';

function Anime() {
  const [anime, setAnime] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('./FetchData')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        console.log(response.json());
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
      <h1>Hello hello {anime}</h1>
      {/* <p>{anime.description}</p> */}
      {/* more properties of the anime */}
    </div>
  );
}

export default Anime;


// pages/api/anime.js

