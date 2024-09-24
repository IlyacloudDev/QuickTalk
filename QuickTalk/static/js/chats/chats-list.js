document.addEventListener('DOMContentLoaded', function() {
    // Получаем контейнер для списка чатов
    const chatListContainer = document.getElementById('chatList');

    // Выполняем GET запрос к API
    fetch(window.CHAT_LIST_API_URL)
    .then(response => response.json())
    .then(data => {
        // Очищаем контейнер перед добавлением чатов
        chatListContainer.innerHTML = '';

        if (data.length === 0) {
            // Если чатов нет, показываем сообщение
            chatListContainer.innerHTML = '<p class="text-center text-white">No chats available.</p>';
        } else {
            data.forEach(chat => {
                // Создаем элемент для каждого чата
                const chatItem = document.createElement('a');
                chatItem.href = window.DETAIL_CHAT; // Ссылка на конкретный чат
                chatItem.className = 'btn btn-primary btn-lg mb-3 d-flex flex-column justify-content-center'; // Используем flex-column для вертикального выравнивания
                chatItem.id = `chat-${chat.id}`;
                // Задание фиксированных размеров
                chatItem.style.width = '100%'; // Ширина 100% контейнера
                chatItem.style.height = '70px'; // Фиксированная высота
                chatItem.style.overflow = 'hidden'; // Скрытие переполнения текста

                if (chat.type === 'group'){
                    // Добавляем flexbox для масштабируемого отступа
                    chatItem.innerHTML = `
                        <div class="d-flex flex-column">
                            <span class="text-truncate" style="max-width: 100%; overflow: hidden; text-overflow: ellipsis;">${chat.chat_name}</span>
                            <small class="text-white-50" style="margin-top: auto;">
                                <i class="fa-solid fa-people-group"></i>
                                <span style="margin-left: 5px;">${chat.type} chat</span> <!-- Отступ между иконкой и текстом -->
                            </small>
                        </div>
                    `;
                } else if (chat.type === 'personal'){
                    chatItem.innerHTML = `
                        <div class="d-flex flex-column">
                            <span class="text-truncate" style="max-width: 100%; overflow: hidden; text-overflow: ellipsis;">${chat.chat_name}</span>
                            <small class="text-white-50" style="margin-top: auto;">
                                <i class="fa-solid fa-user-group"></i>
                                <span style="margin-left: 5px;">${chat.type} chat</span> <!-- Отступ между иконкой и текстом -->
                            </small>
                        </div>
                    `;                    
                }

                // Добавляем элемент в контейнер
                chatListContainer.appendChild(chatItem);
                chatItem.addEventListener('click', function(event) {
                    event.preventDefault();
                    // Устанавливаем в sessionStorage id чата
                    sessionStorage.setItem('selectedChatId', chat.id);
                    // Переходим на страницу детализации чата
                    window.location.href = window.DETAIL_CHAT;
                });
            });
        }
    })
    .catch(error => {
        console.error('Error fetching chat list:', error);
        chatListContainer.innerHTML = '<p class="text-center text-danger">Failed to load chats. Please try again later.</p>';
    });
});
