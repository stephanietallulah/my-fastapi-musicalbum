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
        "artist": "Niki",
        "title": "Backburner",
        "album": "Nicole",
        "rating": "4.7/5",
        "year": 2022,
        "genre": "R&B / Indie Rock",
        "popularity": "Hundreds of million of streams on Spotify",
        "producers": "NIKI and Ethan Gruska",
        "writers": "Nicole Zefanya",
        "duration": "3:34",
        "description": "A melancholic alternative R&B and pop song about unrequited love and the pain of being someone's second choice."
    },

    {
        "id": 3,
        "artist": "beabadoobee",
        "title": "Beaches",
        "album": "This Is How Tomorrow Moves",
        "rating": "4.4/5",
        "year": 2024,
        "genre": "R&B / Indie Rock",
        "popularity": "Over 235 million streams on Spotify",
        "producers": "Rick Rubin and Jacob Bugden",
        "writers": "Beatrice Laus",
        "duration": "3:50",
        "description": "It is about overcoming self-doubt, stepping out of one's comfort zone, and finding a state of calm clarity."
    },

    {
        "id": 4,
        "artist": "Katy Perry",
        "title": "Thinking of You",
        "album": "One of the Boys",
        "rating": "4.7/5",
        "year": 2009,
        "genre": "Soft Rock / Pop Rock",
        "popularity": "Over 240 million streams on Spotify",
        "producers": "Butch Walker",
        "writers": "Katy Perry",
        "duration": "4:06",
        "description": "An emotional soft-rock power ballad about lingering grief, regret, and being unable to move on from a past love while stuck in a new relationship."
    },

    {
        "id": 5,
        "artist": "The 1975",
        "title": "All I Need To Hear",
        "album": "Being Funny in a Foreign Language",
        "rating": "4.2/5",
        "year": 2022,
        "genre": "Soft Pop Rock / Blue-eyed Soul",
        "popularity": "Over 82 million streams on Spotify",
        "producers": "Matty Healy, George Daniel, Jack Antonoff",
        "writers": "Matty Healy",
        "duration": "3:30",
        "description": "It explores emotional dependency and deep-seated isolation."
    },

    {
        "id": 6,
        "artist": "Tyler, the Creator",
        "title": "Darling, I",
        "album": "Chromakopia",
        "rating": "4.1/5",
        "year": 2024,
        "genre": "Hip-hop / Rap",
        "popularity": "Over 240 million streams on Spotify",
        "producers": "Tyler Okonma",
        "writers": "Tyler Okonma, Kamaal Fareed, and Barry White",
        "duration": "4:13",
        "description": "It explores emotional dependency and deep-seated isolation."
    },

    {
        "id": 7,
        "artist": "Luther Kendrick",
        "title": "Heart P6",
        "album": "Unknown",
        "rating": "N/A",
        "year": "Unknown",
        "genre": "R&B / Soul",
        "popularity": "Unknown",
        "producers": "Unknown",
        "writers": "Luther Kendrick",
        "duration": "Unknown",
        "description": "A heartfelt track with emotional depth."
    },

    {
        "id": 8,
        "artist": "Kendrick",
        "title": "6 Kendrick",
        "album": "Unknown",
        "rating": "N/A",
        "year": "Unknown",
        "genre": "Hip-hop / Rap",
        "popularity": "Unknown",
        "producers": "Unknown",
        "writers": "Kendrick",
        "duration": "Unknown",
        "description": "A rap track showcasing lyrical prowess."
    },

    {
        "id": 9,
        "artist": "Eric Bellinger",
        "title": "Drive By",
        "album": "Unknown",
        "rating": "N/A",
        "year": "Unknown",
        "genre": "R&B / Hip-hop",
        "popularity": "Unknown",
        "producers": "Unknown",
        "writers": "Eric Bellinger",
        "duration": "Unknown",
        "description": "A smooth R&B track with hip-hop influences."
    },

    {
        "id": 10,
        "artist": "Taylor Swift",
        "title": "Ruin the Friendship",
        "album": "Unreleased / Demo",
        "rating": "N/A",
        "year": "Unknown",
        "genre": "Pop",
        "popularity": "Fan-favorite unreleased track",
        "producers": "Unknown",
        "writers": "Taylor Swift",
        "duration": "Unknown",
        "description": "A song about crossing the line between friendship and romance."
    },

    {
        "id": 11,
        "artist": "Backstreet Boys",
        "title": "Shape of My Heart",
        "album": "Black & Blue",
        "rating": "4.6/5",
        "year": 2000,
        "genre": "Pop",
        "popularity": "Classic hit with millions of streams",
        "producers": "Max Martin",
        "writers": "Max Martin, Rami Yacoub, Lisa Miskovsky",
        "duration": "3:50",
        "description": "A heartfelt pop ballad about regret and love."
    },

    {
        "id": 12,
        "artist": "Green Day",
        "title": "Last Night on Earth",
        "album": "21st Century Breakdown",
        "rating": "4.3/5",
        "year": 2009,
        "genre": "Alternative Rock",
        "popularity": "Millions of streams on Spotify",
        "producers": "Butch Vig",
        "writers": "Billie Joe Armstrong",
        "duration": "3:57",
        "description": "A romantic rock ballad with emotional intensity."
    },

    {
        "id": 13,
        "artist": "Charlie Burg",
        "title": "I Don’t Wanna Be Okay Without You",
        "album": "Two, Five, Six, Four",
        "rating": "4.5/5",
        "year": 2018,
        "genre": "Indie Pop / R&B",
        "popularity": "Cult favorite indie track",
        "producers": "Charlie Burg",
        "writers": "Charlie Burg",
        "duration": "Unknown",
        "description": "An emotional indie pop song about vulnerability and love."
    },

    {
        "id": 14,
        "artist": "Chase Atlantic",
        "title": "Friends",
        "album": "Unknown",
        "rating": "N/A",
        "year": "Unknown",
        "genre": "Alternative R&B",
        "popularity": "Fan-favorite track",
        "producers": "Chase Atlantic",
        "writers": "Chase Atlantic",
        "duration": "Unknown",
        "description": "A dark, moody track about toxic relationships."
    },

    {
        "id": 15,
        "artist": "Chase Atlantic",
        "title": "Consume",
        "album": "Unknown",
        "rating": "N/A",
        "year": "Unknown",
        "genre": "Alternative R&B",
        "popularity": "Fan-favorite track",
        "producers": "Chase Atlantic",
        "writers": "Chase Atlantic",
        "duration": "Unknown",
        "description": "A track about indulgence, addiction, and desire."
    },

    {
        "id": 16,
        "artist": "Frank Ocean",
        "title": "Moon River",
        "album": "Single Release",
        "rating": "4.8/5",
        "year": 2018,
        "genre": "R&B / Soul",
        "popularity": "Millions of streams on Spotify",
        "producers": "Frank Ocean",
        "writers": "Henry Mancini, Johnny Mercer",
        "duration": "Unknown",
        "description": "Frank Ocean’s haunting cover of the classic ballad."
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
