from django.contrib import admin
from . models import CustomeUserProfile,ChatMessage,GroupMessage, ChatNotificationModel,ChatGroup,FriendsList
# Register your models here.

admin.site.register(CustomeUserProfile)
admin.site.register(ChatMessage)
admin.site.register(GroupMessage)
admin.site.register(ChatNotificationModel)
admin.site.register(ChatGroup)
admin.site.register(FriendsList)
