const API_URL = "https://my-fastapi-musicalbum.vercel.app";
const API_KEY = "student-api-key-123";
let currentAudio = null;
let currentCard = null;
let currentButton = null;

const FETCH_OPTIONS = {
    headers: { "x-api-key": API_KEY}
};

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
    songs.forEach(song => {
        const card = document.createElement("div");
        card.className = "song-card";
        card.innerHTML = `
            <div class="image-container">
                <img src="${song.image_url}" alt="${song.title}">
            </div>
            <div class="song-info">
                <p class="song-year">${song.year}</p>
                <h3>${song.title}</h3>
                <p>${song.artist}</p>
                <p class="song-album">${song.album}</p>
                <p class="song-genre">${song.genre}</p>
               <div class="song-actions">
                <button onclick="viewSong(${song.id})"> Preview </button>
                <button class="play-btn"  onclick="playSong('${song.audio_url}', this)"> ▶ </button>
</div>
            </div>
        `;
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
        song.popularity.replace("Over ", "");

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

// SEARCH
async function searchSongs() {

    const query =
    document.getElementById("searchInput").value;
    const sort =
    document.getElementById("sortFilter").value;

    try {

        const response = await fetch(`${API_URL}/api/v1/songs/search?q=${encodeURIComponent(query || " ")}&sort=${sort}`, FETCH_OPTIONS);
        const data = await response.json();

        displaySongs(data.results);

    }

    catch(error){
        console.error(error);
        alert("Search failed.");
    }
}


// CLOSE PREVIEW POPUP
document
.querySelector(".preview-close")
.addEventListener("click", function(){
    document.querySelector(".song-preview-overlay")
    .style.display = "none";
});

// ROTATION OF THE IMAGE 
function togglePlay(button){
    const card = button.closest(".song-card");
    card.classList.toggle("playing");
    if(card.classList.contains("playing")){
        button.innerHTML = "❚❚";
    } else {
        button.innerHTML = "▶";
    }
}

// MUSIC 
function playSong(url, button) {
    const card = button.closest(".song-card");
    const audio = document.getElementById("audioPlayer");

    // STOP PREVIOUS SONG
    if(currentAudio && currentAudio !== audio){
        currentAudio.pause();
    }

    if(currentCard && currentCard !== card){
        currentCard.classList.remove("playing");
    }

    if(currentButton && currentButton !== button){
        currentButton.innerHTML = "▶";
    }

// will pause if u click a new song
    if(card.classList.contains("playing")){
        audio.pause();
        card.classList.remove("playing");
        button.innerHTML = "▶";
        currentAudio = null;
        currentCard = null;
        currentButton = null;
    }

// will play a new song
    else {
    audio.src = url;
    audio.play();

    card.classList.add("playing");
    button.innerHTML = "❚❚";

    currentAudio = audio;
    currentCard = card;
    currentButton = button;


// will stop the spinning of the image when the music is done
    audio.onended = function() {
        card.classList.remove("playing");
        button.innerHTML = "▶";

        currentAudio = null;
        currentCard = null;
        currentButton = null;
    };
}
}

function showAllSongs(){
    document.getElementById("searchInput").value = "";
    document.getElementById("sortFilter").value = "";
    loadSongs();
}

document
    .getElementById("sortFilter")
    .addEventListener("change", function() {
        searchSongs();
    });

// enter button
document
    .getElementById("searchInput")
    .addEventListener("keydown", function(event) {

        if (event.key === "Enter") {
            searchSongs();
        }

    });

loadSongs();