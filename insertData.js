const {MongoClient} = require('mongodb');
const fs = require('fs');

const uri = "mongodb+srv://burak:ZeffVnP97WkwgYB4@anime.ftfv2.mongodb.net/";
const client = new MongoClient(uri)

async function run(){
    try{
        await client.connect();
        const database = client.db('Anime');
        const collection = database.collection('AnimeList');
        
        const fileRead = fs.readFileSync('Animes.json');
        const videos = JSON.parse(fileRead);

        const documents = Object.keys(videos).map(key => ({
            name: key,
            iframes: videos[key]
          }));

          const result = await collection.insertMany(documents);
          console.log(`${result.insertedCount} documents were inserted`);

    }finally{
        await client.close();
    }
}

run().catch(console.dir);