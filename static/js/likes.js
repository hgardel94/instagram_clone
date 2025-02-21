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
    const messageLiked = {
        0: 'Be the first to like this',
        1: 'You liked this',
        2: 'You and 1 other liked this',
        default: `You and ${likes-1} others liked this`,
    }

    const messageNotLiked = {
        0: 'Be the first to like this',
        1: '1 person liked this',
        default:`${likes} people liked this`,
  }

  if (liked === true){
    element.text(messageLiked[likes] || messageLiked.default)
  }if (liked === false){
    element.text(messageNotLiked[likes] || messageNotLiked.default)
  }
  
  
}
