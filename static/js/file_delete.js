document.addEventListener("DOMContentLoaded", function () {
    document.body.addEventListener("click", function (event) {
        if (event.target.classList.contains("delete-file")) {
            const fileId = event.target.dataset.fileId;
            if (!confirm("Вы уверены, что хотите удалить этот файл?")) return;

            fetch(`/file/delete/${fileId}`, {
                method: "DELETE"
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById(`file-${fileId}`).remove();
                } else {
                    alert(data.error || "Ошибка при удалении файла");
                }
            })
            .catch(error => console.error("Ошибка запроса:", error));
        }
    });
});