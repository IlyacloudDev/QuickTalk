document.getElementById('searchUserByPhoneForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const userPhoneNumberInput = document.getElementById('user_phone');
    const userItemContainer = document.getElementById('userItem');
    
    userItemContainer.innerHTML = ''
    document.getElementById('phone_error').style.display = 'none';
    userPhoneNumberInput.classList.remove('is-invalid');


    
    const data = {
        phone_number: userPhoneNumberInput.value,
    };

    fetch(window.SEARCH_API_USER, {
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
        } else if (response.status === 404) {
            return response.json(); // Обработка ошибки, когда пользователь не найден (404)
        }
         else {
            throw new Error('Something went wrong');
        }
    })
    .then(result => {
        console.log(result)
        if (result.phone_number) {
            const phoneError = document.getElementById('phone_error');
            phoneError.textContent = result.phone_number[0];
            phoneError.style.display = 'block';
            phoneError.classList.add('is-invalid');
        } else if (result.error === "Object does not exist.") {
            userItemContainer.innerHTML = '<p class="text-center text-white">There is no user with such a phone number</p>';
        } else if (result.detail) {
            const userItem = document.createElement('a');
            userItem.href = '#';
            userItem.className = 'btn btn-primary btn-lg mb-3 d-flex flex-column justify-content-center';
            userItem.style.width = '100%';
            userItem.style.height = '70px';
            userItem.style.overflow = 'hidden';

            // // Проверка наличия аватара и установка дефолтного изображения
            const avatarSrc = result.detail.avatar

            userItem.innerHTML = `
                <div class="d-flex align-items-center">
                    <img src="${avatarSrc}" alt="${result.detail.username} avatar" class="rounded-circle" style="width: 50px; height: 50px; object-fit: cover; margin-right: 10px;">
                    <div class="d-flex flex-column">
                        <span class="text-truncate" style="max-width: 100%; overflow: hidden; text-overflow: ellipsis;">${result.detail.username}</span>
                        <small class="text-white-50" style="margin-top: auto;">
                            ${result.detail.phone_number}
                        </small>
                    </div>
                </div>
            `;
            userItemContainer.appendChild(userItem);
        }
    })
    .catch(error => {
        console.error('Error fetching user item:', error);
        userItemContainer.innerHTML = '<p class="text-center text-danger">Failed to load user item. Please try again later.</p>';
    });
});
