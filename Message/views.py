from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Message.models import Message


@login_required
def inbox(request):
    user = request.user
    messages = Message.get_message(user=user)
    active_direct = None
    directs = None
    if messages:
        message = messages[0]
        active_direct = message['user'].username
        directs = Message.objects.filter(user=user,receiver=message['user'])
        directs.update(is_read=True)

        for msg in messages:
            if msg['user'].username == active_direct:
                msg['unread'] = 0
        context = {
            'directs':directs,
            'active_direct':active_direct,
            'messages': messages,
        }

        return render(request, 'chat/direct.html', context )
            
    return render(request, 'chat/direct.html' )