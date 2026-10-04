from fastapi import FastAPI, HTTPException, Header, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

# configuration 
API_KEY = "student-api-key-123"
API_VERSION = "1.0"

# API KEY AUTHENTICATION
def verify_api_key(x_api_key: Optional[str] = Header(default=None)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key."
        )
    return True

app = FastAPI(
    title="NOTENOUGH Music API",
    description="Discover songs, artists, and the stories behind the music.",
    version=API_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DATA MODEL
class Song(BaseModel):
    id: int
    title: str = Field(min_length=1)
    album: Optional[str] = None
    artist: str = Field(min_length=1)
    featured_artist: Optional[str] = None
    writers: str
    producers: str
    year: int = Field(ge=1900, le=2100)
    genre: str = Field(min_length=1)
    language: Optional[str] = None
    popularity: str
    rating: str = Field(min_length=1)
    spotify_url: str
    image_url: str
    audio_url: str
    duration: str = Field(min_length=1)
    description: str = Field(min_length=1)

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
        "genre": "R&B",
        "language": "English",
        "popularity": "Over 118 million of streams on Spotify",
        "rating": "4.7/5",
        "spotify_url": "https://open.spotify.com/track/4t9R5rbtovdvya28uMODDz?si=cd8429623cc245ca",
        "image_url": "https://cdn-images.dzcdn.net/images/cover/0d571082af7c78114321031d7f84d331/1900x1900-000000-80-0-0.jpg",
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/Daniel%20Caesar%20-%20Toronto%202014%20(Official%20Audio).mp3",
        "duration": "4:37",
        "description": "A song about looking back on the past, personal growth, and Daniel Caesar's connection to his hometown of Toronto."
    },

    {
        "id": 2,
        "title": "Backburner",
        "album": "Nicole",
        "artist": "NIKI",
        "featured_artist": "None",
        "writers": "Nicole Zefanya",
        "producers": "NIKI and Ethan Gruska",
        "year": 2022,
        "genre": "Indie Rock",
        "language": "English",
        "popularity": "Over 100 million of streams on Spotify",
        "rating": "4.7/5",
        "spotify_url": "https://open.spotify.com/track/7gqdZpe7MlTLA59viClLoY?si=7d231e5c82f3459f",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTy_KoRj3Uxz9zXTk4k6aZ3fllcVE1PfVXVMJdm5lJUuQ&s=10",
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/Backburner.mp3",
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
        "genre": "Indie Rock",
        "language": "English",
        "popularity": "Over 235 million streams on Spotify",
        "rating": "4.4/5",
        "spotify_url": "https://open.spotify.com/track/1a19jsjG2DvbN1fVJonKUU?si=767f37dbeeb141b4",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2XSGoaWNwdu3fbNJu0DgfBPCbTzmwTmqqSnIyH0HM8w&s=10",
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/beabadoobee%20-%20Beaches.mp3",
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
        "genre": "Soft Pop Rock",
        "language": "English",
        "popularity": "Over 240 million streams on Spotify",
        "rating": "4.7/5",
        "spotify_url": "https://open.spotify.com/track/4ciwlQ4UYHUMj2wuH0ffw6?si=89b385f60af1442b",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTcm43sjdPWddoV08Xd2jJE71bUMNwNPcvLt0pff1462Q&s",
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/Katy%20Perry%20-%20Thinking%20Of%20You%20(With%20Lyrics).mp3",
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
        "genre": "Soft Pop Rock",
        "language": "English",
        "popularity": "Over 82 million streams on Spotify",
        "rating": "4.2/5",
        "spotify_url": "https://open.spotify.com/track/5WdMBJD7V5CVBTBdE2at2D?si=f6f305bea216494f",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR1qI2nxDo6lcWxM0HFjOWeUtVHYfJJY7q2Ht69a1LBcQ&s",
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/The%201975%20-%20All%20I%20Need%20To%20Hear%20(Audio).mp3",
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
        "language": "English",
        "popularity": "Over 240 million streams on Spotify",
        "rating": "4.1/5",
        "spotify_url": "https://open.spotify.com/track/0VaeksJaXy5R1nvcTMh3Xk?si=aab59049ca80461d",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQaoCxvIbeMF_wGllAm9n7Zki9rAS_Jpr0K-G7HSm6Ww&s=10",
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/Tyler,%20The%20Creator%20-%20Darling,%20I%20(feat.%20A$AP%20Rocky).mp3",
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
        "genre": "Indie Pop",
        "language": "English",
        "popularity": "Over 4.2 million streams on Spotify",
        "rating": "4.5/5",
        "spotify_url": "https://open.spotify.com/track/0zZ5TnmUIub96AsZmkCXYS?si=49ae86329b474fe9",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTG-WQt0reCCYhOyhAL4p46UMT0FcE1NO1yaUSMkyvttA&s",
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/Rex%20Orange%20County,%20Daniel%20Caesar%20-%20Indecision%20(Lyrics).mp3",
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
        "language": "English",
        "popularity": "Over 920 million streams on Spotify",
        "rating": "4.1/5",
        "spotify_url": "https://open.spotify.com/track/4HwDCXsMBC7SUdp2WT4MZP?si=cb102e43ec494bef",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQP6nU36o42iFEKXLGD8z_s_4vcDGtqnZBEDCnjtx0mWg&s=10",
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/Chase%20Atlantic%20-%20Into%20It%20(Official%20Audio).mp3",
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
        "genre": "R&B",
        "language": "English",
        "popularity": "Over 112 million streams on Spotify",
        "rating": "4.1/5",
        "spotify_url": "https://open.spotify.com/track/2oVVaVY0LkzwAYYcyzon6Z?si=3f179fe459b642fa",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTnXP_-h2kNQlN9aDX4yF64VzOtYUw0TKpLMyA5dz3-ug&s=10",
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/Heart%20Of%20A%20Woman.mp3",
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
        "genre": "Pop",
        "language": "English",
        "popularity": "Over 1.52 billion streams on Spotify",
        "rating": "4.4/5",
        "spotify_url": "https://open.spotify.com/track/3uuR20w7HgLlb5Hha2mCxb?si=cd74ed152a364d3d",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJLjIzHsiIHa4O6DAXAaf8aqkhfSP7TcOh1AczcPzEXw&s=10",
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/The%20Weeknd%20Moth%20To%20A%20Flame%20(HD%20AUDIO).mp3",
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
        "genre": "OPM",
        "language": "Tagalog",
        "popularity": "Over 118 million streams on Spotify",
        "rating": "4.5/5",
        "spotify_url": "https://open.spotify.com/track/29eiVZ3R6iJcXB01dOAl6H?si=9a3cc16fc7b04926",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQVkKEBiHYVzg6W42Qf6KGvZp5BDERos4fX9srVM6YuIw&s=10",
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/Waltz%20of%20Four%20Left%20Feet.mp3",
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
        "language": "English",
        "popularity": "Over 11 million streams on Spotify",
        "rating": "4.4/5",
        "spotify_url": "https://open.spotify.com/track/554p4ro2rs7dHqGPwQX67H?si=a20776bd59934662",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZ149LbhVD-td9f0ePs0M_HgI43vWVAN6NV0ewazen3g&s=10",
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/PARTYNEXTDOOR%20-%20Some%20Of%20Your%20Love%20(Official%20Audio).mp3",
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
        "language": "English",
        "popularity": "Over 3.27 million streams on Spotify",
        "rating": "4.6/5",
        "spotify_url": "https://open.spotify.com/track/0nJW01T7XtvILxQgC5J7Wh?si=50e8d621e24744e4",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-WWY_96Rm-llgpMDvjX2NIRyPaztQp_VuG8x1qAHAog&s=10",
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/Bruno%20Mars%20-%20When%20I%20Was%20Your%20Man.mp3",
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
        "genre": "OPM",
        "language": "Tagalog",
        "popularity": "Over 200 million streams on Spotify",
        "rating": "4.5/5",
        "spotify_url": "https://open.spotify.com/track/09WPbmLdcBhJPcJwEJc1Yv?si=12e7bd32b0ef4153",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTDIhlKNKwqVpLn8bjocUglgJ-dNRzFmxxhLxbCWx7c6A&s",
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/Pangarap%20Lang%20Kita.mp3",
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
        "genre": "Pop",
        "language": "English",
        "popularity": "Over 2.45 billion streams on Spotify",
        "rating": "4.6/5",
        "spotify_url": "https://open.spotify.com/track/3BJe4B8zGnqEdQPMvfVjuS?si=69b7a8fa7a0348df",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQzEtujGvbM3pJJFDEFL7mVGSgb4BAGzoA0SogCxCGLZQ&s=10", 
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/Lana%20Del%20Rey%20-%20Summertime%20Sadness%20(Lyrics).mp3",
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
        "genre": "OPM",
        "language": "Tagalog",
        "popularity": "Over 147 million streams on Spotify",
        "rating": "4.5/5",
        "spotify_url": "https://open.spotify.com/track/6wcjLOGIdmw8BUaRho4c9L?si=ff7d00b331014be8",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ9Fv_8M1aM9L557rLx4ICLYuSZuEEKLmfuXd19EfdoVg&s",
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/Panaginip%20-%20nicole%20(Official%20Lyric%20Video).mp3",
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
        "genre": "Pop",
        "language": "English",
        "popularity": "Over 592 million streams on Spotify",
        "rating": "4.4/5",
        "spotify_url": "https://open.spotify.com/track/6mXdCcFnPKQznj4CmMRmHC?si=958a47ccf1f44007",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQ6uHMlcvTmONsVa-wvvcuUR3KXwc-4thxKAp5cHmVDg&s=10",
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/Lauv,%20LANY%20-%20Mean%20It%20(Lyrics).mp3",
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
        "genre": "Pop",
        "language": "English",
        "popularity": "Over 400 million streams on Spotify",
        "rating": "4.6/5",
        "spotify_url": "https://open.spotify.com/track/3CWq0pAKKTWb0K4yiglDc4?si=74b752468d544fdf",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQL1r7Kjvv_zi-F42XyK6SBs1wZ5oGFq-nvk8FicMYTsQ&s=10",
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/Taylor%20Swift%20-%20You're%20Losing%20Me%20(From%20The%20Vault).mp3",
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
        "genre": "Contemporary R&B",
        "language": "English",
        "popularity": "Over 419 million streams on Spotify",
        "rating": "4.4/5",
        "spotify_url": "https://open.spotify.com/track/20jbSiX29FDX4oQxBXyUEi?si=da1c033780414c4d",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRhwDxG_sS1WDxTbx4IRPOGHJbHd4iBm4-9ZQ6pceU0WA&s",
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/hate%20that%20i%20made%20you%20love%20me.mp3",
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
        "genre": "Indie Rock",
        "language": "English",
        "popularity": "Over 3.96 billion streams on Spotify",
        "rating": "4.7/5",
        "spotify_url": "https://open.spotify.com/track/5XeFesFbtLpXzIVDNQP22n?si=22b97566c452476e",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSSzuoz1-idhHAm-ZBqI6_9mitNA5fewlNFf_FimaMS4Q&s",
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/I%20Wanna%20Be%20Yours.mp3",
        "duration": "3:04",
        "description": "A song about expressing intense devotion and the desire to be completely committed to someone."
    },  

    {
        "id": 21,
        "title": "Take on Me",
        "album": "Hunting High and Low",
        "artist": "a-ha",
        "featured_artist": "None",
        "writers": "Pål Waaktaar-Savoy, Magne Furuholmen, and Morten Harket.",
        "producers": "Alan Tarney",
        "year": 1984,
        "genre": "Synth-pop",
        "language": "English",
        "popularity": "Over 2.94 billion streams on Spotify",
        "rating": "4.8/5",
        "spotify_url": "https://open.spotify.com/track/2WfaOiMkCvy7F5fcp2zZ8L?si=8eb58dd3fb6f42bf",
        "image_url": "https://i.pinimg.com/1200x/70/07/73/7007730a7ea2cf0c748b79784c109f05.jpg",
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/Take%20on%20Me%20(Video%20Version)%20(2015%20Remaster).mp3",
        "duration": "3:08",
        "description": "A song about taking a chance on love and encouraging someone to embrace a relationship despite uncertainty."
    },  

    {
        "id": 22,
        "title": "I Want You Back",
        "album": "None",
        "artist": "NSync",
        "featured_artist": "None",
        "writers": "Christian Lundin, Jake Schulze, and Andreas Carlsson",
        "producers": "Kristian Lundin",
        "year": 1996,
        "genre": "Pop",
        "language": "English",
        "popularity": "Over 500 million streams on Spotify",
        "rating": "4.7/5",
        "spotify_url": "https://open.spotify.com/track/221LRlPHPuevgE1tuUlof9?si=d1d1fdaec628495c",
        "image_url": "https://i.pinimg.com/736x/10/78/d5/1078d58cd97f1663ab2de36a5272836d.jpg",
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/I%20Want%20You%20Back%20-%20N%20Sync.mp3",
        "duration": "3:22",
        "description": "A song about regretting a breakup and desperately wanting a former lover to come back."
    },  

        {
        "id": 23,
        "title": "Kabisado",
        "album": "Andalucia",
        "artist": "IV OF SPADES",
        "featured_artist": "None",
        "writers": "Blaster Silonga",
        "producers": "IV OF SPADES and Brian Lotho",
        "year": 2025,
        "genre": "OPM",
        "language": "Tagalog",
        "popularity": "Over 76 million streams on Spotify",
        "rating": "4.8/5",
        "spotify_url": "https://open.spotify.com/track/4z928BtE4j1bjhcX9RU44M?si=6d0683e914584a8d",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQDYRAMiOdWsVE_7YpL_ECQR0PgcwgSuGbjne8hzwQePQ&s",
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/IV%20Of%20Spades%20-%20Kabisado%20(Lyrics).mp3",
        "duration": "3:27",
        "description": "A song about being deeply captivated by someone and knowing every detail about them by heart."
    },  

    {
        "id": 24,
        "title": "Paths",
        "album": "BUZZ",
        "artist": "NIKI",
        "featured_artist": "None",
        "writers": "Nicole Zefanya",
        "producers": "NIKI and Ethan Gruska",
        "year": 2024,
        "genre": "R&B",
        "language": "English",
        "popularity": "Over 38 million streams on Spotify",
        "rating": "4.8/5",
        "spotify_url": "https://open.spotify.com/track/68FHdrL6dbruEBrfLjR52a?si=08181e4e3a1c4782",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcThbr2siRDj88MWFOBxDgkkiPYglVGnVSPDOo885kF24w&s",
        "audio_url": "https://leoaffooarcmfqnrjcqu.supabase.co/storage/v1/object/public/songs/NIKI%20-%20Paths%20(Official%20Lyric%20Video).mp3",
        "duration": "3:09",
        "description": " song about the pain of a relationship ending and hoping that two people will cross paths again someday."
    },  
    
]

# validate the starting dataset when the application launches
validated_songs = [Song(**song).model_dump() for song in songs]
songs = validated_songs

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


# SEARCH SONG
@app.get("/api/v1/songs/search", dependencies=[Depends(verify_api_key)])
def search_songs(q: str = Query(..., min_length=0),
    sort: str = "" ):

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

        if q == "" or q in searchable_text:
            results.append(song)

# SORTING
    if sort == "az":
        results.sort(
            key=lambda x: x["title"].lower()
        )

    elif sort == "date":
        results.sort(
            key=lambda x: x["year"],
            reverse=True
        )

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

# HEALTH CHECK (Public)
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "NOTENOUGH Music API",
        "version": API_VERSION,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

# GET ALL SONGS(Protected)
@app.get("/api/v1/songs", dependencies=[Depends(verify_api_key)])
def get_songs():
    return {
        "count": len(songs),
        "songs": songs
    }

# GET ONE SONG (Protected)
@app.get("/api/v1/songs/{song_id}", dependencies=[Depends(verify_api_key)])
def get_song(song_id: int):
    for song in songs:
        if song["id"] == song_id:
            return song

    raise HTTPException(
        status_code=404,
        detail="Song not found."
    )
