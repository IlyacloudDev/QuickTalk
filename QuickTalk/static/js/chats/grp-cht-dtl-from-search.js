document.addEventListener('DOMContentLoaded', function () {
    const chatId = sessionStorage.getItem('selectedChatId');
    const userId = document.getElementById('userId').value;

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if (!chatId) {
        alert('No chat selected!');
        return;
    }

    const apiUrl = `/api/chats/detail-chat/${chatId}/`;

    fetch(apiUrl)
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch chat data');
        }
        return response.json();
    })
    .then(result => {
        const chatInfoContainer = document.getElementById('chatInfo');
        const chatInfoHtml = `
            <div class="text-center">
                <h3 class="text-white"><i class="fa-solid fa-people-group fa-lg"></i>${result.detail.chat_name}</h3>
                <small class="text-white-50" style="margin-top: auto;">
                    ${result.detail.type} chat
                </small>
            </div>
        `;
        chatInfoContainer.innerHTML = chatInfoHtml;
        const buttonChattingContainer = document.getElementById('userChatting');
        buttonChattingContainer.innerHTML = `
            <button id="groupChatting" class="btn btn-light btn-lg">
                <i class="fa-solid fa-paper-plane"></i> Message
            </button>
        `;
        document.getElementById('groupChatting').addEventListener('click', function (e) {
            e.preventDefault();
            const data = {
                user_id_to_join: userId,
                chat_id_to_join: result.detail.id
            };
            fetch(window.JOIN_TO_GROUP_CHAT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                if (data.detail === "The user has already joined this group chat.") {
                    alert("You are already joined to this chat. Redirecting...");
                    window.location.href = window.LIST_API_CHATS;
                } else if (data.detail === "The user was successfully added to the chat.") {
                    window.location.href = window.LIST_API_CHATS;
                } 
            })
            .catch(error => {
                console.error('Error joining group chat:', error);
            });
        })
    })
    .catch(error => {
        console.error('Error fetching user data:', error);
        const chatInfoContainer = document.getElementById('chatInfo');
        chatInfoContainer.innerHTML = '<p class="text-center text-danger">Failed to load chat details.</p>';
    });
})
