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
                    <input type="text" class="form-control" value="${publicUrl}" readonly onclick="this.select()">
                `;
                list.appendChild(listItem);
            });
        })
        .catch(err => console.error('Ошибка загрузки ссылок: ', err));
}

document.addEventListener("DOMContentLoaded", loadPublicLinks);