document.addEventListener("DOMContentLoaded", function () {
    document.body.addEventListener("click", function (event) {
        const button = event.target.closest(".delete-file"); // Гарантируем, что клик именно по кнопке
        if (!button) return;

        const fileId = button.dataset.fileId;
        if (!confirm("Вы уверены, что хотите удалить этот файл?")) return;

        fetch(`/file/delete/${fileId}`, {
            method: "DELETE"
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Удаляем файл из всех блоков, где он присутствует
                document.querySelectorAll(`[id='file-${fileId}']`).forEach(fileElement => fileElement.remove());
            } else {
                alert(data.error || "Ошибка при удалении файла");
            }
        })
        .catch(error => console.error("Ошибка запроса:", error));
    });
});