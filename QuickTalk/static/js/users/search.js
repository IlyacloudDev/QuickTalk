document.addEventListener('DOMContentLoaded', function() {
    const userPhoneNumberInput = document.getElementById('userPhone');
    const userItemContainer = document.getElementById('userItems');

    userPhoneNumberInput.addEventListener('input', function() {
        const query = userPhoneNumberInput.value.trim();
        const apiURL = `/api/users/search-user/?query=${encodeURIComponent(query)}`
        
        if (query.length > 0) {
            fetch(apiURL)
            .then(response => response.json())
            .then(data => {
                userItemContainer.innerHTML = '';
                
                document.getElementById('phone_error').style.display = 'none';
                userPhoneNumberInput.classList.remove('is-invalid');

                if (data.error) {
                    if (data.error === 'Object does not exist.'){
                        userItemContainer.innerHTML = '<p class="text-center text-white">No users available.</p>';
                    } else {
                        const phoneError = document.getElementById('phone_error');
                        phoneError.textContent = data.error;
                        phoneError.style.display = 'block';
                        phoneError.classList.add('is-invalid');
                    }
                } else {
                    const userItem = document.createElement('a');
                    userItem.href = window.DETAIL_USER;
                    userItem.className = 'btn btn-primary btn-lg mb-3 d-flex flex-column justify-content-center';
                    userItem.style.width = '100%';
                    userItem.style.height = '70px';
                    userItem.style.overflow = 'hidden';
                    const avatarSrc = data.avatar;
                    userItem.innerHTML = `
                        <div class="d-flex align-items-center">
                            <img src="${avatarSrc}" alt="${data.username} avatar" class="rounded-circle" style="width: 50px; height: 50px; object-fit: cover; margin-right: 10px;">
                            <div class="d-flex flex-column">
                                <span class="text-truncate" style="max-width: 100%; overflow: hidden; text-overflow: ellipsis;">${data.username}</span>
                                <small class="text-white-50" style="margin-top: auto;">
                                    ${data.phone_number}
                                </small>
                            </div>
                        </div>
                    `;
                    userItemContainer.appendChild(userItem);
                    userItem.addEventListener('click', function(event) {
                        event.preventDefault();
                        sessionStorage.setItem('selectedUser', data.id);
                        window.location.href = window.DETAIL_USER;
                    });
                }
            })
            .catch(error => console.error('Error fetching chat data:', error));
        } else {
            userItemContainer.innerHTML = '';
        }
    });
    document.addEventListener('submit', function(event) {
        event.preventDefault();
    });
});
