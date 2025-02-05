document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("password-form");
    const messageBox = document.getElementById("password-message");

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        
        const formData = new FormData(form);
        fetch("/admin/change_password", {
            method: "POST",
            body: formData
        })
        .then(response => response.ok ? response.text() : Promise.reject("Ошибка смены пароля"))
        .then(message => {
            messageBox.textContent = "Пароль успешно изменен!";
            messageBox.className = "alert alert-success";
            messageBox.style.display = "block";
        })
        .catch(error => {
            messageBox.textContent = error;
            messageBox.className = "alert alert-danger";
            messageBox.style.display = "block";
        });
    });
});