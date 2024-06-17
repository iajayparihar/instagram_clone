from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models import Max

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user')
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name='from_user')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,related_name='to_user')
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def send_message(sender,receiver,body):
        #sender message fun
        sender_message = Message(
            user=from_user,
            sender=from_user,
            receiver=to_user,
            is_read=True
        )
        sender_message.save()

        #receiver message fun
        receiver_message = Message(
            user=to_user,
            sender=from_user,
            receiver=from_user,
            is_read=True
        )
        receiver_message.save()
        return sender_message

    def get_message(user):
        messages = (Message.objects.filter(user=user).values('receiver').annotate(last=Max('date')).order_by('-last'))
        users = []
        for message in messages:
            users.append(
                {
                    "user": User.objects.get(id=message['receiver']),
                    'last': message['last'],
                    'unread': Message.objects.filter(user=user, receiver__id=message['receiver'], is_read=False).count()
                }
            )
        return users