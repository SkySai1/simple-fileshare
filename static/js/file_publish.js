document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".generate-public-link").forEach(button => {
        button.addEventListener("click", function () {
            const fileId = this.getAttribute("data-file-id");
            const messageBox = document.getElementById("publish-message");
            
            if (!messageBox) return; // Проверяем, существует ли элемент
            
            fetch(`/file/generate_public_link/${fileId}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" }
            })
            .then(response => response.json())
            .then(data => {
                if (data.public_link) {
                    messageBox.textContent = "Ссылка успешно опубликована!";
                    messageBox.classList.remove("text-danger");
                    messageBox.classList.add("text-success");
                    loadPublicLinks(); // Обновляем список ссылок
                } else {
                    messageBox.textContent = "Ошибка публикации: " + (data.error || "Неизвестная ошибка");
                    messageBox.classList.remove("text-success");
                    messageBox.classList.add("text-danger");
                }
            })
            .catch(error => {
                messageBox.textContent = "Ошибка запроса: " + error;
                messageBox.classList.remove("text-success");
                messageBox.classList.add("text-danger");
            });
        });
    });
});