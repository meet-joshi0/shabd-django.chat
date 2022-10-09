from distutils.command.upload import upload
from email.mime import image
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.core.validators import MinLengthValidator,RegexValidator
from dropbox.dropbox_client import Dropbox
from django.core.files.base import ContentFile
from chat.settings import DROPBOX_OAUTH2_TOKEN
from django.core.files.images import ImageFile
from shabd.utils.utils import get_file_from_dropbox
from storages.backends.dropbox import DropBoxStorage

dbx = Dropbox(DROPBOX_OAUTH2_TOKEN)
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
class GroupImages(models.Model):
    groupImage = models.ImageField(upload_to = "images/", blank=True)
class ChatGroup(models.Model):
    groupname = models.CharField(max_length=40,blank=True,unique=True,validators=[minimum_length,alphanumeric])
    time = models.DateTimeField( auto_now_add=True)

    groupImage = models.ImageField(upload_to = "images/",blank=True,
        storage = DropBoxStorage())
    description = models.TextField(blank=True) 
    image = models.ForeignKey(GroupImages, on_delete=models.CASCADE,null=True, blank=True, default="")
    
    def __str__(self):
        return self.groupname

    @property
    def get_group_image(self):
        group_img = None

        if self.groupImage and not self.image:
            drpbx_response = get_file_from_dropbox(str(self.groupImage))
            group_img= GroupImages.objects.create(groupImage = drpbx_response)
            self.image = group_img
            self.save()
            group_img = self.image.groupImage
        elif self.image:
            group_img = self.image.groupImage
        return group_img
class FriendsList(models.Model):
    friends = models.ForeignKey(CustomeUserProfile,on_delete=CASCADE,related_name="friend")
    usernm = models.CharField(max_length=350)
    
    def __str__(self) -> str:
        return str(self.usernm)

