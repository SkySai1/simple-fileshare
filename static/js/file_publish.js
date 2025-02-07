document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".generate-public-link").forEach(button => {
        button.addEventListener("click", function () {
            const fileId = this.getAttribute("data-file-id");
            fetch(`/file/generate_public_link/${fileId}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" }
            })
            .then(response => response.json())
            .then(data => {
                if (data.public_link) {
                    alert("Ссылка опубликована: " + data.public_link);
                } else {
                    alert("Ошибка публикации: " + (data.error || "Неизвестная ошибка"));
                }
            })
            .catch(error => console.error("Ошибка запроса:", error));
        });
    });
});