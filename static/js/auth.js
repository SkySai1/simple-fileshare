document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");
    const errorAlert = document.getElementById("error-alert");

    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const formData = {
            username: document.getElementById("username").value,
            password: document.getElementById("password").value
        };

        try {
            const response = await fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                window.location.href = data.redirect_url;
            } else {
                errorAlert.textContent = data.error;
                errorAlert.style.display = "block";
            }
        } catch (error) {
            errorAlert.textContent = "Ошибка соединения с сервером.";
            errorAlert.style.display = "block";
        }
    });
});