function copyToClipboard(link) {
    navigator.clipboard.writeText(link).then(() => {
        alert('Ссылка скопирована!');
    }).catch(err => {
        console.error('Ошибка копирования: ', err);
    });
}

function loadPublicLinks() {
    fetch('/file/public_links')
        .then(response => response.json())
        .then(data => {
            const list = document.getElementById('public-links-list');
            list.innerHTML = '';
            data.forEach(link => {
                const publicUrl = `${window.location.origin}/download/public/${link.hash_key}`;
                const listItem = document.createElement('li');
                listItem.className = 'list-group-item d-flex justify-content-between align-items-center';
                listItem.innerHTML = `
                    <span>${link.file}</span>
                    <button class="btn btn-outline-primary btn-sm" onclick="copyToClipboard('${publicUrl}')">
                        📋 Скопировать ссылку
                    </button>
                `;
                list.appendChild(listItem);
            });
        })
        .catch(err => console.error('Ошибка загрузки ссылок: ', err));
}

document.addEventListener("DOMContentLoaded", loadPublicLinks);