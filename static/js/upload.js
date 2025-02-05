document.addEventListener("DOMContentLoaded", function () {
    const uploadForm = document.getElementById("upload-form");
    const fileInput = document.getElementById("file-input");
    const messageBox = document.getElementById("upload-message");

    uploadForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        fetch("/upload", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                messageBox.textContent = "Файл успешно загружен!";
                messageBox.className = "alert alert-success";
                location.reload();
            } else {
                messageBox.textContent = "Ошибка: " + data.error;
                messageBox.className = "alert alert-danger";
            }
            messageBox.style.display = "block";
        })
        .catch(error => {
            messageBox.textContent = "Ошибка загрузки файла";
            messageBox.className = "alert alert-danger";
            messageBox.style.display = "block";
        });
    });
});