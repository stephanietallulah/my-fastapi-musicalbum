const API_URL = "https://my-fastapi-musicalbum.vercel.app";

function redirectIfLoggedIn() {
    const token = localStorage.getItem("notenoughToken");
    const user = localStorage.getItem("notenoughUser");

    if (token && user) {
        window.location.replace("index.html");
    }
}

redirectIfLoggedIn();
window.addEventListener("pageshow", redirectIfLoggedIn);

const authSlider = document.getElementById("authSlider");
const showSignupBtn = document.getElementById("showSignup");
const showLoginBtn = document.getElementById("showLogin");

if (showSignupBtn) {
    showSignupBtn.addEventListener("click", (event) => {
        event.preventDefault();
        authSlider.classList.add("show-signup");
    });
}

if (showLoginBtn) {
    showLoginBtn.addEventListener("click", (event) => {
        event.preventDefault();
        authSlider.classList.remove("show-signup");
    });
}


// shows or hides password

document.querySelectorAll(".password-toggle").forEach((button) => {

    button.addEventListener("click", () => {

        const input = button.previousElementSibling;

        if (input.type === "password") {
            input.type = "text";
        } else {
            input.type = "password";
        }

    });

});


// register slider

const signupForm = document.getElementById("signupForm");
const signupMessage = document.getElementById("signupMessage");

if (signupForm) {

    signupForm.addEventListener("submit", async (event) => {

        event.preventDefault();

        const username = document
            .getElementById("signupName")
            .value
            .trim();

        const email = document
            .getElementById("signupEmail")
            .value
            .trim();

        const password = document
            .getElementById("signupPassword")
            .value;

        if (!username || !email || !password) {

            signupMessage.textContent =
                "Please fill in all fields.";

            return;
        }

        if (password.length < 6) {

            signupMessage.textContent =
                "Password must be at least 6 characters.";

            return;
        }

        signupMessage.textContent =
            "Creating your account...";

        try {

            const response = await fetch(
                `${API_URL}/api/v1/register`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        username: username,
                        email: email,
                        password: password
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {

                signupMessage.textContent =
                    data.detail || "Registration failed.";

                return;
            }

            signupMessage.textContent =
                "Account created successfully!";

            // Clear password
            document.getElementById("signupPassword").value = "";

            // Move back to login after registration
            setTimeout(() => {

                authSlider.classList.remove("show-signup");

            }, 1200);

        } catch (error) {

            console.error("REGISTER ERROR:", error);

            signupMessage.textContent =
                "Unable to connect to the server.";

        }

    });

}


// log in form 

const loginForm = document.getElementById("loginForm");
const loginMessage = document.getElementById("loginMessage");

if (loginForm) {

    loginForm.addEventListener("submit", async (event) => {

        event.preventDefault();

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        if (!email || !password) {
            loginMessage.textContent =
                "Please enter your email and password.";
            return;
        }

        loginMessage.textContent = "Logging in...";

        try {

            const response = await fetch(
                `${API_URL}/api/v1/login`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {
                loginMessage.textContent =
                    data.detail || "Invalid email or password.";
                return;
            }

            // Save logged-in user
            localStorage.setItem(
                "notenoughUser",
                JSON.stringify(data.user)
            );

            localStorage.setItem(
                "notenoughToken",
                data.token
            );

            loginMessage.textContent =
                "Login successful!";

            // Replace history entry so Chrome's Back button cannot return to login.html
            setTimeout(() => {
                window.location.replace("index.html");
            }, 500);

        } catch (error) {

            console.error("LOGIN ERROR:", error);

            loginMessage.textContent =
                "Unable to connect to the server.";
        }

    });

}