import { MongoClient } from 'mongodb';
import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const uri = "mongodb+srv://burak:ZeffVnP97WkwgYB4@anime.ftfv2.mongodb.net/";
  const client = new MongoClient(uri);

  try {
    await client.connect();
    const db = client.db('Anime');
    const { index } = req.query;
    const num = parseInt(index, 10); // Ensure base 10

    if (isNaN(num)) {
      res.status(400).json({ message: 'Invalid index provided.' });
      return;
    }

    const collection = db.collection('AnimeList');
    const anime = await collection.findOne({ name: "Chainsaw Man" });

    if (!anime || !anime.iframes || num < 0 || num >= anime.iframes.length) {
      res.status(404).json({ message: 'Episode not found' });
      return;
    }

    const episode = anime.iframes[num];
    res.status(200).json(episode);
  } catch (e) {
    res.status(500).json({ message: e.message });
  } finally {
    await client.close();
  }
}
