document.addEventListener('DOMContentLoaded', function () {
    const userId = sessionStorage.getItem('userId');

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if (!userId) {
        alert('No user selected!');
        return;
    }

    const apiUrl = `/api/users/detail-user/${userId}/`;

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch user data');
            }
            return response.json();
        })
        .then(data => {
            const userInfoContainer = document.getElementById('userInfo');

            // Проверяем наличие аватара и устанавливаем значение по умолчанию, если его нет
            const avatarSrc = data.detail.avatar;

            // Формируем HTML разметку
            const userInfoHtml = `
                <div class="text-center">
                    <img src="${avatarSrc}" alt="${data.detail.username} avatar" class="rounded-circle mb-3" style="width: 150px; height: 150px; object-fit: cover;">
                    <h3 class="text-white">${data.detail.username}</h3>
                    <p>${data.detail.phone_number}</p>
                </div>
            `;

            // Вставляем разметку в контейнер
            userInfoContainer.innerHTML = userInfoHtml;

            const currentUserId = document.getElementById('userId').value;

            const buttonChattingContainer = document.getElementById('userChatting');
            if (currentUserId === data.detail.id.toString()) {
                buttonChattingContainer.innerHTML = `
                    <button id="updateProfile" class="btn btn-light btn-lg">
                        <i class="fa-solid fa-gear"></i> Go to update profile
                    </button>
                `;
                // Добавляем обработчик для кнопки "Обновить профиль"
                document.getElementById('updateProfile').addEventListener('click', function (e) {
                    e.preventDefault();
                    window.location.href = window.UPDATE_USER;
                });
            } else {
                buttonChattingContainer.innerHTML = `
                    <button id="personalChatting" class="btn btn-light btn-lg">
                       <i class="fa-solid fa-paper-plane"></i> Message
                    </button>
                `;
                // Добавляем обработчик для кнопки "Сообщение"
                document.getElementById('personalChatting').addEventListener('click', function (e) {
                    e.preventDefault();

                    const data = {
                        chosen_user_to_prsnl_cht_id: userId
                    };

                    fetch(window.CREATE_PERSONAL_API_CHAT, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken
                        },
                        body: JSON.stringify(data)
                    })
                        .then(response => {
                            if (response.status === 400) {
                                alert("Chat already exists. Redirecting...");
                                // Логика для перенаправления на уже существующий чат
                                window.location.href = window.LIST_API_CHATS;
                            } else if (!response.ok) {
                                throw new Error('Failed to create chat');
                            }
                            return response.json();
                        })
                        .then(data => {
                            if (data.detail) {
                                // Перенаправление на новый чат
                                window.location.href = window.LIST_API_CHATS;
                            }
                        })
                        .catch(error => {
                            console.error('Error creating chat:', error);
                        });
                });
            }
        })
        .catch(error => {
            console.error('Error fetching user data:', error);
            const userInfoContainer = document.getElementById('userInfo');
            userInfoContainer.innerHTML = '<p class="text-center text-danger">Failed to load user details.</p>';
        });
});
