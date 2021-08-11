from django.urls import path
from shabd.views import groupList, index, register, groupChat,LoginView, updateResgister,userchat,usersList,friendList,ChatNotification,AddFriend,Active_group_users
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index.as_view(), name="index"),
    path('register', register.as_view(), name="register"),
    path('updregister/<pk>/',updateResgister.as_view(),name="updregister"),
    path('userlist',usersList.as_view(),name="userlist"),
    path('grouplist',groupList.as_view(),name="grouplist"),
    path('friendlist',friendList.as_view(),name="friendlist"),
    path('login',LoginView.as_view(),name="loginuser"),
    path('logout',auth_views.LogoutView.as_view(), name="logout"),
    path('room/<str:room_name>/',groupChat.as_view(),name="room"),
    path('actusers/',Active_group_users.as_view(),name="activeusers"),
    path('userroom/<str:user_name1>/<str:user_name2>/',userchat.as_view(),name="user"),
    path('notification/<str:username>/',ChatNotification.as_view(),name="notification"),
    path('addfriend',AddFriend,name="addfriend")
]

