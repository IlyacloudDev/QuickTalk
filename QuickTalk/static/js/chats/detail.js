document.addEventListener('DOMContentLoaded', function() {
    const chatIdForOutputDetail = sessionStorage.getItem('selectedChatId');
    const apiUrl = `/api/chats/detail-chat/${chatIdForOutputDetail}`;
    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
    const chatSocket = new WebSocket(
        `${wsScheme}://${window.location.host}/ws/chat/${chatIdForOutputDetail}/`
    );

    const messageList = document.getElementById('messageList');
    const userInfo = document.getElementById('userInfo');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendMessageBtn');
    const requestUser = document.getElementById('requestUser').value


    // Запрос для получения прошлых сообщений чата
    fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
        // Отображаем имя чата
        const chatName = document.createElement('h2');
        chatName.textContent = data.detail.chat_name;
        userInfo.prepend(chatName);

        const messages = data.detail.messages_of_chat;

        const noMessagesElement = messageList.querySelector('p.text-center');
        if (noMessagesElement) {
            messageList.removeChild(noMessagesElement);
        }

        if (messages.length === 0) {
            const noMessages = document.createElement('p');
            noMessages.textContent = 'No messages';
            noMessages.classList.add('text-center');
            messageList.appendChild(noMessages);
        } else {
            // Добавляем каждое сообщение в список
            messages.forEach(function(message) {
                const messageElement = document.createElement('div');
                messageElement.classList.add('message-container');
                messageElement.classList.add(message.sender === parseInt(requestUser) ? 'message-sender' : 'message-receiver'); // Выравнивание
            
                // Преобразование timestamp в объект Date
                const timestamp = new Date(message.timestamp);
                
                // Получение часов и минут
                const hours = String(timestamp.getHours()).padStart(2, '0'); // Форматирование: 01, 02, ..., 10, 11, 12
                const minutes = String(timestamp.getMinutes()).padStart(2, '0');
            
                // Форматирование времени
                const formattedTime = `${hours}:${minutes}`;

                const  senderUsername = message.sender === parseInt(requestUser) ? 'you' : message.sender_username
                
                messageElement.innerHTML = `
                    <strong>${senderUsername}:</strong> ${message.content} <br>
                    <small>${formattedTime}</small>
                `;
                messageList.appendChild(messageElement);
            });
        }
    })
    .catch(error => {
        console.error('Error fetching chat details:', error);
    });

    // Обрабатываем входящие сообщения через WebSocket
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const messageElement = document.createElement('div');
        messageElement.classList.add('message-container');
        messageElement.classList.add(data.user_id === parseInt(requestUser) ? 'message-sender' : 'message-receiver'); // Выравнивание

        const timestamp = new Date(data.timestamp);

        const hours = String(timestamp.getHours()).padStart(2, '0'); // Форматирование: 01, 02, ..., 10, 11, 12
        const minutes = String(timestamp.getMinutes()).padStart(2, '0');

        const formattedTime = `${hours}:${minutes}`;

        const senderUsername = data.user_id === parseInt(requestUser) ? 'you' : data.username

        messageElement.innerHTML = `
            <strong>${senderUsername}:</strong> ${data.message} <br>
            <small>${formattedTime}</small>
        `;
        messageList.appendChild(messageElement);
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    // Обработка отправки сообщений
    const form = document.getElementById('sendMessageForm');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const message = messageInput.value;

        if (message.trim() !== '') {
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInput.value = ''; // Очищаем поле ввода после отправки
        }
    });

    // Функция для активации/деактивации кнопки отправки сообщения
    function toggleSendButton() {
        if (messageInput.value.trim() === '') {
            sendButton.disabled = true; // Отключаем кнопку, если поле пустое
        } else {
            sendButton.disabled = false; // Включаем кнопку, если есть текст
        }
    }

    // Проверяем состояние кнопки при вводе текста
    messageInput.addEventListener('input', toggleSendButton);
    toggleSendButton(); // Проверка при загрузке страницы
});
