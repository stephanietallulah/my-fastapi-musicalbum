import os
import bcrypt
import jwt
from fastapi import FastAPI, HTTPException, Header, Query, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv(override=True)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# configuration 
API_KEY = os.getenv("API_KEY")
API_VERSION = "1.0"

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"

# API KEY AUTHENTICATION
def verify_api_key(x_api_key: Optional[str] = Header(default=None)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key."
        )
    return True

# JWT TOKEN AUTHENTICATION
security = HTTPBearer()

def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Authentication token has expired."
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token."
        )

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

def verify_admin(user=Depends(verify_token)):
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required."
        )

    return user

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
    mood: list[str]
    energy: str
    vibe: list[str]
    best_for: list[str]
    duration: str = Field(min_length=1)
    description: str = Field(min_length=1)

# SONG UPDATE MODEL // for patch; to update one or few fields only
class SongUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    album: Optional[str] = None
    artist: Optional[str] = Field(default=None, min_length=1)
    featured_artist: Optional[str] = None
    writers: Optional[str] = None
    producers: Optional[str] = None
    year: Optional[int] = Field(default=None, ge=1900, le=2100)
    genre: Optional[str] = Field(default=None, min_length=1)
    language: Optional[str] = None
    popularity: Optional[str] = None
    rating: Optional[str] = Field(default=None, min_length=1)
    spotify_url: Optional[str] = None
    image_url: Optional[str] = None
    audio_url: Optional[str] = None
    mood: Optional[list[str]] = None
    energy: Optional[str] = None
    vibe: Optional[list[str]] = None
    best_for: Optional[list[str]] = None
    duration: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)

# USER REGISTRATION MODEL
class UserRegister(BaseModel):
    username: str = Field(min_length=1)
    email: str = Field(min_length=3)
    password: str = Field(min_length=6)

class UserLogin(BaseModel):
    email: str = Field(min_length=3)
    password: str = Field(min_length=1)

class SongCreate(BaseModel):
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
    mood: list[str]
    energy: str
    vibe: list[str]
    best_for: list[str]
    duration: str = Field(min_length=1)
    description: str = Field(min_length=1)

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

# REGISTER USER
@app.post("/api/v1/register")
def register_user(user: UserRegister):

    try:
        # Check if username already exists
        existing_username = (
            supabase
            .table("user")
            .select("user_id")
            .eq("username", user.username)
            .execute()
        )

        if existing_username.data:
            raise HTTPException(
                status_code=409,
                detail="Username already exists."
            )

        # Check if email already exists
        existing_email = (
            supabase
            .table("user")
            .select("user_id")
            .eq("email", user.email)
            .execute()
        )

        if existing_email.data:
            raise HTTPException(
                status_code=409,
                detail="Email already exists."
            )

        # Hash password
        password_hash = bcrypt.hashpw(
            user.password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        # Insert user
        response = (
            supabase
            .table("user")
            .insert({
                "username": user.username,
                "email": user.email,
                "password_hash": password_hash,
                "role": "user"
            })
            .execute()
        )

        return {
            "message": "User registered successfully.",
            "user": {
                "user_id": response.data[0]["user_id"],
                "username": response.data[0]["username"],
                "email": response.data[0]["email"],
                "role": response.data[0]["role"]
            }
        }

    except HTTPException:
        raise

    except Exception as e:
        print("REGISTER ERROR:", e)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to register user: {str(e)}"
        )

# LOGIN USER
@app.post("/api/v1/login")
def login_user(user: UserLogin):

    try:

        response = (
            supabase
            .table("user")
            .select("user_id, username, email, password_hash, role")
            .eq("email", user.email)
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password."
            )

        account = response.data[0]

        password_matches = bcrypt.checkpw(
            user.password.encode("utf-8"),
            account["password_hash"].encode("utf-8")
        )

        if not password_matches:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password."
            )

        token = jwt.encode(
            {
                "user_id": account["user_id"],
                "username": account["username"],
                "email": account["email"],
                "role": account["role"]
            },
            JWT_SECRET,
            algorithm=JWT_ALGORITHM
        )

        return {
            "message": "Login successful.",
            "token": token,
            "user": {
                "user_id": account["user_id"],
                "username": account["username"],
                "email": account["email"],
                "role": account["role"]
            }
        }
    except HTTPException:
        raise

    except Exception as e:

        print("LOGIN ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail="Login failed."
        )

