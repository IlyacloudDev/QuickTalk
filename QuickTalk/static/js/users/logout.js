document.getElementById('logoutButton').addEventListener('click', function(event) {
    event.preventDefault();

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(window.LOGOUT_API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        credentials: 'same-origin'  // Учитывая, что используется сессионная аутентификация
    })
    .then(response => {
        if (response.ok) {
            // Перенаправляем на страницу после успешного выхода
            window.location.href = window.START_URL;
        } else {
            console.error('Logout failed:', response);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
