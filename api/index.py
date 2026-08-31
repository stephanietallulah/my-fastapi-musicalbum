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
        "title": "Toronto 2014",
        "album": "Freudian",
        "artist": "Daniel Caesar",
        "featured_artist": "Mustafa",
        "writers": "Daniel Caesar, Mustafa, Simon Hessman, Dylan Wiggins",
        "producers": "Daniel Caesar, Sir Dylan, Simon On The Moon",
        "year": 2023,
        "genre": "R&B / Soul",
        "mood": "Nonstalgic / Emotional",
        "language": "English",
        "theme": "Love / Heartbreak",
        "popularity": "Over 118 million of streams on Spotify",
        "duration": "4:37",
        "description": "A song about looking back on the past, personal growth, and Daniel Caesar's connection to his hometown of Toronto."
    },

    {
        "id": 2,
        "title": "Backburner",
        "album": "Nicole",
        "artist": "Niki",
        "featured_artist": "None",
        "writers": "Nicole Zefanya",
        "producers": "NIKI and Ethan Gruska",
        "year": 2022,
        "genre": "R&B / Indie Rock",
        "mood": "Melancholic / Reflective",
        "language": "English",
        "theme": "Unrequited Love / Heartbreak",
        "popularity": "Over 100 million of streams on Spotify",
        "rating": "4.7/5",
        "duration": "3:34",
        "description": "A song about staying attached to someone who doesn't fully prioritize you, despite knowing you deserve more."
    },

    {
        "id": 3,
        "title": "Beaches",
        "album": "This Is How Tomorrow Moves",
        "artist": "beabadoobee",
        "featured_artist": "None",
        "writers": "Beatrice Laus",
        "producers": "Rick Rubin and Jacob Bugden",
        "year": 2024,
        "genre": "R&B / Indie Rock",
        "mood": "Dreamy / Romantic",
        "language": "English",
        "theme": "Love / Attraction",
        "popularity": "Over 235 million streams on Spotify",
        "rating": "4.4/5",
        "duration": "3:50",
        "description": "It is about overcoming self-doubt, stepping out of one's comfort zone, and finding a state of calm clarity."
    },

    {
        "id": 4,
        "title": "Thinking of You",
        "album": "One of the Boys",
        "artist": "Katy Perry",
        "featured_artist": "None",
        "writers": "Katy Perry",
        "producers": "Butch Walker",
        "year": 2009,
        "genre": "Soft Rock / Pop Rock",
        "mood": "Melancholic / Nostalgic",
        "language": "English",
        "theme": "Heartbreak / Regret",
        "popularity": "Over 240 million streams on Spotify",
        "rating": "4.7/5",
        "duration": "4:06",
        "description": "An emotional soft-rock power ballad about lingering grief, regret, and being unable to move on from a past love while stuck in a new relationship."
    },

    {
        "id": 5,
        "title": "All I Need To Hear",
        "album": "Being Funny in a Foreign Language",
        "artist": "The 1975",
        "featured_artist": "None",
        "writers": "Matty Healy",
        "producers": "Matty Healy, George Daniel, Jack Antonoff",
        "year": 2022,
        "genre": "Soft Pop Rock / Blue-eyed Soul",
        "mood": "Tender / Emotional",
        "language": "English",
        "popularity": "Over 82 million streams on Spotify",
        "rating": "4.2/5",
        "duration": "3:30",
        "description": "It explores emotional dependency and deep-seated isolation."
    },

    {
        "id": 6,
        "title": "Darling, I",
        "album": "Chromakopia",
        "artist": "Tyler, the Creator",
        "featured_artist": "Teezo Touchdown",
        "writers": "Tyler Okonma, Kamaal Fareed, and Barry White",
        "producers": "Tyler Okonma",
        "year": 2024,
        "genre": "Hip-hop / Rap",
        "mood": "Romantic / Warm",
        "language": "English",
        "popularity": "Over 240 million streams on Spotify",
        "rating": "4.1/5",
        "duration": "4:13",
        "description": "It explores emotional dependency and deep-seated isolation."
    },

    {
        "id": 7,
        "title": "Indecision",
        "album": "None",
        "artist": "Rex Orange County",
        "featured_artist": "Daniel Caesar",
        "writers": "Alexander O'Connor, Ashton Simmonds, Dylan Wiggins, and Aaron Paris",
        "producers": "Rex Orange County, Daniel Caesar, and Sir Dylan",
        "year": 2026,
        "genre": "Indie Pop / R&B",
        "mood": "Dreamy / Emotional",
        "language": "English",
        "popularity": "Over 4.2 million streams on Spotify",
        "rating": "4.5/5",
        "duration": "3:06",
        "description": "A dreamy and emotional indie-pop song about uncertainty in love and the struggle of making a decision about a relationship."
    },
   
    {
        "id": 8,
        "title": "Into It",
        "album": "Chase Atlantic (2017)",
        "artist": "Chase Atlantic",
        "featured_artist": "None",
        "writers": "Christian Anthony, Clinton Cave, Mitchel Cave",
        "producers": "Christian Anthony, Clinton Cave, Mitchel Cave",
        "year": 2017,
        "genre": "Alternative / Indie",
        "mood": "Flirty / Energetic",
        "language": "English",
        "popularity": "Over 920 million streams on Spotify",
        "rating": "4.1/5",
        "duration": "3:17",
        "description": "A dark, energetic track about fame, relationships, and embracing a chaotic lifestyle despite its pressures."
    },

    {
        "id": 9,
        "title": "Heart of A Woman",
        "album": "Finally Over It",
        "artist": "Summer Walker",
        "featured_artist": "None",
        "writers": "Summer Walker, David “Dos Dias” Bishop",
        "producers": "Tavaras Jordan",
        "year": 2025,
        "genre": "R&B / Soul",
        "mood": "Romantic / Emotional",
        "language": "English",
        "popularity": "Over 112 million streams on Spotify",
        "rating": "4.1/5",
        "duration": "2:50",
        "description": "A song about loving someone despite their flaws and reaching the limit of how much you can tolerate in a relationship."
    },

     {
        "id": 10,
        "title": "Moth To A Flame",
        "album": "Paradise Again",
        "artist": "Swedish House Mafia",
        "featured_artist": "The Weeknd",
        "writers": "Axel Hedfors (Axwell), Steve Angello, Sebastian Ingrosso, Carl Nordström, and Abel “The Weeknd” Tesfaye",
        "producers": "Swedish House Mafia and Carl Nordström",
        "year": 2022,
        "genre": "Dance / Electronic / Pop",
         "mood": "Dark / Seductive",
        "language": "English",
        "popularity": "Over 1.52 billion streams on Spotify",
        "rating": "4.4/5",
        "duration": "2:50",
        "description": "A song about being drawn to someone even when you know the relationship may be complicated."
    },

    {
        "id": 11,
        "title": "Waltz of Four Left Feet",
        "album": "For Princesses, By Thieves (O Mga Awit ng Hiraya Para sa Guni-guning Sinta",
        "artist": "Shirebound & Busking",
        "featured_artist": "None",
        "writers": "Iego Tan",
        "producers": "Ean Aguila",
        "year": 2019,
        "genre": "OPM / Indie / Kundiman",
        "mood": "Bittersweet / Melancholic",
        "language": "Tagalog",
        "popularity": "Over 118 million streams on Spotify",
        "rating": "4.5/5",
        "duration": "5:38",
        "description": "A song about quietly admiring someone and being content simply to be near them."
    },

    {
        "id": 12,
        "title": "Some Of Your Love",
        "album": "PARTYNEXTDOOR 3 (P3) [10-YEAR EDITION]",
        "artist": "PARTYNEXTDOOR",
        "featured_artist": "None",
        "writers": "Brathwaite, Jordan Evans, Jordon Manswell, J’vell Boyce, James Tatum, R. Dumas, J-J. Debout",
        "producers": "Jordan Evans, Jordon Manswell, J’vell Boyce",
        "year": 2026,
        "genre": "R&B",
        "mood": "Romantic / Melancholic",
        "language": "English",
        "popularity": "Over 11 million streams on Spotify",
        "rating": "4.4/5",
        "duration": "2:39",
        "description": "A song about centered on attraction and wanting affection from someone."
    },

    {
        "id": 13,
        "title": "When I Was Your Man",
        "album": "Unorthodox Jukebox",
        "artist": "Bruno Mars",
        "featured_artist": "None",
        "writers": "Bruno Mars, Philip Lawrence, Ari Levine, Andrew Wyatt",
        "producers": "The Smeezingtons",
        "year": 2012,
        "genre": "Pop / Soul",
        "mood": "Sad / Regretful",
        "language": "English",
        "popularity": "Over 3.27 million streams on Spotify",
        "rating": "4.6/5",
        "duration": "3:33",
        "description": "A song about regret and realizing too late that you should have treated someone better."
    },

   {
        "id": 14,
        "title": "Pangarap Lang Kita",
        "album": "Middle-Aged Juvenile Novelty Pop Rockers",
        "artist": "Parokya Ni Edgar",
        "featured_artist": "Happee Sy",
        "writers": "Chito Miranda",
        "producers": "Chito Miranda",
        "year": 2010,
        "genre": "OPM / Pop Rock",
        "mood": "Romantic / Bittersweet",
        "language": "Tagalog",
        "popularity": "Over 200 million streams on Spotify",
        "rating": "4.5/5",
        "duration": "3:14",
        "description": "A song about loving someone who feels out of reach and accepting that they may remain only a dream."
    },
    
    {
        "id": 15,
        "title": "Summertime Sadness",
        "album": "Born To Die",
        "artist": "Lana Del Rey",
        "featured_artist": "None",
        "writers": "Lana Del Rey, Rick Nowels, Kieran De Jour",
        "producers": "Emile Haynie, Rick Nowels",
        "year": 2012,
        "genre": "Pop / Trip-Hop",
        "mood": "Melancholic / Dreamy",
        "language": "English",
        "popularity": "Over 2.45 billion streams on Spotify",
        "rating": "4.6/5",
        "duration": "4:25",
        "description": "A song about love, longing, and the sadness that comes with the possibility of losing someone."
    },

    {
        "id": 16,
        "title": "Panaginip",
        "album": "None",
        "artist": "nicole",
        "featured_artist": "None",
        "writers": "Nicole Brian De Leon",
        "producers": "Stephen Tan",
        "year": 2025,
        "genre": "Indie Pop / OPM",
        "mood": "Dreamy / Melancholic",
        "language": "Tagalog",
        "popularity": "Over 147 million streams on Spotify",
        "rating": "4.5/5",
        "duration": "5:17",
        "description": "A song about being deeply captivated by someone and imagining a future together."
    },

    {
        "id": 17,
        "title": "Mean It",
        "album": "~how i'm feeling~",
        "artist": "Lauv",
        "featured_artist": "Lany",
        "writers": "Ari Leff, Paul Klein, Jake Goss, Michael Matosic, Michael Pollack, John Hill, Jordan Palmer",
        "producers": "Lauv, LANY, Mike Crossey, John Hill, Jordan Palmer",
        "year": 2020,
        "genre": "Pop / Electropop",
        "mood": "Vulnerable / Melancholic",
        "language": "English",
        "popularity": "Over 592 million streams on Spotify",
        "rating": "4.4/5",
        "duration": "3:52",
        "description": "A song about wanting someone to be honest about their feelings instead of giving mixed signals."
    },

    {
        "id": 18,
        "title": "You’re Losing Me (From The Vault)",
        "album": "Midnights (The Late Night Edition)",
        "artist": "Taylor Swift",
        "featured_artist": "None",
        "writers": "Taylor Swift, Jack Antonoff",
        "producers": "Taylor Swift, Jack Antonoff",
        "year": 2023,
        "genre": "Downtempo / Pop",
        "mood": "Heartbroken / Frustrated",
        "language": "English",
        "popularity": "Over 400 million streams on Spotify",
        "rating": "4.6/5",
        "duration": "4:38",
        "description": "A song about relationship falling apart and the painful realization that it may no longer be possible to save it."
    },  

    {
        "id": 19,
        "title": "hate that i made you love me",
        "album": "petal",
        "artist": "Ariana Grande",
        "featured_artist": "None",
        "writers": "Ariana Grande, Ilya Salmanzadeh",
        "producers": "Ariana Grande, Ilya Salmanzadeh",
        "year": 2026,
        "genre": "Contemporary R&B / Pop",
        "mood": "Sad / Regretful",
        "language": "English",
        "popularity": "Over 419 million streams on Spotify",
        "rating": "4.4/5",
        "duration": "3:17",
        "description": "A song about unwanted attention, emotional boundaries, and being blamed for someone else's attachment."
    },  

    {
        "id": 20,
        "title": "I Wanna Be Yours",
        "album": "AM",
        "artist": "Arctic Monkeys",
        "featured_artist": "None",
        "writers": "Alex Turner, John Cooper Clarke",
        "producers": "James Ford, Ross Orton",
        "year": 2013,
        "genre": "Indie Rock / Alternative Rock",
        "mood": "Romantic / Intimate",
        "language": "English",
        "popularity": "Over 3.96 billion streams on Spotify",
        "rating": "4.7/5",
        "duration": "3:04",
        "description": "A song about expressing intense devotion and the desire to be completely committed to someone."
    },  

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
