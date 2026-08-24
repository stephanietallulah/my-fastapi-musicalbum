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
        "title": "Ocho Rios",
        "album": "Never Enough",
        "year": 2023,
        "genre": "R&B / Soul",
        "duration": "3:45",
        "description": "A smooth and emotional R&B track from Never Enough."
    },

    {
        "id": 2,
        "artist": "Daniel Caesar",
        "title": "Let Me Go",
        "album": "Never Enough",
        "year": 2023,
        "genre": "R&B / Soul",
        "duration": "3:48",
        "description": "A reflective song about relationships and emotional distance."
    },

    {
        "id": 3,
        "artist": "Daniel Caesar",
        "title": "Do You Like Me?",
        "album": "Never Enough",
        "year": 2023,
        "genre": "R&B / Soul",
        "duration": "3:59",
        "description": "A romantic R&B song exploring attraction and uncertainty."
    },

    {
        "id": 4,
        "artist": "Daniel Caesar",
        "title": "Always",
        "album": "Never Enough",
        "year": 2023,
        "genre": "R&B / Soul",
        "duration": "3:34",
        "description": "An emotional track about lingering feelings and devotion."
    },

    {
        "id": 5,
        "artist": "Daniel Caesar",
        "title": "Cool",
        "album": "Never Enough",
        "year": 2023,
        "genre": "R&B / Soul",
        "duration": "3:47",
        "description": "A mellow song with a laid-back sound and intimate atmosphere."
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
