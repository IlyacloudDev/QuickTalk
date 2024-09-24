document.addEventListener('DOMContentLoaded', function() {
    const chatIdForOutputDetail = sessionStorage.getItem('selectedChatId');
    const apiUrl = `/api/chats/detail-chat/${chatIdForOutputDetail}`;

    // Элемент для отображения списка сообщений и имени чата
    const messageList = document.getElementById('messageList');
    const userInfo = document.getElementById('userInfo');

    // Запрос к API для получения деталей чата
    fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        // Отображаем имя чата сверху
        const chatName = document.createElement('h2');
        chatName.textContent = data.detail.chat_name;
        userInfo.prepend(chatName);  // Добавляем в начало блока userInfo

        // Проверяем наличие сообщений
        const messages = data.messages_of_chat;

        if (messages.length === 0) {
            // Если сообщений нет, показываем текст "No messages"
            const noMessages = document.createElement('p');
            noMessages.textContent = 'No messages';
            noMessages.classList.add('text-center', 'text-muted');
            messageList.appendChild(noMessages);
        // } else {
        //     // Если есть сообщения, выводим их
        //     messages.forEach(function(message) {
        //         const messageItem = document.createElement('div');
        //         messageItem.textContent = message.content;  // Предполагается, что в сообщении есть поле 'content'
        //         messageItem.classList.add('message-item', 'mb-2', 'p-2', 'rounded');
                
        //         // Стили для сообщений (пример)
        //         if (message.sender_id === data.current_user_id) {
        //             // Сообщения от текущего пользователя справа
        //             messageItem.classList.add('bg-primary', 'text-white', 'align-self-end');
        //         } else {
        //             // Сообщения от других пользователей слева
        //             messageItem.classList.add('bg-secondary', 'text-white');
        //         }
                
        //         messageList.appendChild(messageItem);
        //     });
        }
    })
    .catch(error => {
        console.error('Error fetching chat details:', error);
    });
});