# SEARCH SONG
@app.get("/api/v1/songs/search", dependencies=[Depends(verify_api_key)])
def search_songs(
    q: str = Query(..., min_length=1),
    sort: str = ""
):
    try:
        response = (
            supabase
            .table("songs")
            .select("*")
            .execute()
        )

        songs = response.data
        keyword = q.lower()

        results = []

        for song in songs:
            searchable_text = " ".join([
                str(song.get("title", "")),
                str(song.get("album", "")),
                str(song.get("artist", "")),
                str(song.get("featured_artist", "")),
                str(song.get("writers", "")),
                str(song.get("producers", "")),
                str(song.get("genre", "")),
                str(song.get("language", "")),
                str(song.get("popularity", "")),
                str(song.get("energy", "")),
                str(song.get("duration", "")),
                str(song.get("description", "")),
                " ".join(song.get("mood", [])),
                " ".join(song.get("vibe", [])),
                " ".join(song.get("best_for", [])),
                str(song.get("year", ""))
            ]).lower()

            if keyword in searchable_text:
                results.append(song)

        if sort == "az":
            results.sort(key=lambda x: x["title"].lower())

        elif sort == "date":
            results.sort(key=lambda x: x["year"], reverse=True)

        return {
            "query": q,
            "count": len(results),
            "results": results
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to search songs: {str(e)}"
        )

# GET ONE SONG
@app.get("/api/v1/songs/{song_id}", dependencies=[Depends(verify_api_key)])
def get_song(song_id: int):

    try:
        response = (
            supabase
            .table("songs")
            .select("*")
            .eq("id", song_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=404,
                detail="Song not found."
            )

        return response.data[0]

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch song."
        )

# GET ALL SONGS (Protected)
@app.get("/api/v1/songs", dependencies=[Depends(verify_api_key)])
def get_songs():
    try:
        response = supabase.table("songs").select("*").execute()
        songs_data = response.data
        return {
            "count": len(songs_data),
            "songs": songs_data
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch songs from database: {str(e)}"
        )

# CREATE SONG
@app.post(
    "/api/v1/songs",
    status_code=201,
    dependencies=[Depends(verify_token)]
)
def create_song(song: Song):

    try:
        existing = (
            supabase
            .table("songs")
            .select("id")
            .eq("id", song.id)
            .execute()
        )

        if existing.data:
            raise HTTPException(
                status_code=409,
                detail="A song with this ID already exists."
            )

        response = (
            supabase
            .table("songs")
            .insert(song.model_dump())
            .execute()
        )

        return {
            "message": "Song created successfully.",
            "song": response.data[0]
        }

    except HTTPException:
        raise

    except Exception as e:
        print("CREATE SONG ERROR:", e)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create song: {str(e)}"
    )

# UPDATE SONG
@app.patch(
    "/api/v1/songs/{song_id}",
    dependencies=[Depends(verify_token)]
)
def update_song(
    song_id: int,
    song: SongUpdate
):

    try:
        existing = (
            supabase
            .table("songs")
            .select("id")
            .eq("id", song_id)
            .execute()
        )

        if not existing.data:
            raise HTTPException(
                status_code=404,
                detail="Song not found."
            )

        update_data = song.model_dump(
            exclude_unset=True
        )

        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="No fields were provided for update."
            )

        response = (
            supabase
            .table("songs")
            .update(update_data)
            .eq("id", song_id)
            .execute()
        )

        return {
            "message": "Song updated successfully.",
            "song": response.data[0]
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to update song."
        )

# DELETE SONG
@app.delete(
    "/api/v1/songs/{song_id}",
    dependencies=[Depends(verify_token)]
)
def delete_song(song_id: int):

    try:
        existing = (
            supabase
            .table("songs")
            .select("id")
            .eq("id", song_id)
            .execute()
        )

        if not existing.data:
            raise HTTPException(
                status_code=404,
                detail="Song not found."
            )

        supabase \
            .table("songs") \
            .delete() \
            .eq("id", song_id) \
            .execute()

        return {
            "message": "Song deleted successfully.",
            "song_id": song_id
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to delete song."
        )

# TEST JWT TOKEN
@app.get("/api/v1/test-auth")
def test_auth(user=Depends(verify_token)):
    return {
        "message": "Token is valid.",
        "user": user
    }

@app.post(
    "/api/v1/admin/songs",
    status_code=201
)
def admin_create_song(
    song: SongCreate,
    user=Depends(verify_admin)
):
    try:

        response = (
            supabase
            .table("songs")
            .insert({
                "title": song.title,
                "album": song.album,
                "artist": song.artist,
                "featured_artist": song.featured_artist,
                "writers": song.writers,
                "producers": song.producers,
                "year": song.year,
                "genre": song.genre,
                "language": song.language,
                "popularity": song.popularity,
                "rating": song.rating,
                "spotify_url": song.spotify_url,
                "image_url": song.image_url,
                "audio_url": song.audio_url,
                "mood": song.mood,
                "energy": song.energy,
                "vibe": song.vibe,
                "best_for": song.best_for,
                "duration": song.duration,
                "description": song.description
            })
            .execute()
        )

        return {
            "message": "Song added successfully.",
            "song": response.data[0]
        }

    except Exception as e:

        print("ADMIN CREATE SONG ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail=f"Failed to add song: {str(e)}"
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
