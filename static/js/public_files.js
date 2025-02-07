document.addEventListener("DOMContentLoaded", function () {
    function loadPublicFiles() {
        fetch("/file/public_files")
            .then(response => response.json())
            .then(files => {
                const list = document.getElementById("public-files-list");
                list.innerHTML = "";

                if (files.length === 0) {
                    list.innerHTML = "<p class='text-muted'>Публичных файлов нет.</p>";
                    return;
                }

                files.forEach(file => {
                    const li = document.createElement("li");
                    li.className = "list-group-item d-flex justify-content-between align-items-center";
                    li.innerHTML = `
                        <div>
                            <strong>${file.filename}</strong>
                            <br>
                            <small>Размер: ${(file.size / 1024).toFixed(2)} KB</small>
                            <br>
                            <small>Изменен: ${file.modified}</small>
                            <br>
                            <small>Владелец: ${file.owner_username}</small>
                        </div>
                        <a href="/download/${file.file_id}" class="btn btn-primary btn-sm">Скачать</a>
                    `;
                    list.appendChild(li);
                });
            })
            .catch(error => console.error("Ошибка загрузки публичных файлов:", error));
    }

    loadPublicFiles(); // Загружаем список при загрузке страницы

    document.addEventListener("publicFilesUpdated", loadPublicFiles); // Обновляем при изменениях
});