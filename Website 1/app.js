const API_URL = "https://my-fastapi-musicalbum.vercel.app";
const API_KEY = "api-key-one";
let currentAudio = null;
let currentCard = null;
let currentButton = null;
let allSongs = [];
let userFavorites = [];
let selectedSongForPlaylist = null;


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



// Helper: fetch songs once and cache in memory
async function getSongs(forceRefresh = false) {
    if (allSongs.length > 0 && !forceRefresh) {
        return allSongs;
    }
    const response = await fetch(`${API_URL}/api/v1/songs`, FETCH_OPTIONS);
    if (!response.ok) throw new Error("Failed to load songs.");
    const data = await response.json();
    allSongs = data.songs || [];
    return allSongs;
}


async function loadSongs() {
    const songList = document.getElementById("songList");

    if (!songList) return;

    if (allSongs.length === 0) {
        songList.innerHTML =
            `<p class="loading-songs">Loading songs...</p>`;
    }

    try {
        const songs = await getSongs();

        // Display songs immediately
        displaySongs(songs);

        // Update favorites separately
        loadFavorites().then(() => {
            displaySongs(allSongs);
        });

    } catch (error) {
        console.error("Song loading error:", error);
        songList.innerHTML =
            "Unable to connect to the API.";
    }
}


// LOAD USER FAVORITES
async function loadFavorites() {
    const token = localStorage.getItem("notenoughToken");

    if (!token) {
        userFavorites = [];
        return;
    }

    try {
        const response = await fetch(`${API_URL}/api/v1/favorites`, {
            headers: {
                "x-api-key": API_KEY,
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) throw new Error("Failed to load favorites.");

        const data = await response.json();
        userFavorites = data.favorites.map(favorite => String(favorite.song_id));
    } catch (error) {
        console.error("Unable to load favorites:", error);
        userFavorites = [];
    }
}

async function showFavoriteSongs() {
    const token = localStorage.getItem("notenoughToken");

    if (!token) {
        window.location.href = "login.html";
        return;
    }

    try {
        const [songs] = await Promise.all([
            getSongs(),
            loadFavorites()
        ]);

        const favoriteSongs = songs.filter(song =>
            userFavorites.includes(String(song.id))
        );

        displaySongs(favoriteSongs);
    } catch (error) {
        console.error("Unable to load favorite songs:", error);
    }
}

// DISPLAY SONGS
function displaySongs(songs) {
    const songList = document.getElementById("songList");
    songList.innerHTML = "";

    const token = localStorage.getItem("notenoughToken");

    const songsToDisplay = token ? songs : songs.slice(0, 4);

    songsToDisplay.forEach(song =>  {
        const card = document.createElement("article");
        card.className = "landing-song-card";

        const isFav = userFavorites.includes(String(song.id));

        card.innerHTML = `
            <div class="landing-song-image">
                <div class="vinyl-disc"></div>

                <img src="${song.image_url}" alt="${song.title}">

                <button
                    type="button"
                    class="favorite-button ${isFav ? "active" : ""}"
                    data-song-id="${song.id}"
                >
                    <svg class="heart-icon" viewBox="0 0 24 24">
                        <path d="M12 20.5C12 20.5 3.5 15.1 3.5 8.8C3.5 5.9 5.8 3.8 8.5 3.8C10.2 3.8 11.4 4.6 12 5.7C12.6 4.6 13.8 3.8 15.5 3.8C18.2 3.8 20.5 5.9 20.5 8.8C20.5 15.1 12 20.5 12 20.5Z" />
                    </svg>
                </button>

                <button type="button" class="landing-play-button">▶</button>

                <button
                    type="button"
                    class="playlist-button"
                    data-song-id="${song.id}"
                >
                    + Playlist
                </button>
            </div>

            <div class="landing-song-overlay">
                <h3>${song.title}</h3>
                <p>${song.artist}</p>
            </div>
        `;

        // FAVORITE BUTTON
        const favButton = card.querySelector(".favorite-button");

        favButton.addEventListener("click", function (event) {
            event.stopPropagation();
            toggleFavorite(favButton, song.id);
        });

        // PLAY BUTTON
        const playButton = card.querySelector(".landing-play-button");

        playButton.addEventListener("click", function (event) {
            event.stopPropagation();
            playSong(song.audio_url, playButton);
        });

        // ADD THIS
        const playlistButton = card.querySelector(".playlist-button");

        playlistButton.addEventListener("click", function (event) {
            event.stopPropagation();
            openPlaylistMenu(song.id);
        });

        // SONG CARD
        card.addEventListener("click", function () {
            viewSong(song.id);
        });

        songList.appendChild(card);
    });
}



// LOAD USER PLAYLISTS
async function loadPlaylists() {
    const token = localStorage.getItem("notenoughToken");

    if (!token) {
        window.location.href = "login.html";
        return [];
    }

    try {
        const response = await fetch(`${API_URL}/api/v1/playlists`, {
            headers: {
                "x-api-key": API_KEY,
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error("Failed to load playlists.");
        }

        const data = await response.json();

        return data.playlists || [];

    } catch (error) {
        console.error("Playlist error:", error);
        alert("Unable to load playlists.");
        return [];
    }
}

async function showPlaylists() {

    const playlists = await loadPlaylists();

    const songList = document.getElementById("songList");

    songList.innerHTML = "";

    if (playlists.length === 0) {
        songList.innerHTML = `
            <p class="no-playlists">
                You don't have any playlists yet.
            </p>
        `;
        return;
    }

    playlists.forEach(playlist => {

        const playlistCard = document.createElement("div");

        playlistCard.className = "playlist-card";

        playlistCard.innerHTML = `
            <div class="playlist-card-content">
                <span class="playlist-icon">♫</span>

                <div class="playlist-info">
                    <h3>${playlist.name}</h3>
                    <p>${playlist.description || "No description"}</p>
                </div>

                <button
                    type="button"
                    class="delete-playlist-button"
                    aria-label="Delete playlist"
                    title="Delete playlist"
                >
                    🗑
                </button>
            </div>
        `;

        const deleteButton = playlistCard.querySelector(".delete-playlist-button");

        deleteButton.addEventListener("click", function (event) {
            event.stopPropagation(); // Prevents opening the playlist when clicking delete
            deletePlaylist(playlist.playlist_id, playlist.name);
        });

        playlistCard.addEventListener("click", function () {
            showPlaylistSongs(playlist.playlist_id, playlist.name);
        });

        songList.appendChild(playlistCard);
    });
}

// CUSTOM CONFIRMATION MODAL HELPER
function openConfirmModal({ title, message, confirmText = "Delete" }) {
    return new Promise((resolve) => {
        const modal = document.getElementById("confirmModal");
        const titleEl = document.getElementById("confirmModalTitle");
        const messageEl = document.getElementById("confirmModalMessage");
        const proceedBtn = document.getElementById("confirmProceedButton");
        const cancelBtn = document.getElementById("confirmCancelButton");
        const closeBtn = document.getElementById("confirmModalClose");

        if (!modal) {
            resolve(window.confirm(message));
            return;
        }

        titleEl.textContent = title;
        messageEl.textContent = message;
        proceedBtn.textContent = confirmText;
        modal.style.display = "flex";

        const cleanup = (result) => {
            modal.style.display = "none";
            proceedBtn.removeEventListener("click", onProceed);
            cancelBtn.removeEventListener("click", onCancel);
            closeBtn.removeEventListener("click", onCancel);
            modal.removeEventListener("click", onBackdrop);
            resolve(result);
        };

        const onProceed = () => cleanup(true);
        const onCancel = () => cleanup(false);
        const onBackdrop = (event) => {
            if (event.target === modal) cleanup(false);
        };

        proceedBtn.addEventListener("click", onProceed);
        cancelBtn.addEventListener("click", onCancel);
        closeBtn.addEventListener("click", onCancel);
        modal.addEventListener("click", onBackdrop);
    });
}

// DELETE PLAYLIST
async function deletePlaylist(playlistId, playlistName) {
    const token = localStorage.getItem("notenoughToken");

    if (!token) {
        window.location.href = "login.html";
        return;
    }

    const confirmed = await openConfirmModal({
        title: "Delete Playlist?",
        message: `Are you sure you want to delete "${playlistName}"? All songs inside this playlist will be removed.`,
        confirmText: "Delete Playlist"
    });
    if (!confirmed) return;

    try {
        const response = await fetch(
            `${API_URL}/api/v1/playlists/${playlistId}`,
            {
                method: "DELETE",
                headers: {
                    "x-api-key": API_KEY,
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            const errData = await response.json().catch(() => ({}));
            throw new Error(errData.detail || "Failed to delete playlist.");
        }

        showToast(`Deleted "${playlistName}".`, "success");
        showPlaylists();

    } catch (error) {
        console.error("Delete playlist error:", error);
        showToast(error.message || "Unable to delete playlist.", "error");
    }
}

// ADMIN: DELETE SONG
async function deleteSong(songId, songTitle) {
    const token = localStorage.getItem("notenoughToken");

    if (!token) {
        window.location.href = "login.html";
        return;
    }

    const confirmed = confirm(`Are you sure you want to permanently delete "${songTitle}"?`);
    if (!confirmed) return;

    try {
        const response = await fetch(
            `${API_URL}/api/v1/songs/${songId}`,
            {
                method: "DELETE",
                headers: {
                    "x-api-key": API_KEY,
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw new Error(data.detail || "Failed to delete song.");
        }

        // Close preview modal
        const overlay = document.querySelector(".song-preview-overlay");
        if (overlay) overlay.style.display = "none";

        showToast(`Deleted "${songTitle}".`, "success");

        // Refresh song list
        await getSongs(true);
        const songFilter = document.getElementById("song-filter");
        if (songFilter && songFilter.value === "favorites") {
            showFavoriteSongs();
        } else {
            loadSongs();
        }
    } catch (error) {
        console.error("Delete song error:", error);
        showToast(error.message || "Unable to delete song.", "error");
    }
}

async function showPlaylistSongs(playlistId, playlistName) {

    const token = localStorage.getItem("notenoughToken");

    if (!token) {
        window.location.href = "login.html";
        return;
    }

    try {

        const [playlistResponse, songs] = await Promise.all([
            fetch(`${API_URL}/api/v1/playlists/${playlistId}/songs`, {
                headers: {
                    "x-api-key": API_KEY,
                    "Authorization": `Bearer ${token}`
                }
            }),
            getSongs()
        ]);

        if (!playlistResponse.ok) {
            throw new Error("Failed to load playlist songs.");
        }

        const playlistData = await playlistResponse.json();

        const playlistSongIds = playlistData.songs.map(song =>
            String(song.song_id)
        );

        const playlistSongs = songs.filter(song =>
            playlistSongIds.includes(String(song.id))
        );

        document.getElementById("songSectionTitle").textContent =
            playlistName;

        document.getElementById("backToPlaylistsButton").style.display =
            "inline-flex";

        displaySongs(playlistSongs);

    } catch (error) {

        console.error("Playlist songs error:", error);
        alert("Unable to load playlist songs.");

    }
}


// OPEN PLAYLIST MENU
async function openPlaylistMenu(songId) {
    const token = localStorage.getItem("notenoughToken");

    if (!token) {
        window.location.href = "login.html";
        return;
    }

    const playlists = await loadPlaylists();

    selectedSongForPlaylist = songId;

    const playlistList = document.getElementById("playlistList");
    playlistList.innerHTML = "";

    if (playlists.length === 0) {
        playlistList.innerHTML = `
            <p class="no-playlists">
                You don't have any playlists yet.
            </p>
        `;
    } else {
        playlists.forEach(playlist => {

            const button = document.createElement("button");

            button.className = "playlist-item";
            button.textContent = playlist.name;

            button.addEventListener("click", async function () {

                await addSongToPlaylist(
                    playlist.playlist_id,
                    selectedSongForPlaylist
                );

                closePlaylistModal();
            });

            playlistList.appendChild(button);
        });
    }

    document.getElementById("playlistModal").style.display = "flex";
}

// CLOSE PLAYLIST MODAL
function closePlaylistModal() {
    document.getElementById("playlistModal").style.display = "none";
    selectedSongForPlaylist = null;
}

const playlistModalClose = document.getElementById("playlistModalClose");
const playlistModal = document.getElementById("playlistModal");

if (playlistModalClose) {
    playlistModalClose.addEventListener("click", function () {
        closePlaylistModal();
    });
}

if (playlistModal) {
    playlistModal.addEventListener("click", function (event) {
        if (event.target === playlistModal) {
            closePlaylistModal();
        }
    });
}

// CREATE PLAYLIST
const createPlaylistButton = document.getElementById("createPlaylistButton");
const createPlaylistModal = document.getElementById("createPlaylistModal");
const createPlaylistClose = document.getElementById("createPlaylistClose");
const savePlaylistButton = document.getElementById("savePlaylistButton");

if (savePlaylistButton) {
    savePlaylistButton.addEventListener("click", createPlaylist);
}

if (createPlaylistButton) {
    createPlaylistButton.addEventListener("click", function () {

        // Close Add to Playlist modal
        playlistModal.style.display = "none";

        // Open Create Playlist modal
        createPlaylistModal.style.display = "flex";

        document.getElementById("playlistNameInput").value = "";
        document.getElementById("playlistDescriptionInput").value = "";

    });
}

// function to create a new playlist
async function createPlaylist() {

    const token = localStorage.getItem("notenoughToken");

    if (!token) {
        window.location.href = "login.html";
        return;
    }

    const name = document.getElementById("playlistNameInput").value.trim();
    const description = document.getElementById("playlistDescriptionInput").value.trim();

    if (!name) {
        showToast("Please enter a playlist name.", "error");
        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/api/v1/playlists`,
            {
                method: "POST",
                headers: {
                    "x-api-key": API_KEY,
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: name,
                    description: description
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Failed to create playlist."
            );
        }

        createPlaylistModal.style.display = "none";

        showToast("Playlist created successfully!", "success");

        // Refresh playlist list
        const songFilter = document.getElementById("song-filter");

        if (songFilter && songFilter.value === "playlists") {
            showPlaylists();
        }

    } catch (error) {

        console.error("Create playlist error:", error);

        showToast(
            error.message || "Unable to create playlist.",
            "error"
        );
    }
}

// CLOSE CREATE PLAYLIST
if (createPlaylistClose) {
    createPlaylistClose.addEventListener("click", function () {

        createPlaylistModal.style.display = "none";

        // Open Add to Playlist modal again
        playlistModal.style.display = "flex";

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
        
        document.getElementById("spotifyButton").onclick = function () {
            window.open(
                song.spotify_url,
                "_blank"
            );
        };

        const deleteSongButton = document.getElementById("deleteSongButton");
        const currentUser = savedUser ? JSON.parse(savedUser) : null;

        if (deleteSongButton) {
            if (currentUser && savedToken && currentUser.role === "admin") {
                deleteSongButton.style.display = "inline-flex";
                deleteSongButton.onclick = function () {
                    deleteSong(song.id, song.title);
                };
            } else {
                deleteSongButton.style.display = "none";
                deleteSongButton.onclick = null;
            }
        }

        // SHOW POPUP
        document.querySelector(".song-preview-overlay")
            .style.display = "flex";
    } catch (error) {
        console.error(error);
        alert("Unable to retrieve song.");
    }
}

// CLOSE PREVIEW POPUP
const previewOverlay = document.querySelector(".song-preview-overlay");
const previewCloseButton = document.querySelector(".preview-close");

if (previewCloseButton && previewOverlay) {
    previewCloseButton.addEventListener("click", function (event) {
        event.stopPropagation();
        previewOverlay.style.display = "none";
    });

    // Also close when clicking the dark backdrop outside the modal card
    previewOverlay.addEventListener("click", function (event) {
        if (event.target === previewOverlay) {
            previewOverlay.style.display = "none";
        }
    });
}

// Close open popups with the Escape key
document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        const confirmModal = document.getElementById("confirmModal");
        if (confirmModal && confirmModal.style.display === "flex") {
            confirmModal.style.display = "none";
            return;
        }
        if (previewOverlay) previewOverlay.style.display = "none";
        closePlaylistModal();
        closeAdminModal();
    }
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

// PROFILE MENU
const profileButton = document.getElementById("profileButton");
const profileMenu = document.getElementById("profileMenu");
const profileUsername = document.getElementById("profileUsername");
const profileEmail = document.getElementById("profileEmail");
const logoutButton = document.getElementById("logoutButton");

const savedUser = localStorage.getItem("notenoughUser");
const savedToken = localStorage.getItem("notenoughToken");

const adminModal = document.getElementById("adminModal");
const adminModalClose = document.getElementById("adminModalClose");
const addSongButton = document.getElementById("addSongButton");

function closeAdminModal() {
    if (adminModal) {
        adminModal.style.display = "none";
    }
}

if (adminModalClose) {
    adminModalClose.addEventListener("click", closeAdminModal);
}

if (adminModal) {
    adminModal.addEventListener("click", function (event) {
        if (event.target === adminModal) {
            closeAdminModal();
        }
    });
}

if (savedUser && savedToken) {
    const user = JSON.parse(savedUser);

    if (user.role === "admin" && addSongButton) {
        addSongButton.style.display = "inline-flex";
        addSongButton.addEventListener("click", function () {
            if (adminModal) {
                adminModal.style.display = "flex";
                const titleInput = document.getElementById("adminTitle");
                if (titleInput) titleInput.focus();
            }
        });
    }
}

if (savedUser && savedToken) {

    const user = JSON.parse(savedUser);

    profileUsername.textContent = user.username;
    profileEmail.textContent = user.email;

    profileButton.addEventListener("click", function () {
        profileMenu.classList.toggle("show");
    });

    logoutButton.addEventListener("click", function () {
        localStorage.removeItem("notenoughUser");
        localStorage.removeItem("notenoughToken");

        window.location.href = "login.html";
    });

} else {

    profileButton.addEventListener("click", function () {
        window.location.href = "login.html";
    });

}

const adminSongForm = document.getElementById("adminSongForm");

if (adminSongForm) {

    adminSongForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const token = localStorage.getItem("notenoughToken");

        try {

            const response = await fetch(
                `${API_URL}/api/v1/admin/songs`,
                {
                    method: "POST",

                    headers: {
                        "x-api-key": API_KEY,
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({

                        title: document.getElementById("adminTitle").value,

                        album:
                            document.getElementById("adminAlbum").value || null,

                        artist:
                            document.getElementById("adminArtist").value,

                        featured_artist:
                            document.getElementById("adminFeaturedArtist").value || null,

                        writers:
                            document.getElementById("adminWriters").value,

                        producers:
                            document.getElementById("adminProducers").value,

                        year:
                            Number(document.getElementById("adminYear").value),

                        genre:
                            document.getElementById("adminGenre").value,

                        language:
                            document.getElementById("adminLanguage").value || null,

                        popularity:
                            document.getElementById("adminPopularity").value,

                        rating:
                            document.getElementById("adminRating").value,

                        spotify_url:
                            document.getElementById("adminSpotifyUrl").value,

                        image_url:
                            document.getElementById("adminImageUrl").value,

                        audio_url:
                            document.getElementById("adminAudioUrl").value,

                        mood:
                            document.getElementById("adminMood").value
                                .split(",")
                                .map(item => item.trim())
                                .filter(Boolean),

                        energy:
                            document.getElementById("adminEnergy").value,

                        vibe:
                            document.getElementById("adminVibe").value
                                .split(",")
                                .map(item => item.trim())
                                .filter(Boolean),

                        best_for:
                            document.getElementById("adminBestFor").value
                                .split(",")
                                .map(item => item.trim())
                                .filter(Boolean),

                        duration:
                            document.getElementById("adminDuration").value,

                        description:
                            document.getElementById("adminDescription").value

                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.detail || "Failed to add music."
                );
            }

            showToast("Music added successfully!", "success");

            adminSongForm.reset();
            closeAdminModal();

            await getSongs(true);
            loadSongs();

        } catch (error) {

            console.error("Admin music error:", error);

            showToast(
                error.message || "Unable to add music.",
                "error"
            );
        }

    });

}

// HIDE LOGIN AND SIGN UP BUTTONS WHEN LOGGED IN
const loginButton = document.getElementById("loginButton");
const signupButton = document.getElementById("signupButton");
const loginCTA = document.getElementById("loginCTA");

if (savedUser && savedToken) {
    if (loginButton) loginButton.style.display = "none";
    if (signupButton) signupButton.style.display = "none";
    if (loginCTA) loginCTA.style.display = "none";
}

let toastTimeout = null;

function showToast(message, type = "success") {
    const toast = document.getElementById("toastNotification");
    const toastMessage = document.getElementById("toastMessage");
    const toastIcon = document.getElementById("toastIcon");

    if (!toast || !toastMessage || !toastIcon) return;

    toastMessage.textContent = message;
    toast.classList.remove("success", "error");
    toast.classList.add(type, "show");
    toastIcon.textContent = type === "error" ? "!" : "✦";

    clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => {
        toast.classList.remove("show");
    }, 3000);
}

// ADD SONG TO PLAYLIST
async function addSongToPlaylist(playlistId, songId) {
    const token = localStorage.getItem("notenoughToken");

    if (!token) {
        window.location.href = "login.html";
        return;
    }

    try {
        const response = await fetch(
            `${API_URL}/api/v1/playlists/${playlistId}/songs`,
            {
                method: "POST",
                headers: {
                    "x-api-key": API_KEY,
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    song_id: songId
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            if (response.status === 409) {
                showToast("This song is already in the playlist.", "error");
                return;
            }

            throw new Error(data.detail || "Failed to add song.");
        }

        showToast("Song added to playlist!", "success");

    } catch (error) {
        console.error("Add to playlist error:", error);
        showToast("Unable to add song to playlist.", "error");
    }
}

// TOGGLE FAVORITE
async function toggleFavorite(button, songId) {
    const token = localStorage.getItem("notenoughToken");

    if (!token) {
        window.location.href = "login.html";
        return;
    }

    const isCurrentlyFavorite = button.classList.contains("active");

    try {
        const url = isCurrentlyFavorite
            ? `${API_URL}/api/v1/favorites/${songId}`
            : `${API_URL}/api/v1/favorites`;

        const options = isCurrentlyFavorite
            ? {
                  method: "DELETE",
                  headers: {
                      "x-api-key": API_KEY,
                      "Authorization": `Bearer ${token}`
                  }
              }
            : {
                  method: "POST",
                  headers: {
                      "x-api-key": API_KEY,
                      "Authorization": `Bearer ${token}`,
                      "Content-Type": "application/json"
                  },
                  body: JSON.stringify({
                      song_id: Number(songId)
                  })
              };

        const res = await fetch(url, options);

        if (res.status === 401) {
            localStorage.removeItem("notenoughToken");
            localStorage.removeItem("notenoughUser");
            window.location.href = "login.html";
            return;
        }

        if (!res.ok) {
            const errData = await res.json().catch(() => ({}));
            console.error("Favorites API error:", res.status, errData);
            throw new Error(errData.detail || `HTTP ${res.status}`);
        }

        if (isCurrentlyFavorite) {
            button.classList.remove("active");
            userFavorites = userFavorites.filter(id => id !== String(songId));
            showToast("Removed from favorites.", "success");
        } else {
            button.classList.add("active");
            if (!userFavorites.includes(String(songId))) {
                userFavorites.push(String(songId));
            }
            showToast("Added to favorites!", "success");
        }
    } catch (error) {
        console.error("Favorite error:", error);
        showToast(error.message || "Unable to update favorites.", "error");
    }
}

const backToPlaylistsButton = document.getElementById("backToPlaylistsButton");
const songFilter = document.getElementById("song-filter");

if (songFilter) {
    songFilter.addEventListener("change", function () {

        const selected = this.value;
        const title = document.getElementById("songSectionTitle");

        if (selected === "all") {

            title.textContent = "All Songs";

            if (backToPlaylistsButton) {
                backToPlaylistsButton.style.display = "none";
            }

            loadSongs();

        } else if (selected === "favorites") {

            title.textContent = "Favorites";

            if (backToPlaylistsButton) {
                backToPlaylistsButton.style.display = "none";
            }

            showFavoriteSongs();

        } else if (selected === "playlists") {

            title.textContent = "My Playlists";

            if (backToPlaylistsButton) {
                backToPlaylistsButton.style.display = "none";
            }

            showPlaylists();
        }
    });
}

if (backToPlaylistsButton) {
    backToPlaylistsButton.addEventListener("click", function () {

        document.getElementById("songSectionTitle").textContent =
            "My Playlists";

        backToPlaylistsButton.style.display = "none";

        showPlaylists();
    });
}