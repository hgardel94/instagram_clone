$(document).on('click', '.like-button', function(e) {
    e.preventDefault(); 
    
    var post_id = $(this).data('post-id');  
    var liked = $(this).data('liked');   
    var url = liked ? '/posts/remove_like_post/' + post_id + '/' : '/posts/like_post/' + post_id + '/';  // Determinar la URL

    $.ajax({
        type: 'GET',
        url: url,
        success: function(response) {
            var button = $('#post-' + post_id + ' .like-button');
            var icon = button.find('i'); 
            var likeMessage = $('#post-' + post_id + ' .like-message');
            button.data('liked', !liked); 

            
            icon.toggleClass('bi-heart-fill text-danger bi-heart');

            var likes = response.likes;  

            
            $('#post-' + post_id + ' .likes-count').text(`${likes} likes`);

            updateLikeMessage(likeMessage, likes, !liked);
        },
        error: function(xhr, errmsg, err) {
            console.error(xhr.status + ": " + xhr.responseText); 
        }
    });
});


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
