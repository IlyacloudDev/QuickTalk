document.addEventListener('DOMContentLoaded', function() {
    const chatIdForDeleteChat = sessionStorage.getItem('selectedChatId');
    const apiUrl = `/api/chats/delete-chat/${chatIdForDeleteChat}/`;
    const deleteChatForm = document.getElementById('deleteChatForm');

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    deleteChatForm.addEventListener('submit', function(event) {
        event.preventDefault();

        // Отправляем DELETE запрос
        fetch(apiUrl, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            // Проверяем, если это успешный ответ с кодом 204
            if (response.status === 204) {
                window.location.href = window.CHATS_LIST_URL; // Нет содержимого, поэтому возвращаем null
            } else if (response.status === 400) {
                return response.json(); // Обработка ошибок валидации
            } else {
                throw new Error('Something went wrong');
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while deleting the chat.");
        });
    });
});
