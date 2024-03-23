from pymongo import MongoClient

# Create a new MongoClient
client = MongoClient('mongodb://localhost:27017/')

# Connect to your database
db = client['animeLibrary']

# Assume you have a list of data
data = [
    {"season": 1, "episode": 1, "link": "https://example.com/1"},
    {"season": 1, "episode": 2, "link": "https://example.com/2"},
    # Add more data as needed
]

# Insert the data into a collection in your database
db.myCollection.insert_many(data)