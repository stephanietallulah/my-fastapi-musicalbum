const API_URL = "https://my-fastapi-musicalbum.vercel.app";
const API_KEY = "api-key-one";

const FETCH_OPTIONS = {
    headers: {
        "x-api-key": API_KEY
    }
};

let allSongs = [];

const savedUser = localStorage.getItem("notenoughUser");
const savedToken = localStorage.getItem("notenoughToken");
const isLoggedIn = Boolean(savedUser && savedToken);

// load songs from api
async function loadSongs() {
    try {
        const response = await fetch(
            `${API_URL}/api/v1/songs`,
            FETCH_OPTIONS
        );

        const data = await response.json();

        allSongs = data.songs;

        console.log("Songs loaded:", allSongs);

        displayStatistics();
        displayTopSongs();

        const overviewSection = document.getElementById("overview");
        const genresSection = document.getElementById("genres");
        const guestStatsLock = document.getElementById("guestStatsLock");

        if (isLoggedIn) {
            if (guestStatsLock) guestStatsLock.style.display = "none";
            if (overviewSection) overviewSection.style.display = "block";
            if (genresSection) genresSection.style.display = "block";

            displaySongsByYear();
            displayGenreDistribution();
            loadGenreOptions();
        } else {
            if (guestStatsLock) guestStatsLock.style.display = "flex";
            if (overviewSection) overviewSection.style.display = "none";
            if (genresSection) genresSection.style.display = "none";
        }
    }

    catch (error) {
        console.error("API Error:", error);
    }
}

// statistics
function displayStatistics(){
    
    // total songs
    document.getElementById("totalsong").textContent = 
        allSongs.length;
    
    // total artists
    const artists = new Set(
        allSongs.map(song => song.artist)
    );

    document.getElementById("totalartist").textContent = artists.size;

    // average rating
    const ratings = allSongs
        .map(song => parseFloat(song.rating))
        .filter(rating => !isNaN(rating));
    
    const averageRating =
        ratings.reduce((sum, rating) => sum + rating, 0)
        / ratings.length;
    
    document.getElementById("averagerating").textContent = averageRating.toFixed(1);

    // total streams
    const totalStreams = allSongs.reduce(
        (total, song) => total + getStreams(song.popularity), 0
    );

    document.getElementById("totalstreams").textContent = formatStreams(totalStreams);
}

// get streams
function getStreams(popularity) {

    if (!popularity) {
        return 0;
    }

    const text = popularity.toLowerCase();

    const match = text.match(
        /([\d,.]+)\s*(million|billion|thousand)/
    );

    if (!match) {
        return 0;
    }

    const number = parseFloat(
        match[1].replace(/,/g, "")
    );

    const unit = match[2];

    if (unit === "billion") {
        return number * 1000000000;
    }

    if (unit === "million") {
        return number * 1000000;
    }

    if (unit === "thousand") {
        return number * 1000;
    }

    return number;
}

// format streams
function formatStreams(number) {

    if (number >= 1000000000) {
        return (number / 1000000000).toFixed(1) + "B";
    }

    if (number >= 1000000) {
        return (number / 1000000).toFixed(1) + "M";
    }

    if (number >= 1000) {
        return (number / 1000).toFixed(1) + "K";
    }

    return number.toString();
}

// top songs + images
function displayTopSongs() {

    const container =
        document.getElementById("top-songs");

    container.innerHTML = "";

    const topLimit = isLoggedIn ? 5 : 3;
    const sortedSongs = [...allSongs]
        .sort(
            (a, b) =>
                getStreams(b.popularity) -
                getStreams(a.popularity)
        )
        .slice(0, topLimit);


    sortedSongs.forEach((song, index) => {

        const ranking =
            document.createElement("div");

        ranking.className = "song-ranking";

        ranking.innerHTML = `

            <span class="song-rank">
                ${String(index + 1).padStart(2, "0")}
            </span>

            <img
                class="song-cover"
                src="${song.image_url}"
                alt="${song.title}"
            >

            <div class="song-ranking-info">

                <h3>
                    ${song.title}
                </h3>

                <p>
                    ${song.artist}
                </p>

            </div>

            <span class="song-streams">
                ${formatStreams(getStreams(song.popularity))}
            </span>

        `;

        container.appendChild(ranking);

    });

}

// songs by year
function displaySongsByYear() {

    const container =
        document.getElementById("songs-by-year");

    container.innerHTML = "";

    const yearCounts = {};

    allSongs.forEach(song => {

        const year = song.year;

        if (!yearCounts[year]) {
            yearCounts[year] = 0;
        }

        yearCounts[year]++;

    });

    const years = Object.keys(yearCounts)
        .sort((a, b) => a - b);

    const maxSongs =
        Math.max(...Object.values(yearCounts));

    const chart =
        document.createElement("div");

    chart.className = "year-chart";

    years.forEach(year => {

        const count =
            yearCounts[year];
        const percentage =
            (count / maxSongs) * 100;
        const item =
            document.createElement("div");

        item.className = "year-item";
        item.innerHTML = `

            <span class="year-label">
                ${year}
            </span>

            <div class="year-bar">

                <div
                    class="year-fill"
                    style="width: ${percentage}%;">
                </div>

            </div>

            <span class="year-count">
                ${count} ${count === 1 ? "song" : "songs"}
            </span>

        `;

        chart.appendChild(item);

    });

    container.appendChild(chart);

}

