$(document).on('click', '.like-button', function(e) {
    e.preventDefault(); // Prevenir el comportamiento por defecto (en caso de ser un formulario, etc.)
    
    var post_id = $(this).data('post-id');  // Obtener el ID del post
    var liked = $(this).data('liked');   // Comprobar si ya está likeado
    var url = liked ? '/posts/remove_like_post/' + post_id + '/' : '/posts/like_post/' + post_id + '/';  // Determinar la URL

    // Enviar la solicitud AJAX para dar o quitar like
    $.ajax({
        type: 'GET',
        url: url,
        success: function(response) {
            var button = $('#post-' + post_id + ' .like-button');
            var icon = button.find('i'); // Icono del corazón
            var likeMessage = $('#post-' + post_id + ' .like-message');
            button.data('liked', !liked); // Actualizar el estado de "liked"

            // Cambiar el ícono del corazón
            icon.toggleClass('bi-heart-fill text-danger bi-heart');

            var likes = response.likes;  // Obtener el nuevo número de likes

            // Actualizar el contador de likes
            $('#post-' + post_id + ' .likes-count').text(`${likes} likes`);

            // Actualizar el mensaje de los likes
            updateLikeMessage(likeMessage, likes, !liked);
        },
        error: function(xhr, errmsg, err) {
            console.error(xhr.status + ": " + xhr.responseText); // En caso de error
        }
    });
});

// Función para actualizar el mensaje según el número de likes
function updateLikeMessage(element, likes, liked) {
    if (likes === 0) {
        element.text('Be the first to like this');
        return;
    } 
    if (likes === 1 && liked) {
        element.text('You liked this');
        return;
    }
    if (likes === 1 && !liked) {
        element.text('1 person liked this');
        return;
    } 
    if (likes === 2 && liked) {
        element.text('You and 1 other person liked this');
        return;
    }
    if (likes >= 2 && liked) {
        element.text(`You and ${likes - 1} others liked this`);
        return;
    }
    if (likes >= 2 && !liked) {
        element.text(`${likes} people liked this`);
        return;
    }
}
