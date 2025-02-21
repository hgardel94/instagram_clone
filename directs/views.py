import json
from django.http import  JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Conversation, Message
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from accounts.models import  Profile
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models import Q





@login_required
def inbox(request):
    conversations = Conversation.objects.filter(participants=request.user).order_by('-updated_at')
    user = request.user
    for conversation in conversations:
        conversation.last_message = conversation.messages.last() 
        conversation.unread = conversation.messages.exclude(sender = user).exclude(read_by__has_key=str(request.user.id)).count()
        other_user = conversation.participants.exclude(id=request.user.id).first()
        conversation.other_user = other_user
        if conversation.last_message:
            conversation.last_message_unread = conversation.last_message.is_unread_by(request.user)

    return render(request, 'directs/inbox.html', {'conversations': conversations})



@login_required
def thread(request, conversation_id):
    user = request.user
    conversation = get_object_or_404(Conversation.objects.filter(participants=user), id=conversation_id)
    other_user = conversation.participants.exclude(id=user.id).first()

    if request.method == 'GET':
        unread_messages = conversation.messages.exclude(sender=user).exclude(read_by__has_key=str(user.id))
        for message in unread_messages:
            message.mark_as_read(user)

    messages = list(conversation.messages.all().order_by('timestamp').select_related('sender'))

    for i, message in enumerate(messages):  
        message.is_read_by_other = message.is_read_by(other_user)
        next_message = messages[i + 1] if i + 1 < len(messages) else None
        message.show_avatar = (message.sender != user) and (next_message is None or message.sender != next_message.sender)
        if message.sender == user:
            message.show_avatar = False
    
    return render(request, 
                 'directs/thread.html', 
                 {
                     'conversation': conversation,
                     'messages': messages,
                     'other_user': other_user,
                 })


def load_users(request):
    user = request.user
    followed_users = user.followings.values_list('following', flat = True)
    users_profile = Profile.objects.filter(Q(user__in = followed_users) | Q(user=user)).exclude(id=request.user.id)
    
    data = []
    for profile in users_profile:
        data.append({
            'id': profile.user.id,
            'username': profile.user.username,
            'image': profile.image.url if profile.image else '',  
            
        })
    
    return JsonResponse(data, safe=False)   

def validate_conversation(user, recipient):
    return Conversation.objects.filter(participants=user).filter(participants=recipient).distinct().first()


require_POST
def check_conversation(request, user_id):
    user = request.user
    recipient = get_object_or_404(User, id=user_id)
    conversation = validate_conversation(user, recipient)
    if conversation:
        return JsonResponse({'conversation_id': conversation.id})
    return JsonResponse({'conversation_id': None})



def send_message(request, conversation_id):
   
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Requieres AJAX request'}, status=400)
    
    content = request.POST.get('content')
    if not content:
        return JsonResponse({'success': False, 'error': 'The message is empty'}, status=400)
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    try:
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )
       
        timestamp = message.timestamp.strftime("%H:%M")
        return JsonResponse({
            'success': True,
            'message': {
                'content': message.content,
                'timestamp': timestamp
            }
        })
    except Exception as e:
        
        return JsonResponse({'success': False, 'error': str(e)}, status=500)



@require_POST
@login_required
def create_conversation(request):
    
    
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'You need AJAX request'}, status=400)
    
    recipient_id = request.POST.get('recipient_id')
    if not recipient_id:
        return JsonResponse({'success': False, 'error': 'You need a recipient'}, status=400)
    
   
    User = get_user_model()
    try:
        recipient = User.objects.get(pk=recipient_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Not recipient'}, status=404)
    
    candidate_conversations = Conversation.objects.filter(participants=request.user).filter(participants=recipient).distinct()
    
    conversation = None
    for conv in candidate_conversations:
        participant_ids = set(conv.participants.values_list('id', flat=True))
        if participant_ids == {request.user.id, recipient.id}:
            conversation = conv
            break

    if conversation:
        
        return JsonResponse({'success': True, 'conversation_id': conversation.id})
    if not conversation:
        
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, recipient)
        return JsonResponse({'success': True, 'conversation_id': conversation.id})