const genreCategories = {
    "R&B / Soul": "R&B",
    "R&B / Indie Rock": "R&B",
    "R&B": "R&B",

    "Indie Pop / R&B": "R&B / Indie",
    "Contemporary R&B / Pop": "R&B / Pop",

    "Pop / Soul": "Pop",
    "Pop / Trip-Hop": "Pop",
    "Pop / Electropop": "Pop",
    "Downtempo / Pop": "Pop",

    "Soft Rock / Pop Rock": "Rock",
    "Soft Pop Rock / Blue-eyed Soul": "Rock / Soul",

    "Indie Rock / Alternative Rock": "Indie / Alternative",
    "Alternative / Indie": "Indie / Alternative",

    "OPM / Indie / Kundiman": "OPM",
    "OPM / Pop Rock": "OPM",

    "Dance / Electronic / Pop": "Electronic / Dance",

    "Hip-hop / Rap": "Hip-hop"
};

// genre distribution
function displayGenreDistribution() {

    const container =
        document.getElementById("genre-distribution");
    container.innerHTML = "";

    const genreCounts = {};

    allSongs.forEach(song => {

        const category = genreCategories[song.genre] || song.genre;

        if (!genreCounts[category]) {
            genreCounts[category] = 0;
        }

        genreCounts[category]++;

    });

    const sortedGenres =
        Object.entries(genreCounts)
            .sort((a, b) => b[1] - a[1]);

    const maxSongs =
        Math.max(...Object.values(genreCounts));

    sortedGenres.forEach(
        ([genre, count]) => {

            const percentage =
                (count / maxSongs) * 100;

            const item =
                document.createElement("div");

            item.className = "genre-item";

            item.innerHTML = `

                <span class="genre-label">
                    ${genre}
                </span>

                <div class="genre-bar">

                    <div
                        class="genre-fill"
                        style="width: ${percentage}%;">
                    </div>

                </div>

                <span class="genre-count">
                    ${count} ${count === 1 ? "song" : "songs"}
                </span>
            `;

            container.appendChild(item);

        }
    );
}


// genre dropdown
function loadGenreOptions() {

    const select =
        document.getElementById("select-genre");

    const genres = [
        ...new Set(
            allSongs.map(song => song.genre)
        )
    ];

    genres.sort();

    genres.forEach(genre => {

        const option =
            document.createElement("option");

        option.value = genre;

        option.textContent = genre;

        select.appendChild(option);

    });


    select.addEventListener(
        "change",
        displayGenreAnalysis
    );

}


// genre analysis

function displayGenreAnalysis() {
    const genre =
        document.getElementById("select-genre").value;


    if (!genre) {
        document.getElementById("genre-name").textContent = "";
        document.getElementById("genre-song-count").textContent = "0";
        document.getElementById("genre-artist-count").textContent = "0";
        document.getElementById("genre-percentage").textContent = "0%";
        document.getElementById("genre-song-list").innerHTML = "";
        document.getElementById("selected-song-details").innerHTML = `
            <p class="empty-song-message">
                Select a song to view its details
            </p>
            `;

        return;
    }

    const genreSongs =
        allSongs.filter(
            song => song.genre === genre
        );
    
    if (genreSongs.length == 0) {
        return;
    }

    // genre summary
    const totalSongs =
        genreSongs.length;


    const artists = [
        ...new Set(
            genreSongs.map(song => song.artist)
        )
    ];

    const totalArtists = artists.length;


    const percentage = (
        (totalSongs / allSongs.length) * 100
    ).toFixed(0);

    document.getElementById("genre-name").textContent = genre;

    document.getElementById("genre-song-count").textContent = totalSongs;

    document.getElementById("genre-artist-count").textContent = totalArtists;

    document.getElementById("genre-percentage").textContent = percentage + "%";

    // song list

    const songList = document.getElementById("genre-song-list");

    songList.innerHTML = genreSongs.map((song, index) => {

        return `
            <div class="genre-song-row"
                 data-song-index="${index}">

                <div class="genre-song-number">
                    ${String(index + 1).padStart(2, "0")}
                </div>

                <img
                    class="genre-song-image"
                    src="${song.image_url}"
                    alt="${song.title}"
                >

                <div class="genre-song-info">
                    <h4>${song.title}</h4>
                    <p>${song.artist}</p>
                </div>

                <div class="genre-song-year">
                    ${song.year}
                </div>

                <div class="genre-song-duration">
                    ${song.duration}
                </div>

                <div class="genre-song-rating">
                    ★ ${song.rating}/5
                </div>

            </div>
        `;

    }).join("");


    /* selected song */
    displaySelectedGenreSong(genreSongs[0]);

    /* click song */
    document.querySelectorAll(".genre-song-row")
        .forEach((row, index) => {

            row.addEventListener("click", () => {

                displaySelectedGenreSong(
                    genreSongs[index]
                );

            });

        });

}

