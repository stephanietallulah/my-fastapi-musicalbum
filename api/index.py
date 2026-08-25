from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Daniel Caesar Music API",
    description="A beginner-friendly REST API containing information about Daniel Caesar songs.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MUSIC DATA
songs = [

    {
        "id": 1,
        "artist": "Daniel Caesar",
        "title": "Toronto 2014",
        "album": "Freudian",
        "year": 2017,
        "genre": "R&B / Soul",
        "duration": "3:34",
        "description": "A soulful track reflecting on love, memories, and personal experiences."
    },

    {
        "id": 2,
        "artist": "Daniel Caesar",
        "title": "Do You Like Me?",
        "album": "Never Enough",
        "year": 2023,
        "genre": "R&B / Soul",
        "duration": "3:59",
        "description": "A romantic R&B song exploring attraction, uncertainty, and emotional connection."
    },

    {
        "id": 3,
        "artist": "Daniel Caesar",
        "title": "Disillusioned",
        "album": "Never Enough",
        "year": 2023,
        "genre": "R&B / Soul",
        "duration": "3:42",
        "description": "A reflective song about disappointment, changing perspectives, and relationships."
    },

    {
        "id": 4,
        "artist": "Daniel Caesar",
        "title": "Cool",
        "album": "Never Enough",
        "year": 2023,
        "genre": "R&B / Soul",
        "duration": "2:36",
        "description": "A heartfelt track about the powerful connection between two people."
    },

    {
        "id": 5,
        "artist": "Daniel Caesar",
        "title": "Always",
        "album": "Never Enough",
        "year": 2023,
        "genre": "R&B / Soul",
        "duration": "3:34",
        "description": "An emotional track about lingering feelings, love, and devotion."
    },

    {
        "id": 6,
        "artist": "Daniel Caesar",
        "title": "Valentina",
        "album": "Never Enough",
        "year": 2023,
        "genre": "R&B / Soul",
        "duration": "2:34",
        "description": "A smooth and romantic R&B song expressing admiration and affection."
    },

        {
        "id": 8,
        "artist": "Daniel Caesar",
        "title": "Valentina",
        "album": "Never Enough",
        "year": 2023,
        "genre": "R&B / Soul",
        "duration": "2:34",
        "description": "A smooth and romantic R&B song expressing admiration and affection."
    }

]


# HOME
@app.get("/")
def home():

    return {
        "message": "Welcome to Daniel Caesar's Album Never Enough",
        "endpoints": [
            "/songs",
            "/songs/{song_id}",
            "/songs/search"
        ]
    }


# GET ALL SONGS
@app.get("/songs")
def get_songs():

    return {
        "count": len(songs),
        "songs": songs
    }


# SEARCH SONGS
# IMPORTANT: This must come BEFORE /songs/{song_id}
@app.get("/songs/search")
def search_songs(q: str = Query(..., min_length=1)):

    q = q.lower()

    results = []

    for song in songs:

        searchable_text = (
            f"{song['artist']} "
            f"{song['title']} "
            f"{song['album']} "
            f"{song['year']} "
            f"{song['genre']} "
            f"{song['description']}"
        ).lower()

        if q in searchable_text:
            results.append(song)

    return {
        "query": q,
        "count": len(results),
        "results": results
    }


# GET ONE SONG
@app.get("/songs/{song_id}")
def get_song(song_id: int):

    for song in songs:

        if song["id"] == song_id:
            return song

    raise HTTPException(
        status_code=404,
        detail="Song not found."
    )
