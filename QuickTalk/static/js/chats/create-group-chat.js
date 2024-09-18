document.getElementById('createGroupChatForm').addEventListener('submit', function(event){
    event.preventDefault();

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const groupChatNameInput = document.getElementById('group_name')

    document.getElementById('name_error').style.display = 'none';
    groupChatNameInput.classList.remove('is-invalid');

    const data = {
        name: groupChatNameInput.value,
    };

    fetch(window.CREATE_API_GROUP_CHAT, {
        method: 'POST',
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
            nameError.classList.add('is-invalid');
        } else if (result.detail) {
            window.location.href = window.START_URL;
        }
    })
    .catch(error => {
        // Обрабатываем ошибку запроса
        console.error('Error:', error);
    });
})