function displaySelectedGenreSong(song) {

    const details =
        document.getElementById("selected-song-details");


    details.innerHTML = `

        <div class="selected-song">

            <img
                class="selected-song-image"
                src="${song.image_url}"
                alt="${song.title}"
            >

            <div>

                <h3 class="selected-song-title">
                    ${song.title}
                </h3>

                <p class="selected-song-artist">
                    ${song.artist}
                    ${song.featured_artist
                        ? `(feat. ${song.featured_artist})`
                        : ""}
                </p>


                <div class="song-detail-grid">

                    <div class="song-detail-label">
                        Album
                    </div>

                    <div class="song-detail-value">
                        ${song.album}
                    </div>


                    <div class="song-detail-label">
                        Year
                    </div>

                    <div class="song-detail-value">
                        ${song.year}
                    </div>


                    <div class="song-detail-label">
                        Genre
                    </div>

                    <div class="song-detail-value">
                        ${song.genre}
                    </div>


                    <div class="song-detail-label">
                        Language
                    </div>

                    <div class="song-detail-value">
                        ${song.language}
                    </div>


                    <div class="song-detail-label">
                        Duration
                    </div>

                    <div class="song-detail-value">
                        ${song.duration}
                    </div>

                </div>

            </div>

        </div>


        <div class="selected-song-extra">

            <div class="selected-song-extra-row">

                <div class="label">
                    Featured Artist
                </div>

                <div class="value">
                    ${song.featured_artist || "—"}
                </div>

            </div>


            <div class="selected-song-extra-row">

                <div class="label">
                    Writers
                </div>

                <div class="value">
                    ${song.writers || "—"}
                </div>

            </div>


            <div class="selected-song-extra-row">

                <div class="label">
                    Producers
                </div>

                <div class="value">
                    ${song.producers || "—"}
                </div>

            </div>


            <div class="selected-song-extra-row">

                <div class="label">
                    Rating
                </div>

                <div class="value">
                    ${song.rating}/5
                </div>

            </div>


            <div class="selected-song-extra-row">

                <div class="label">
                    Popularity
                </div>

                <div class="value">
                    ${song.popularity}
                </div>

            </div>


            <div class="selected-song-extra-row">

                <div class="label">
                    Description
                </div>

                <div class="value">
                    ${song.description || "—"}
                </div>

            </div>


            ${
                song.audio_url
                ? `
                    <a
                        href="${song.audio_url}"
                        target="_blank"
                        class="listen-button"
                    >
                        Listen
                    </a>
                `
                : ""
            }

        </div>

    `;
}

// load songs
loadSongs();

// PROFILE MENU
const profileButton = document.getElementById("profileButton");
const profileMenu = document.getElementById("profileMenu");
const profileUsername = document.getElementById("profileUsername");
const profileEmail = document.getElementById("profileEmail");
const logoutButton = document.getElementById("logoutButton");

if (isLoggedIn && profileButton) {
    const user = JSON.parse(savedUser);
    const initial = (user.username || "U").charAt(0).toUpperCase();

    if (profileUsername) profileUsername.textContent = user.username;
    if (profileEmail) profileEmail.textContent = user.email;

    const profileAvatar = document.getElementById("profileAvatar");
    const profileButtonIcon = document.getElementById("profileButtonIcon");
    const profileRoleBadge = document.getElementById("profileRoleBadge");

    if (profileAvatar) profileAvatar.textContent = initial;
    if (profileButtonIcon) profileButtonIcon.textContent = initial;
    if (profileRoleBadge) {
        profileRoleBadge.textContent = (user.role || "user").toUpperCase();
    }

    profileButton.addEventListener("click", function (event) {
        event.stopPropagation();
        const isOpen = profileMenu.classList.toggle("show");
        profileButton.setAttribute("aria-expanded", String(isOpen));
    });

    document.addEventListener("click", function (event) {
        if (!event.target.closest(".profile-container")) {
            profileMenu.classList.remove("show");
            profileButton.setAttribute("aria-expanded", "false");
        }
    });

    if (logoutButton) {
        logoutButton.addEventListener("click", function () {
            localStorage.removeItem("notenoughUser");
            localStorage.removeItem("notenoughToken");
            window.location.href = "../Website 1/login.html";
        });
    }
} else if (profileButton) {
    profileButton.addEventListener("click", function () {
        window.location.href = "../Website 1/login.html";
    });
}