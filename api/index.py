const API_URL = "https://my-fastapi-musicalbum.vercel.app";


// GET ALL SONGS
async function loadSongs() {
    try {
        const response = await fetch(`${API_URL}/songs`);
        const data = await response.json();
        displaySongs(data.songs);
    }

    catch (error) {
        console.error(error);
        document.getElementById("songList").innerHTML = "Unable to connect to the API.";
    }
}


// DISPLAY SONGS
function displaySongs(songs) {
    const songList =
        document.getElementById("songList");

    songList.innerHTML = "";

    songs.forEach(song => {
        const card = document.createElement("div");
        card.className = "song-card";
        card.innerHTML = `
            <div class="song-year">${song.year}</div>
            <h3>${song.artist} - ${song.title}</h3>
            <p class="song-album">${song.album}</p>
            <p>${song.genre}</p>
            <p>${song.duration}</p>
            <p>${song.description}</p>
            <button onclick="viewSong(${song.id})"> View Details</button>
            <a href="${song.spotify_url}" 
                   target="_blank" 
                   class="spotify-button">
                    ▶ Play on Spotify
                </a>
        `;

        songList.appendChild(card);
    });

}

// DISPLAY IMAGES
function displaySongs(songs) {
    const songList = document.getElementById("songList");

    songList.innerHTML = "";

    songs.forEach(song => {
        const card = document.createElement("div");

        card.className = "song-card";

        card.innerHTML = `
            <img src="./coverphoto.jpeg" alt="Never Enough album cover">

            <p class="song-year">${song.year}</p>
            <h3>${song.title}</h3>
            <p>${song.artist}</p>
            <p class="song-album">${song.album}</p>
            <p>${song.description}</p>
            <button onclick="viewSong(${song.id})">
                View Song
            </button>
        `;

        songList.appendChild(card);
    });
}

// GET ONE SONG
async function viewSong(id) {

    try {
        const response = await fetch(`${API_URL}/songs/${id}`);
        const song = await response.json();

        alert(`
            ${song.artist} - ${song.title}
            Album:
            ${song.album}

            Genre:
            ${song.genre}

            Duration:
            ${song.duration}

            Description:
            ${song.description}
        `);
    }
    catch (error) {
        console.error(error);
        alert("Unable to retrieve song.");
    }

}

// SEARCH
async function searchSongs() {

    const query = document.getElementById("searchInput").value;
    if (!query) {
        loadSongs();
        return;
    }
    try {
        const response =
            await fetch(`${API_URL}/songs/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        displaySongs(data.results);
    }

    catch (error) {
        console.error(error);
        alert("Search failed.");
    }
}

loadSongs();


