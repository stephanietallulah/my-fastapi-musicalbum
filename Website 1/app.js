const API_URL = "https://my-fastapi-musicalbum.vercel.app";
const API_KEY = "api-key-one";
let currentAudio = null;
let currentCard = null;
let currentButton = null;

const FETCH_OPTIONS = {
    headers: { "x-api-key": API_KEY}
};

window.addEventListener("scroll", function () {
    const header = document.querySelector(".landing-header");
    if (window.scrollY > 10) {
        header.classList.add("scrolled");
    } else {
        header.classList.remove("scrolled");
    }
});

// GET ALL SONGS
async function loadSongs() {
    try {
        const response = await fetch(`${API_URL}/api/v1/songs`, FETCH_OPTIONS);
        const data = await response.json();
        displaySongs(data.songs);
    }

    catch (error) {
        console.error(error);
        document.getElementById("songList").innerHTML = "Unable to connect to the API.";
    }
}

// DISPLAY IMAGES
function displaySongs(songs) {
    const songList = document.getElementById("songList");

    songList.innerHTML = "";

    // Show only 3 songs on the landing page
    songs.slice(0, 3).forEach(song => {

        const card = document.createElement("article");
        card.className = "landing-song-card";

        card.innerHTML = `
            <div class="landing-song-image">

                <div class="vinyl-disc"></div>

                <img src="${song.image_url}" alt="${song.title}">

                <button class="landing-play-button">
                    ▶
                </button>

            </div>

            <div class="landing-song-overlay">

                <h3>${song.title}</h3>

                <p>${song.artist}</p>

            </div>
        `;

        const playButton = card.querySelector(".landing-play-button");

        playButton.addEventListener("click", function(event) {
            event.stopPropagation();
            playSong(song.audio_url, playButton);
        });

        card.addEventListener("click", function() {
            viewSong(song.id);
        });

        songList.appendChild(card);
    });
}


// GET ONE SONG
async function viewSong(id) {
    try {
        const response = await fetch(`${API_URL}/api/v1/songs/${id}`, FETCH_OPTIONS);
        const song = await response.json();

        // LEFT SIDE DATA
        document.getElementById("modalImage").src =
        song.image_url;

        document.getElementById("previewYear").textContent =
            song.year;

        document.getElementById("previewTitle").textContent =
            song.title;

        document.getElementById("previewArtist").textContent =
            song.artist;

        document.getElementById("previewAlbum").textContent =
            song.album;
        
        document.getElementById("previewRating").textContent =
            song.rating;

        document.getElementById("previewStreams").textContent =
            song.popularity
                .replace(/^Over\s+/i, "")
                .replace(/\s*(of\s+)?streams\s+on\s+Spotify/i, "");

        // RIGHT SIDE DATA
        document.getElementById("previewAlbumInfo").textContent =
            song.album;

        document.getElementById("previewFeatured").textContent =
            song.featured_artist || "None";

        document.getElementById("previewWriters").textContent =
            song.writers || "Not available";

        document.getElementById("previewProducers").textContent =
            song.producers || "Not available";

        document.getElementById("previewGenre").textContent =
            song.genre;

        document.getElementById("previewLanguage").textContent =
            song.language || "English";

        document.getElementById("previewDuration").textContent =
            song.duration;

        document.getElementById("previewPopularity").textContent =
            song.popularity || "Not available";

        document.getElementById("previewDescription").textContent =
            song.description;
        
        document.getElementById("spotifyButton").onclick = function() {

            window.open(
                song.spotify_url,
                "_blank"
            );

};

// SHOW POPUP
        document.querySelector(".song-preview-overlay")
        .style.display = "flex";
    }

    catch(error){
        console.error(error);
        alert("Unable to retrieve song.");
    }

}

// CLOSE PREVIEW POPUP
document
.querySelector(".preview-close")
.addEventListener("click", function(){
    document.querySelector(".song-preview-overlay")
    .style.display = "none";
});



// MUSIC 
function playSong(url, button) {
    const card = button.closest(".landing-song-card");
    const audio = document.getElementById("audioPlayer");

    // Stop previous card animation & button
    if (currentCard && currentCard !== card) {
        currentCard.classList.remove("playing");
    }
    if (currentButton && currentButton !== button) {
        currentButton.innerHTML = "▶";
    }

    // Pause if clicking the currently playing song
    if (card.classList.contains("playing")) {
        if (audio) audio.pause();
        card.classList.remove("playing");
        button.innerHTML = "▶";
        currentAudio = null;
        currentCard = null;
        currentButton = null;
    } else {
        // Start spinning immediately on click
        card.classList.add("playing");
        button.innerHTML = "❚❚";

        if (audio && url) {
            audio.src = url;
            audio.play().catch(err => console.warn("Audio playback issue:", err));

            audio.onended = function () {
                card.classList.remove("playing");
                button.innerHTML = "▶";
                currentAudio = null;
                currentCard = null;
                currentButton = null;
            };
        }

        currentAudio = audio;
        currentCard = card;
        currentButton = button;
    }
}

loadSongs();