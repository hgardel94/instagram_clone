document.addEventListener('DOMContentLoaded', function() {
    var showCommentsLinks = document.querySelectorAll('.show-comments');

    showCommentsLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            var postId = this.getAttribute('data-post-id');
            var commentList = this.parentElement.nextElementSibling;

            // Si los comentarios están ocultos, los mostramos
            if (commentList.style.display === 'none' || commentList.style.display === '') {
                fetch(`/posts/comments/${postId}/`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok ' + response.statusText);
                        }
                        return response.json();
                    })
                    .then(comments => {
                        commentList.innerHTML = '';  // Limpia los comentarios previos
                        comments.forEach(comment => {
                            var profileImage = comment.user__profile__image || '/media/profile_images/default_user.png';
                            var commentDiv = document.createElement('div');
                            var commentDiv = document.createElement('div');
                            commentDiv.classList.add('comment');
                            commentDiv.innerHTML = `
                                <img src="${profileImage}" alt="Profile Image" class="rounded-circle" style="width: 30px; height: 30px; object-fit: cover;">
                                <p><strong>${comment.user__username}:</strong> ${comment.text}</p>
                            `;
                            commentList.appendChild(commentDiv);
                        });
                        commentList.style.display = 'block';
                        this.textContent = 'Hide comments';  // Cambia el texto a 'Hide comments'
                    })
                    .catch(error => console.error('Error:', error));
            } else {  // Si los comentarios ya están visibles, los ocultamos
                commentList.style.display = 'none';
                this.textContent = 'See the comments';  // Cambia el texto a 'See the comments'
            }
        });
    });
});
