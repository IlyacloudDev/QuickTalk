document.addEventListener('DOMContentLoaded', function() {
    const chatIdForOutputDetail = sessionStorage.getItem('selectedChatId');
    const apiDetailUrl = `/api/chats/detail-chat/${chatIdForOutputDetail}/`;
    const apiUpdateUrl = `/api/chats/update-group-chat/${chatIdForOutputDetail}/`

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const groupChatNameInput = document.getElementById('group_name');

    // Загружаем данные чата для заполнения формы
    fetch(apiDetailUrl)
    .then(response => response.json())
    .then(data => {
        groupChatNameInput.value = data.detail.chat_name; // Заполняем поле имени чата
    })
    .catch(error => {
        console.error('Error fetching chat details:', error);
    });

    // Обрабатываем форму редактирования чата
    document.getElementById('editGroupChatForm').addEventListener('submit', function(event) {
        event.preventDefault();

        document.getElementById('name_error').style.display = 'none';
        groupChatNameInput.classList.remove('is-invalid');

        const data = {
            name: groupChatNameInput.value,
        };

        fetch(apiUpdateUrl, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.status === 400) {
                return response.json();
            } else if (response.ok) {
                return response.json();
            } else {
                throw new Error('Something went wrong');
            }
        })
        .then(result => {
            if (result.name) {
                const nameError = document.getElementById('name_error');
                nameError.textContent = result.name[0];
                nameError.style.display = 'block';
                groupChatNameInput.classList.add('is-invalid');
            } else if (result.detail) {
                window.location.href = window.CHATS_LIST_URL;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
