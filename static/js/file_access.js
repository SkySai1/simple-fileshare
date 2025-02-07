document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".toggle-public").forEach(button => {
        button.addEventListener("click", function () {
            const fileId = this.dataset.fileId;
            const icon = this.querySelector("i");
            
            fetch(`/file/toggle_public/${fileId}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    icon.classList.toggle("bi-unlock", data.is_public);
                    icon.classList.toggle("bi-lock", !data.is_public);
                } else {
                    alert(data.error || "Ошибка при обновлении доступа");
                }
            })
            .catch(error => console.error("Ошибка запроса:", error));
        });
    });
});