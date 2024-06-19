'use strict';

document.addEventListener('DOMContentLoaded', function () {
  // Initialize chat interface elements and functionalities
  initChatUI();
  // Fetch and display chat sessions as soon as the DOM is ready
  fetchChatSessions();
});
console.log("URL IN CHAT", BASE_URL)
// Initialize chat UI components and functionalities
function initChatUI() {
  const chatContactsBody = document.querySelector('.app-chat-contacts .sidebar-body'),
        chatHistoryBody = document.querySelector('.chat-history-body'),
        chatSidebarLeftBody = document.querySelector('.app-chat-sidebar-left .sidebar-body'),
        chatSidebarRightBody = document.querySelector('.app-chat-sidebar-right .sidebar-body'),
        formSendMessage = document.querySelector('.form-send-message'),
        messageInput = document.querySelector('.message-input'),
        searchInput = document.querySelector('.chat-search-input');

  // Initialize Perfect Scrollbar for chat UI elements
  new PerfectScrollbar(chatContactsBody, { wheelPropagation: false, suppressScrollX: true });
  new PerfectScrollbar(chatHistoryBody, { wheelPropagation: false, suppressScrollX: true });
  new PerfectScrollbar(chatSidebarLeftBody, { wheelPropagation: false, suppressScrollX: true });
  new PerfectScrollbar(chatSidebarRightBody, { wheelPropagation: false, suppressScrollX: true });

  // Event listener for sending messages
  formSendMessage.addEventListener('submit', function(event) {
    event.preventDefault();
    sendMessage();
  });

  // Event listener for chat search input
  if (searchInput) {
    searchInput.addEventListener('keyup', debounce(searchChats, 500));
  }
}

function fetchChatSessions() {
  fetch(`${BASE_URL}/chats/`)
    .then(response => response.json())
    .then(data => {
      const chatList = document.querySelector('#chat-list');
      chatList.innerHTML = ''; // Clear existing chat list

      data.forEach(session => {
        const avatarURL = session.participant1.avatar || 'img/avatars/1.png'; 

        const currentUserIdInt = parseInt(currentUserId, 10);

        let otherParticipant = session.participant1.id === currentUserIdInt ? session.participant2 : session.participant1;

        const listItem = document.createElement('li');
        listItem.className = 'chat-contact-list-item';
        
        // Inner HTML structure similar to your template
        listItem.innerHTML = `
          <a class="d-flex align-items-center">
            <div class="flex-shrink-0 avatar avatar-online">
              <img src="${avatarURL}" alt="A" class="rounded-circle">
            </div>
            <div class="chat-contact-info flex-grow-1 ms-2">
              <h6 class="chat-contact-name text-truncate m-0">${otherParticipant.username}</h6>
              <p class="chat-contact-status text-muted text-truncate mb-0">Active now</p> <!-- Example status -->
            </div>
            <small class="text-muted mb-auto">5 Minutes</small> <!-- Placeholder time -->
          </a>
        `;
        
        listItem.dataset.sessionId = session.id; // Store session ID for reference
        listItem.addEventListener('click', function() {
          setActiveChatSession(session.id);
        });

        chatList.appendChild(listItem);
      });
    })
    .catch(error => console.error('Error fetching chat sessions:', error));
}


// Fetch and display messages for the selected chat session
function fetchMessages(sessionId) {
  fetch(`${BASE_URL}/chats/${sessionId}/messages/`)
    .then(response => response.json())
    .then(data => {
      const messageList = document.querySelector('#chat-history');
      messageList.innerHTML = ''; // Clear existing messages

      const defaultAvatar = 'img/avatars/1.png';

      data.forEach(message => {
        // Create elements to match your original message structure
        const messageElement = document.createElement('li');
        messageElement.className = 'chat-message';

        // Convert both IDs to integers for comparison
        const authorId = parseInt(message.author.id, 10);
        const userId = parseInt(currentUserId, 10);

        if (authorId === userId) {
          messageElement.classList.add('chat-message-right');
        }

        messageElement.innerHTML = `
          <div class="d-flex overflow-hidden">
            <div class="user-avatar flex-shrink-0 me-3">
              <div class="avatar avatar-sm">
                <img src="${defaultAvatar}" alt="A" class="rounded-circle">
              </div>
            </div>
            <div class="chat-message-wrapper flex-grow-1">
              <div class="chat-message-text">
                <p class="mb-0">${message.content}</p>
              </div>
            </div>
          </div>
        `;
        messageList.appendChild(messageElement);
      });
      messageList.scrollTop = messageList.scrollHeight; // Scroll to the latest message
    })
    .catch(error => console.error('Error fetching messages:', error));
}

// Send a new message
function sendMessage() {
  const messageInput = document.querySelector('.message-input');
  const content = messageInput.value.trim();
  if (!content) return; // Do not send empty messages

  const sessionId = window.activeChatSessionId;
  if (!sessionId) {
    alert('Please select a chat session.');
    return;
  }

  fetch(`${BASE_URL}/chats/${sessionId}/messages/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrfToken()
    },
    body: JSON.stringify({ content })
  })
  .then(response => response.json())
  .then(() => {
    messageInput.value = ''; // Clear input after sending
    fetchMessages(sessionId); // Refresh the message list..
  })
  .catch(error => console.error('Error sending message:', error));
}

// Helper function to get CSRF token from cookies
function getCsrfToken() {
  const cookies = decodeURIComponent(document.cookie).split(';');
  for (let cookie of cookies) {
    const trimmedCookie = cookie.trim();
    if (trimmedCookie.startsWith('csrftoken=')) {
      return trimmedCookie.substring('csrftoken='.length);
    }
  }
  return '';
}

// Set the active chat session ID and fetch its messages
function setActiveChatSession(sessionId) {
  window.activeChatSessionId = sessionId;
  fetchMessages(sessionId);

  const chatListItem = document.querySelector(`[data-session-id="${sessionId}"] .chat-contact-name`);
  const chatHeaderName = document.querySelector('.chat-history-header .chat-contact-info h6');
  if (chatListItem && chatHeaderName) {
    chatHeaderName.textContent = chatListItem.textContent;
  }
}

// Debounce function to limit how often a function is executed
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Example search functionality (to be implemented based on backend capabilities)
function searchChats() {
  const searchTerm = document.querySelector('.chat-search-input').value;
  // Implement search functionality based on searchTerm
  console.log('Searching for:', searchTerm);
  // Ideally, you would make a fetch request to your backend search endpoint
}
