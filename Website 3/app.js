const API_URL = "https://my-fastapi-musicalbum.vercel.app";
const API_KEY = "api-key-one";

const FETCH_OPTIONS = {
    headers: {
        "x-api-key": API_KEY
    }
};

let allSongs = [];

let selectedMood = "";
let selectedSituation = "";
let selectedEnergy = "";

const savedUser = localStorage.getItem("notenoughUser");
const savedToken = localStorage.getItem("notenoughToken");
const isLoggedIn = Boolean(savedUser && savedToken);

function toList(value) {
    if (Array.isArray(value)) return value.map(v => String(v).trim().toLowerCase());
    if (typeof value === "string") return value.split(",").map(v => v.trim().toLowerCase());
    return [];
}

/* load songs */
async function loadSongs() {
    try {
        const response = await fetch(
            `${API_URL}/api/v1/songs`,
            FETCH_OPTIONS
        );

        const data = await response.json();
        allSongs = Array.isArray(data) ? data : (data.songs || []);
        console.log("Songs loaded:", allSongs);

        loadGenreOptions();
        loadEraOptions();

        if (selectedMood && !isLoggedIn) {
            findMusic();
        }
    } catch (error) {
        console.error("API Error:", error);
    }
}

/* music steps - makes one question visible at a time */
const musicSteps = document.querySelectorAll(".music-step");
const stepCounter = document.getElementById("step-counter");
const progressFill = document.getElementById("progress-fill");

function showStep(step) {
    if (!musicSteps.length) return;

    musicSteps.forEach((musicStep, index) => {
        musicStep.classList.toggle("active", index === step - 1);
    });

    if (stepCounter) stepCounter.textContent = `${step} / 4`;
    if (progressFill) progressFill.style.width = `${step * 25}%`;
}

/* start discovering (optional if button exists) */
const startBtn = document.getElementById("start-discovering");
if (startBtn) {
    startBtn.addEventListener("click", () => {
        clearRecommendations();
        document.getElementById("choose-music")?.scrollIntoView({
            behavior: "smooth"
        });
        showStep(1);
    });
}

/* configure guest mode vs logged-in full access */
function applyAuthMode() {
    const guestBanner = document.getElementById("guestSigninBanner");
    const loggedInElements = document.querySelectorAll(".logged-in-only");
    const lockedCards = document.querySelectorAll(".mood-choice.locked");

    if (isLoggedIn) {
        if (guestBanner) guestBanner.style.display = "none";

        loggedInElements.forEach(el => {
            el.style.display = el.classList.contains("mood-choice") || el.classList.contains("pop-buttons")
                ? "flex"
                : "block";
        });

        lockedCards.forEach(card => {
            card.classList.remove("locked");
            const lockIcon = card.querySelector(".lock-icon");
            const unlockedIcon = card.querySelector(".unlocked-icon");
            const unlockLabel = card.querySelector(".unlock-label");
            if (lockIcon) lockIcon.style.display = "none";
            if (unlockedIcon) unlockedIcon.style.display = "flex";
            if (unlockLabel) unlockLabel.style.display = "none";
        });
    }
}

applyAuthMode();

/* mood choices */
const moodChoices = document.querySelectorAll(".mood-choice");

moodChoices.forEach(choice => {
    choice.addEventListener("click", () => {
        if (!isLoggedIn && choice.classList.contains("locked")) {
            window.location.href = "../Website 1/login.html";
            return;
        }

        moodChoices.forEach(item => item.classList.remove("selected"));
        choice.classList.add("selected");

        selectedMood = choice.dataset.value;

        if (isLoggedIn) {
            const moodNextBtn = document.getElementById("mood-next");
            if (moodNextBtn) moodNextBtn.disabled = false;
        } else {
            // Guest mode: directly display Chill recommendations without steps 2-4
            findMusic();
            document.getElementById("recommendations")?.scrollIntoView({
                behavior: "smooth"
            });
        }
    });
});

/* mood next button */
document
    .getElementById("mood-next")
    ?.addEventListener("click", () => {
        showStep(2);
    });

/* situation choices */
const situationChoices = document.querySelectorAll(".situation-choice");

