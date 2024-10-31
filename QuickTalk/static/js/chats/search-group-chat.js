document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('groupName');
    const searchResults = document.getElementById('groupChatItems');

    searchInput.addEventListener('input', function() {
        const query = searchInput.value.trim();
        const apiURL = `/api/chats/search-group-chat/?query=${encodeURIComponent(query)}`
        
        if (query.length > 0) {
            fetch(apiURL)
            .then(response => response.json())
            .then(data => {
                // Очищаем предыдущие результаты
                searchResults.innerHTML = '';
                
                if (data.length > 0) {
                    data.forEach(chat => {
                        const chatItem = document.createElement('a');
                        chatItem.href = window.DETAIL_CHAT;  // путь к чату
                        chatItem.className = 'btn btn-primary btn-lg mb-3 d-flex flex-column justify-content-center';
                        chatItem.style.width = '100%';
                        chatItem.style.height = '70px';
                        chatItem.style.overflow = 'hidden';

                        chatItem.innerHTML = `
                            <div class="d-flex align-items-center">
                                <div class="d-flex flex-column">
                                    <span class="text-truncate" style="max-width: 100%; overflow: hidden; text-overflow: ellipsis;">${chat.chat_name}</span>
                                    <small class="text-white-50" style="margin-top: auto;">
                                        <i class="fa-solid fa-people-group"></i>
                                        ${chat.type}
                                    </small>
                                </div>
                            </div>
                        `;
                        searchResults.appendChild(chatItem);
                        chatItem.addEventListener('click', function(event) {
                            event.preventDefault();
                            sessionStorage.setItem('selectedChatId', chat.id);
                            window.location.href = window.DETAIL_CHAT;
                        });
                    });
                } else {
                    searchResults.innerHTML = '<p class="text-center text-white">No chats available.</p>';
                }
            })
            .catch(error => console.error('Error fetching chat data:', error));
        } else {
            searchResults.innerHTML = ''; // Очищаем результаты, если запрос пустой
        }
    });
    document.addEventListener('submit', function(event) {
        event.preventDefault();
    });
});
