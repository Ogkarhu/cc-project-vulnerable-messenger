from django.db import models

    
    
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    isadmin = models.BooleanField(default=False)
    password = models.CharField(max_length=30, default="")
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.IntegerField()
    msg_id = models.IntegerField()
    message = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