situationChoices.forEach(choice => {
    choice.addEventListener("click", () => {
        situationChoices.forEach(item => {
            item.classList.remove("selected");
        });

        choice.classList.add("selected");
        selectedSituation = choice.dataset.value;

        const situationNext = document.getElementById("situation-next");
        if (situationNext) situationNext.disabled = false;
    });
});

/* situation next button */
document
    .getElementById("situation-next")
    ?.addEventListener("click", () => {
        showStep(3);
    });

/* energy choices */
const energyChoices = document.querySelectorAll(".energy-card");

energyChoices.forEach(choice => {
    choice.addEventListener("click", () => {
        energyChoices.forEach(item => {
            item.classList.remove("selected");
        });

        choice.classList.add("selected");
        selectedEnergy = choice.dataset.value;

        const prefNext = document.getElementById("preference-next");
        if (prefNext) prefNext.disabled = false;
    });
});

/* preference next button */
document
    .getElementById("preference-next")
    ?.addEventListener("click", () => {
        document.getElementById("selected-mood").textContent = selectedMood;
        document.getElementById("selected-situation").textContent = selectedSituation;
        document.getElementById("selected-energy").textContent = selectedEnergy;

        showStep(4);
    });

/* clear recommendation */
function clearRecommendations() {
    document.getElementById("recommended-music").innerHTML = "";
    document.getElementById("best-match").innerHTML = "";

    selectedMood = "";
    selectedSituation = "";
    selectedEnergy = "";

    document.querySelectorAll(".mood-choice").forEach(choice => {
        choice.classList.remove("selected");
    });

    document.querySelectorAll(".situation-choice").forEach(choice => {
        choice.classList.remove("selected");
    });

    document.querySelectorAll(".energy-card").forEach(choice => {
        choice.classList.remove("selected");
    });

    const moodNext = document.getElementById("mood-next");
    if (moodNext) moodNext.disabled = true;

    const situationNext = document.getElementById("situation-next");
    if (situationNext) situationNext.disabled = true;

    const preferenceNext = document.getElementById("preference-next");
    if (preferenceNext) preferenceNext.disabled = true;

    document.getElementById("select-genre").value = "";
    document.getElementById("select-era").value = "";
    document.getElementById("select-rating").value = "";
    document.getElementById("select-popularity").value = "";

    document.getElementById("selected-mood").textContent = "—";
    document.getElementById("selected-situation").textContent = "—";
    document.getElementById("selected-energy").textContent = "—";

    showStep(1);
}

/* situation back button */
document
    .getElementById("situation-back")
    ?.addEventListener("click", () => {
        clearRecommendations();
        showStep(1);
    });

/* preference back button */
document
    .getElementById("preference-back")
    ?.addEventListener("click", () => {
        clearRecommendations();
        showStep(2);
    });

/* find back button */
document
    .getElementById("find-back")
    ?.addEventListener("click", () => {
        clearRecommendations();
        showStep(3);
    });

/* home button */
document
    .getElementById("home-link")
    ?.addEventListener("click", () => {
        clearRecommendations();
        document.getElementById("home")?.scrollIntoView({
            behavior: "smooth"
        });
    });

/* find music */
document
    .getElementById("find-music")
    ?.addEventListener("click", findMusic);

/* surprise */
document
    .getElementById("surprise")
    ?.addEventListener("click", surpriseMe);

