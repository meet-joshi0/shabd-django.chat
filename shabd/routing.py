from django.urls import re_path,path
from . import consumers

websocket_urlpatterns = [
   # re_path(r'ws/chat/(?P<room_name>\w+)/$',consumers.GroupChatConsumer.as_asgi()),
    path('ws/groupchat/<str:room_name>/',consumers.GroupChatConsumer.as_asgi()),
    path('ws/userchat/<str:user_name1>/<str:user_name2>/',consumers.UserChatConsumer.as_asgi()),
    path('ws/notification/<str:username>/',consumers.ChatNotification.as_asgi()),
    path('ws/activeusers/<str:room_name>/',consumers.ActiveGroupUsers.as_asgi()),
    path('ws/activeusernew/<str:username>/',consumers.NewActiveGroupUsers.as_asgi()),


]