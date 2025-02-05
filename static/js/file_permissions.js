document.addEventListener("DOMContentLoaded", function () {
    const userSelect = document.getElementById("user_id");
    const checkboxes = document.querySelectorAll('input[name="file_access"]');

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

    if (userSelect.value) {
        updatePermissions(userSelect.value);
    }
});