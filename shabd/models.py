from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.core.validators import MinLengthValidator,RegexValidator


minimum_length = MinLengthValidator(3,message="groupname should be minimun three charachter long")
alphanumeric = RegexValidator(r'^[\w]+$')


# models
      
class CustomeUserProfile(AbstractUser):
    name = models.CharField(max_length=100,blank=True,null=True)
    userImage = models.ImageField(upload_to = "images/",default='default.jpg')
    DoB = models.DateField(null=True)

   


    def __str__(self):
        return self.username
    


class ChatMessage(models.Model):
    sender = models.CharField(max_length=100,blank=True)
    reciver = models.CharField(max_length=100,blank=True)
    message = models.CharField(max_length=10000,null=True)
    time = models.DateTimeField(auto_now_add=True) 


    def __str__(self):
        return self.message

class GroupMessage(models.Model):
    sender = models.CharField(max_length=100,blank=True)
    groupName = models.CharField(max_length=100,blank=True)
    message = models.CharField(max_length=10000,null=True)
    time = models.DateTimeField(auto_now_add=True) 

    


    def __str__(self):
        return self.groupName

class ChatNotificationModel(models.Model):
    username = models.CharField(max_length=40,blank=True)
    sender = models.CharField(max_length=40,blank=True) 


    def __str__(self):
        return self.username

class ChatGroup(models.Model):
    groupname = models.CharField(max_length=40,blank=True,unique=True,validators=[minimum_length,alphanumeric])
    time = models.DateTimeField( auto_now_add=True)
    groupImage = models.ImageField(upload_to = "images/",blank=True)
    description = models.TextField(blank=True) 
 
    def __str__(self):
        return self.groupname
    
    
class FriendsList(models.Model):
    friends = models.ForeignKey(CustomeUserProfile,on_delete=CASCADE,related_name="friend")

    usernm = models.CharField(max_length=350)
    
    def __str__(self) -> str:
        return str(self.usernm)

