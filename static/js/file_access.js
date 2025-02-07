document.addEventListener("DOMContentLoaded", function () {
    function updatePublicStatus(fileId, isPublic) {
        const toggleSwitch = document.querySelector(`.toggle-public[data-file-id='${fileId}']`);
        if (toggleSwitch) {
            toggleSwitch.checked = isPublic;
        }
    }

    document.querySelectorAll(".toggle-public").forEach(toggle => {
        toggle.addEventListener("change", function () {
            const fileId = this.dataset.fileId;
            fetch(`/file/toggle_public/${fileId}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updatePublicStatus(fileId, data.is_public);
                    document.dispatchEvent(new Event("publicFilesUpdated")); // Сообщаем другим скриптам
                } else {
                    alert(data.error || "Ошибка при обновлении доступа");
                }
            })
            .catch(error => console.error("Ошибка запроса:", error));
        });
    });

    fetch("/file/public_files")
        .then(response => response.json())
        .then(files => {
            files.forEach(file => updatePublicStatus(file.file_id, true));
        })
        .catch(error => console.error("Ошибка загрузки публичных файлов:", error));
});