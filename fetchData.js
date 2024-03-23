const { MongoClient } = require('mongodb');

// Replace the URI string with your connection string.
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
