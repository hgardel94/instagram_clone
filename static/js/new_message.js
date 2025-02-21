document.addEventListener('DOMContentLoaded', () => {
    
    const messageModalEl = document.getElementById('messageModal');
    const messageModal = new bootstrap.Modal(messageModalEl);
    const newConversationModal = new bootstrap.Modal(document.getElementById('newConversationModal'));
    const chatContainer = document.getElementById('conversation-messages');
    const friendSelectContainer = document.getElementById('friendSelect');
    const modalBody = document.getElementById('modal-body');
  
    let currentConversationId = null;
    let currentRecipient = null;
  
    
    function getCSRFToken() {
      const csrfCookie = document.cookie.split('; ')
        .find(cookie => cookie.startsWith('csrftoken='));
      return csrfCookie ? csrfCookie.split('=')[1] : null;
    }
  
    
    function secureFetch(url, options = {}) {
      const headers = options.headers || {};
      headers['X-CSRFToken'] = getCSRFToken();
      return fetch(url, {
        ...options,
        headers: {
          ...headers,
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      });
    }
  
   
    function scrollToBottom() {
      modalBody.scrollTop = modalBody.scrollHeight;
    }
  
    
    function loadFriends() {
      secureFetch('/directs/load_users/')
        .then(response => response.json())
        .then(users => {
          friendSelectContainer.innerHTML = '';
          users.forEach(user => {
            const friendItem = document.createElement('div');
            friendItem.className = 'user-item';
            friendItem.dataset.userId = user.id;
            friendItem.dataset.username = user.username;
            friendItem.dataset.profilePic = user.image;
            friendItem.innerHTML = `
              <img src="${user.image}" class="message-profile-pic" alt="Perfil">
              <span class="user-username">${user.username}</span>
            `;
            friendSelectContainer.appendChild(friendItem);
          });
        })
        .catch(error => console.error('Error to load firends:', error));
    }
  
    
    function loadMessagesAndShowModal(conversationId, otherUser, profilePic) {
      secureFetch(`/directs/thread/${conversationId}/`)
        .then(response => response.text())
        .then(html => {
          chatContainer.innerHTML = html;
          chatContainer.dataset.conversationId = conversationId;
          document.getElementById('modal-profile-pic').src = profilePic;
          document.getElementById('modal-username').textContent = otherUser;
          messageModal.show();
          setTimeout(scrollToBottom, 200);
          
        })
        .catch(error => console.error('Error to load messages:', error));
    }
  
    
    function checkExistingConversation() {
      secureFetch(`/directs/check_conversation/${currentRecipient.id}/`)
        .then(response => response.json())
        .then(data => {
          if (data.conversation_id) {
            currentConversationId = data.conversation_id;
            
            newConversationModal.hide();
            loadMessagesAndShowModal(currentConversationId, currentRecipient.username, currentRecipient.image);
          } else {
           
            newConversationModal.hide();
            prepareNewConversation();
          }
        })
        .catch(error => console.error('Error to verify conversation:', error));
    }
  
    // Preparar el modal para una nueva conversación (sin ID asignado aún)
    function prepareNewConversation() {
      document.getElementById('modal-profile-pic').src = currentRecipient.image;
      document.getElementById('modal-username').textContent = currentRecipient.username;
      chatContainer.innerHTML = '';
      messageModal.show();
      
    }
  
    
    document.querySelectorAll('.link-messages').forEach(link => {
      link.addEventListener('click', (event) => {
        event.preventDefault();
        currentConversationId = link.dataset.conversationId;
        currentRecipient = {
          username: link.dataset.otherUser,
          image: link.dataset.profilePic
        };
        loadMessagesAndShowModal(currentConversationId, currentRecipient.username, currentRecipient.image);
      });
    });
  
   
    document.getElementById('openNewMessageModal').addEventListener('click', () => {
      newConversationModal.show();
      loadFriends();
      
    });
  
    
    friendSelectContainer.addEventListener('click', (event) => {
      const userItem = event.target.closest('.user-item');
      if (userItem) {
        currentRecipient = {
          id: userItem.dataset.userId,
          username: userItem.dataset.username,
          image: userItem.dataset.profilePic
        };
        
        checkExistingConversation();
      }
    });
  
    
    document.addEventListener('submit', (event) => {
      if (event.target && event.target.matches('#message-form')) {
        event.preventDefault();
        
        if (!currentConversationId) {
          
          fetch('/directs/create_conversation/', {
            method: 'POST',
            headers: {
              'X-Requested-With': 'XMLHttpRequest',
              'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
              'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({ recipient_id: currentRecipient.id })
          })
          .then(response => response.json())
          .then(data => {
            
            if (data.success) {
              currentConversationId = data.conversation_id;
              sendMessage();
            } else {
              console.error('Error to create conversation:', data.error);
            }
          })
          .catch(error => console.error('Error to create conversation:', error));
        } else {
          sendMessage();
        }
      }
    });
  

    function sendMessage() {
      const messageInput = document.getElementById('message-input');
      const formData = new URLSearchParams({
        'content': messageInput.value
      });
      
      fetch(`/directs/send/${currentConversationId}/`, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        console.log("Respuesta de send:", data);
        if (data.success) {
          const messageDiv = document.createElement('div');
          messageDiv.className = 'conversation-content sender';
          messageDiv.innerHTML = `
            <div class="sender-user-container">
              <div class="message-sender">
                <p class="sender-text">${data.message.content}</p>
              </div>
              <div class="message-meta">
                <small class="time-sent">${data.message.timestamp}✔️</small>
              </div>
            </div>
          `;
          chatContainer.appendChild(messageDiv);
          messageInput.value = '';
          scrollToBottom();
        } else {
          console.error('Error to send the message:', data.error);
        }
      })
      .catch(error => console.error('Error to send message:', error));
    }
  });
  