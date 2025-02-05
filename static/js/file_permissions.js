document.addEventListener("DOMContentLoaded", function () {
    const userSelect = document.getElementById("user_id");
    const checkboxes = document.querySelectorAll('input[name="file_access"]');
    const form = document.getElementById("permissions-form");
    const messageBox = document.getElementById("permissions-message");

    function updatePermissions(userId) {
        fetch(`/admin/get_permissions/${userId}`)
            .then(response => response.json())
            .then(files => {
                checkboxes.forEach(checkbox => {
                    checkbox.checked = files.includes(checkbox.value);
                });
            })
            .catch(error => console.error("Ошибка загрузки прав доступа:", error));
    }

    userSelect.addEventListener("change", function () {
        updatePermissions(this.value);
    });

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        
        const formData = new FormData(form);
        fetch("/admin/update_permissions", {
            method: "POST",
            body: formData
        })
        .then(response => response.ok ? response.text() : Promise.reject("Ошибка обновления"))
        .then(message => {
            messageBox.textContent = "Права успешно обновлены!";
            messageBox.className = "alert alert-success";
            messageBox.style.display = "block";
        })
        .catch(error => {
            messageBox.textContent = error;
            messageBox.className = "alert alert-danger";
            messageBox.style.display = "block";
        });
    });

    if (userSelect.value) {
        updatePermissions(userSelect.value);
    }
});