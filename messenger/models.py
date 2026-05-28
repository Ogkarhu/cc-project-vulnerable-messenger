from django.db import models

    
    
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    isadmin = models.BooleanField(default=False)
    #from django.contrib.auth.models import AbstractUser
    #   class User(AbstractUser):
    #     user_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=30, default="")
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #recipient = models.ForeignKey(User, related_name='incoming_messages', on_delete=models.CASCADE)
    recipient = models.IntegerField()
    # msg_id = models.AutoField(primary_key=False)
    msg_id = models.IntegerField()
    message = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
