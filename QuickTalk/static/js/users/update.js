document.getElementById('editProfileForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(window.UPDATE_API_URL, {
        method: 'PUT',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
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
        if (result.avatar || result.username) {
            if (result.avatar) {
                const avatarError = document.getElementById('avatar_error');
                avatarError.textContent = result.avatar[0];
                avatarError.style.display = 'block';
                document.getElementById('avatar').classList.add('is-invalid');
            }
            if (result.username) {
                const usernameError = document.getElementById('username_error');
                usernameError.textContent = result.username[0];
                usernameError.style.display = 'block';
                document.getElementById('username').classList.add('is-invalid');
            }
        } else if (result.detail) {
            window.location.href = window.START_URL;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