/* get streams */
function getStreams(popularity) {
    if (!popularity) {
        return 0;
    }

    const text = popularity.toLowerCase();
    const match = text.match(/([\d,.]+)\s*(million|billion|thousand)/);

    if (!match) {
        return 0;
    }

    const number = parseFloat(match[1].replace(/,/g, ""));
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

function getPopularityLevel(popularity) {
    if (!popularity) {
        return "";
    }

    const streams = getStreams(popularity);

    if (streams >= 100000000) {
        return "very-popular";
    }

    if (streams >= 10000000) {
        return "popular";
    }

    return "other";
}

async function findMusic() {
    if (!allSongs || allSongs.length === 0) {
        await loadSongs();
    }
    if (!allSongs || allSongs.length === 0) return;

    const selectedGenre = document.getElementById("select-genre")?.value || "";
    const selectedEra = document.getElementById("select-era")?.value || "";
    const selectedRating = document.getElementById("select-rating")?.value || "";
    const selectedPopularity = document.getElementById("select-popularity")?.value || "";

    const chillAliases = ["chill", "calm", "mellow", "relaxed", "peaceful", "dreamy", "ambient"];

    let recommendedSongs = allSongs.map(song => {
        let score = 0;
        const songMoods = toList(song.mood);
        const songVibes = toList(song.vibe);

        /* mood - 30% */
        if (selectedMood) {
            const target = selectedMood.toLowerCase();
            if (target === "chill") {
                if (
                    songMoods.some(m => chillAliases.includes(m)) ||
                    songVibes.some(v => chillAliases.includes(v)) ||
                    (song.energy && song.energy.toLowerCase() === "low")
                ) {
                    score += 30;
                }
            } else if (songMoods.includes(target) || songVibes.includes(target)) {
                score += 30;
            }
        }

        /* situation - 25% */
        if (
            selectedSituation &&
            toList(song.best_for).includes(selectedSituation.toLowerCase())
        ) {
            score += 25;
        }

        /* energy - 20% */
        if (
            selectedEnergy &&
            song.energy &&
            song.energy.toLowerCase() === selectedEnergy.toLowerCase()
        ) {
            score += 20;
        }

        /* genre - 10% */
        if (
            selectedGenre &&
            song.genre &&
            song.genre.toLowerCase() === selectedGenre.toLowerCase()
        ) {
            score += 10;
        }

        /* rating - 10% */
        if (
            selectedRating &&
            parseFloat(song.rating) >= Number(selectedRating)
        ) {
            score += 10;
        }

        /* era - 5% */
        if (
            selectedEra &&
            song.year === Number(selectedEra)
        ) {
            score += 5;
        }

        return {
            song: song,
            score: score
        };
    });

    /* remove songs with no match */
    recommendedSongs = recommendedSongs.filter(item => item.score > 0);

    /* highest matches first */
    recommendedSongs.sort((a, b) => b.score - a.score);

    /* show 3 songs in guest mode, 10 songs when logged in */
    const maxResults = isLoggedIn ? 10 : 3;
    recommendedSongs = recommendedSongs.slice(0, maxResults);

    console.log("Recommended songs:", recommendedSongs);

    displayRecommendations(
        recommendedSongs,
        selectedGenre,
        selectedEra,
        selectedRating,
        selectedPopularity
    );

    document.getElementById("recommendations")?.scrollIntoView({
        behavior: "smooth"
    });
}

/* surprise music */
function surpriseMe() {
    if (allSongs.length === 0) {
        return;
    }

    const randomIndex = Math.floor(Math.random() * allSongs.length);
    const randomSong = allSongs[randomIndex];

    displaySurprise(randomSong);
}

/* display function of surprise music */
function displaySurprise(song) {
    const recSection = document.getElementById("recommendations");
    if (recSection) recSection.style.display = "block";

    const container = document.getElementById("recommended-music");
    container.innerHTML = "";
    const songElement = document.createElement("div");
    songElement.className = "recommendations";
    songElement.innerHTML = `
        <div class="song-rank">
            ★
        </div>

        <img
            class="song-image" src="${song.image_url}" alt="${song.title}">

        <div class="song-info">
            <h3>${song.title}</h3>

            <p>${song.artist}</p>

            <div class="song-meta">${song.genre} · ${song.year}</div>

            <div class="match-info">
                <span class="match-score">Surprise Pick</span>
            </div>
        </div>

        <div class="song-rating">${song.rating}</div>
    `;

    container.appendChild(songElement);
    recSection?.scrollIntoView({ behavior: "smooth" });
}

/* display recommendations */
function displayRecommendations(recommendations, selectedGenre, selectedEra, selectedRating, selectedPopularity) {
    const recSection = document.getElementById("recommendations");
    recSection.style.display = "block";

    const container = document.getElementById("recommended-music");
    container.innerHTML = "";

    if (recommendations.length === 0) {
        container.innerHTML = `
            <p>No matching songs found.</p>
        `;
        return;
    }

    /* best match */
    const bestMatchTitle = document.createElement("h2");
    bestMatchTitle.textContent = "Best Match";
    bestMatchTitle.className = "recommendation-heading";
    container.appendChild(bestMatchTitle);

    const chillAliases = ["chill", "calm", "mellow", "relaxed", "peaceful", "dreamy", "ambient"];
    const targetMood = selectedMood.toLowerCase();

    recommendations.forEach((item, index) => {
        const song = item.song;
        const score = item.score;

        const moodMatch = Boolean(selectedMood) && (
            targetMood === "chill"
                ? (
                    toList(song.mood).some(m => chillAliases.includes(m)) ||
                    toList(song.vibe).some(v => chillAliases.includes(v)) ||
                    (song.energy && song.energy.toLowerCase() === "low")
                )
                : (
                    toList(song.mood).includes(targetMood) ||
                    toList(song.vibe).includes(targetMood)
                )
        );

        const situationMatch =
            Boolean(selectedSituation) &&
            toList(song.best_for).includes(selectedSituation.toLowerCase());

        const energyMatch =
            Boolean(selectedEnergy) &&
            song.energy &&
            song.energy.toLowerCase() === selectedEnergy.toLowerCase();

        const genreMatch =
            selectedGenre &&
            song.genre &&
            song.genre.toLowerCase() === selectedGenre.toLowerCase();

        const eraMatch =
            selectedEra &&
            song.year === Number(selectedEra);

        const ratingMatch =
            selectedRating &&
            parseFloat(song.rating) >= Number(selectedRating);

        const popularityMatch =
            selectedPopularity &&
            getPopularityLevel(song.popularity) === selectedPopularity;

        const songElement = document.createElement("div");

        songElement.className =
            index === 0
                ? "recommendations best-match"
                : "recommendations";

        songElement.innerHTML = `
            ${index === 0 ? `
                <div class="best-match-label">
                    BEST MATCH
                </div>
            ` : ""}

            <div class="song-rank">
                ${index + 1}
            </div>

            <img
                class="song-image"
                src="${song.image_url}"
                alt="${song.title}"
            >

            <div class="song-info">
                <h3>${song.title}</h3>

                <p>
                    ${song.artist}
                </p>

                <div class="song-meta">
                    ${song.genre} · ${song.year}
                </div>

                <div class="match-info">
                    <span class="match-score">
                        ${score}% Match
                    </span>
                </div>

                <div class="match-details">
                    <span class="${moodMatch ? "matched" : "not-matched"}">
                        ${moodMatch ? "✓" : "✕"} Mood
                    </span>

                    ${selectedSituation ? `
                        <span class="${situationMatch ? "matched" : "not-matched"}">
                            ${situationMatch ? "✓" : "✕"} Situation
                        </span>
                    ` : ""}

                    ${selectedEnergy ? `
                        <span class="${energyMatch ? "matched" : "not-matched"}">
                            ${energyMatch ? "✓" : "✕"} Energy
                        </span>
                    ` : ""}

                    ${selectedGenre ? `
                        <span class="${genreMatch ? "matched" : "not-matched"}">
                            ${genreMatch ? "✓" : "✕"} Genre
                        </span>
                    ` : ""}

                    ${selectedEra ? `
                        <span class="${eraMatch ? "matched" : "not-matched"}">
                            ${eraMatch ? "✓" : "✕"} Era
                        </span>
                    ` : ""}

                    ${selectedRating ? `
                        <span class="${ratingMatch ? "matched" : "not-matched"}">
                            ${ratingMatch ? "✓" : "✕"} Rating
                        </span>
                    ` : ""}

                    ${selectedPopularity ? `
                        <span class="${popularityMatch ? "matched" : "not-matched"}">
                            ${popularityMatch ? "✓" : "✕"} Popularity
                        </span>
                    ` : ""}
                </div>
            </div>

            <div class="song-rating">
                ${song.rating}
            </div>
        `;

        container.appendChild(songElement);
    });
}

/* load genre options */
function loadGenreOptions() {
    const select = document.getElementById("select-genre");

    const genres = [
        ...new Set(
            allSongs.map(song => song.genre)
        )
    ];

    genres.sort();
    genres.forEach(genre => {
        const option = document.createElement("option");
        option.value = genre;
        option.textContent = genre;
        select.appendChild(option);
    });
}

/* load era options */
function loadEraOptions() {
    const select = document.getElementById("select-era");

    const years = [
        ...new Set(
            allSongs.map(song => song.year)
        )
    ];

    years.sort((a, b) => a - b);

    years.forEach(year => {
        const option = document.createElement("option");
        option.value = year;
        option.textContent = year;
        select.appendChild(option);
    });
}

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