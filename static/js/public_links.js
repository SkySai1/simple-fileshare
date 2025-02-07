function loadPublicLinks() {
    fetch('/file/public_links')
        .then(response => response.json())
        .then(data => {
            const list = document.getElementById('public-links-list');
            list.innerHTML = '';
            data.forEach(link => {
                const publicUrl = `${window.location.origin}/file/download/public/${link.hash_key}`;
                const createdAt = new Date(link.created_at).toLocaleString();
                const listItem = document.createElement('li');
                listItem.className = 'list-group-item d-flex justify-content-between align-items-center';
                listItem.innerHTML = `
                    <span>${link.file} <small class="text-muted">(${createdAt})</small></span>
                    <div class="d-flex gap-2">
                        <input type="text" class="form-control" value="${publicUrl}" readonly onclick="this.select()">
                        <button class="btn btn-danger btn-sm" onclick="deletePublicLink('${link.hash_key}')">🗑</button>
                    </div>
                `;
                list.appendChild(listItem);
            });
        })
        .catch(err => console.error('Ошибка загрузки ссылок: ', err));
}

function deletePublicLink(hashKey) {
    fetch(`/file/delete_public_link/${hashKey}`, { method: 'DELETE' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadPublicLinks();
            } else {
                alert("Ошибка удаления: " + (data.error || "Неизвестная ошибка"));
            }
        })
        .catch(err => console.error('Ошибка удаления ссылки: ', err));
}

document.addEventListener("DOMContentLoaded", loadPublicLinks);