from django.shortcuts import render, redirect, get_object_or_404
from .models import Conversation, Message
from django.contrib.auth.decorators import login_required
from django.utils import timezone

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
            
    
    messages_queryset = conversation.messages.all().order_by('timestamp').select_related('sender')
    
    messages = list(messages_queryset)
    
    for i, message in enumerate(messages):
        message.is_read_by_other = message.is_read_by(other_user)
        
        if message.sender != user:
             
            if i == len(messages) - 1 or messages[i + 1].sender == user:
                message.show_avatar = True
                continue
            if i == len(messages) - 1 or messages[i + 1].sender == user:
                message.show_avatar = False
                continue
        if message.sender == user:
            
            message.show_avatar = False

    return render(request, 'directs/thread.html', {
        'conversation': conversation,
        'messages': messages,
        'other_user': other_user,
    })

    
    



    

@login_required
def send_message(request, conversation_id):
    if request.method == 'POST':
        conversation = get_object_or_404(Conversation, id=conversation_id)
        content = request.POST.get('content', '').strip()
        
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            conversation.updated_at = timezone.now()  # Actualizar última actividad
            conversation.save()
    
    return redirect('directs:thread', conversation_id=conversation_id)