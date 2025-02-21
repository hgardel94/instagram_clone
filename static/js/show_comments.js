document.addEventListener('DOMContentLoaded', () => {
    const modal = new bootstrap.Modal(document.getElementById('postModal'));
    const modalImg = document.getElementById('modal-img');
    const modalComments = document.getElementById('modal-comments');
    const commentForm = document.getElementById('comment-form');
    const commentText = document.getElementById('comment-text');
    let currentPostId = null;

    
    const loadCommentsAndShowModal = (postId) => {
        fetch(`/posts/post/${postId}/`)
            .then(response => response.text())
            .then(html => {
                modalComments.innerHTML = html;
                modalImg.src = document.querySelector(`[data-post-id="${postId}"]`).closest('.post').querySelector('.post-pic').src;
                modal.show();
            })
            .catch(err => console.error('Error to load comments:', err));
    };

    
    const handleCommentSubmit = (event) => {
        event.preventDefault();

        if (!currentPostId) return;

        const formData = new URLSearchParams({
            'text': commentText.value
        });

        fetch(`/posts/add_comment/${currentPostId}/`, {
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
            if (data.success) {
                const newComment = document.createElement('p');
                newComment.innerHTML = `
                    <img src="${data.comment.profile_pic}" class="profile-pic me-2 mt-2" alt="Foto de perfil">
                    <strong>${data.comment.user}</strong> ${data.comment.text} <small class="text-muted">${data.comment.created_at}</small>`;
                modalComments.appendChild(newComment);
                commentText.value = ''; 
            } else {
                console.error('Error to add comment:', data.errors);
            }
        })
        .catch(err => console.error('Error AJAX request:', err));
    };

    
    document.querySelectorAll('.open-modal').forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            currentPostId = link.getAttribute('data-post-id');
            loadCommentsAndShowModal(currentPostId);
        });
    });

    commentForm.addEventListener('submit', handleCommentSubmit);
});