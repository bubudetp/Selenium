// pages/api/anime.ts
import { MongoClient } from 'mongodb';
import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  // Your MongoDB connection string should be in an environment variable
  const uri = "mongodb+srv://burak:ZeffVnP97WkwgYB4@anime.ftfv2.mongodb.net/";

  const client = new MongoClient(uri);

  try {
    await client.connect();
    const db = client.db('Anime');
    const collection = db.collection('AnimeList');
    const anime = await collection.findOne({ name: "Chainsaw Man" });
    res.status(200).json(anime);
  } catch (e) {
    res.status(500).json({ message: e.message });
  } finally {
    await client.close();
  }
}


