document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".toggle-admin").forEach(switchInput => {
        switchInput.addEventListener("change", function () {
            const userId = this.dataset.userId;
            const isAdmin = this.checked;
            const formData = new FormData();
            formData.append("user_id", userId);
            formData.append("is_admin", isAdmin ? "on" : "off");

            fetch("/admin/set_admin_status", {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const roleCell = document.getElementById(`role-${userId}`);
                    roleCell.textContent = isAdmin ? "Администратор" : "Пользователь";
                } else {
                    alert("Ошибка: " + data.error);
                    this.checked = !isAdmin; // Откат переключателя
                }
            })
            .catch(error => {
                console.error("Ошибка запроса:", error);
                this.checked = !isAdmin; // Откат переключателя в случае ошибки
            });
        });
    });
});