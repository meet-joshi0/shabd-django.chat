import redis
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from . models import ChatMessage,GroupMessage, ChatNotificationModel, CustomeUserProfile
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from datetime import datetime
from django.utils import timezone



# =================================================================== #
# ----------------------- GROUP CHAT  ------------------------------- #
# =================================================================== #

# stricrredis
r = redis.Redis(host='',port='',password='',db='',decode_responses=True)


class GroupChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

       

        user_name = str(self.scope['user'])
        username_group = "new_user_%s" % (user_name)
        add_online_user = await userList(self, user_name)
        user_data = await userInformationList(self, user_name)


    
        #send userdata to NewActiveGroupUser consumer
        await self.channel_layer.group_send(
             username_group,
            {
                "type": "chat_message",
                "message":  user_data,

            }
        )

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        user_name = str(self.scope['user'])

        #remove username from redis database
        r.srem(self.room_group_name, user_name)



        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):

        username = self.scope['user']
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.save_message(username,self.room_name,message)
        
        display_message = str(username) +" &nbsp:&nbsp " + message
      


        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'chat_message',
                'message': display_message,
            }
        )

    async def chat_message(self, event):

        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message,
        }))


    @sync_to_async

    # save group messages to database
    def save_message(self, username, group_name, message):

        GroupMessage.objects.create(
            sender=username, groupName=group_name, message=message)


# ================================================================== #
# ----------------------- ONE TO ONE CHAT -------------------------- #
# ================================================================== #


class UserChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        user1 = self.scope['url_route']['kwargs']['user_name1']
        user2 = self.scope['url_route']['kwargs']['user_name2']

        username = str(self.scope['user'])

        self.room_name = user1+user2
        self.room_group_name = 'chat_%s' % (self.room_name)

        if self.scope['user'].id:

            await self.channel_layer.group_add(
                self.room_group_name, self.channel_name
            )
    

        reciver = reciver_name(username, user1, user2)

        notifi_list = await self.getNotification(username, reciver)

        # send notification list to ChatNotification consumer
        await self.channel_layer.group_send(
            username, {
                'type': 'chat_message',
                'message': notifi_list,
            })

      

        await self.accept()

    async def disconnect(self,close_code):

        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        username = str(self.scope['user'])

        user1 = self.scope['url_route']['kwargs']['user_name1']
        user2 = self.scope['url_route']['kwargs']['user_name2']

        reciver = reciver_name(username, user1, user2)

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        await self.save_message(username, reciver, message)
        
        display_message = (str(username) + ' &nbsp; : &nbsp; ' + message)


        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'chat_message',
                'message': display_message,
            }
        )

    async def chat_message(self, event):

        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message,
        }))

    # save chat messages to database
    @sync_to_async
    def save_message(self, username, reciver, message):

        ChatMessage.objects.create(
            sender=username, reciver=reciver, message=message)

    # retrives stored notifications from database
    @sync_to_async
    def getNotification(self, username, reciver):
       
        userNotifications = []
        a = ChatNotificationModel.objects.filter(
            username=username).values('sender')
            
        for x in a:
            userNotifications.append(x['sender'])

        return userNotifications


# =================================================================== #
# ---------------------- CHAT NOTIFICATION -------------------------- #
# =================================================================== #


class ChatNotification(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_group_name = str(self.scope['user'])
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):

        text_data_json = json.loads(text_data)

        message = text_data_json['message']

        username = self.scope['user']
        reciver = message['reciver']

        await self.storeNotification(username, reciver)

        await self.channel_layer.group_send(
            reciver, {
                'type': 'chat_message',
                'message': message['username'],
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message,
        }))

    # stores user notification to database
    @sync_to_async
    def storeNotification(self, username, sender):
        ChatNotificationModel.objects.create(username=sender, sender=username)


# -----------------------------------------------------------------------------#
# -------------------------- Active Users in Group ----------------------------#
# -----------------------------------------------------------------------------#


class ActiveGroupUsers(AsyncWebsocketConsumer):

    async def connect(self):

        room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'active_%s' % (room_name)

        user_name = str(self.scope['user'])

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        user_data = await singleUserInformation(self, user_name)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": json.dumps(user_data),
            }
        )

        await self.accept()

    async def disconnect(self, close_code):

        username = str(self.scope['user'])
        status = {'disconnect': {'username': username}}

        #remove user from redis database
        r.srem(self.room_group_name, username)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": json.dumps(status),
            }
        )

        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):

        message = text_data

        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'chat_message',
                'message':  json.dumps(message),
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=message)


# ====================================================================== #
# ======================== New Active User ============================= #
# ====================================================================== #


class NewActiveGroupUsers(AsyncWebsocketConsumer):

    async def connect(self):

        user = str(self.scope['user'])
        self.room_group_name = 'new_user_%s' % (user)

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self,close_code):

        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):

        message = json.loads(text_data)

        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'chat_message',
                'message': message,
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message,
        }))


# get all joined userimages from database
@sync_to_async
def userInformationList(self, name):
    
    status = []

    for x in r.smembers(self.room_group_name):

        data = CustomeUserProfile.objects.filter(
            username=x).values('userImage')

        user_image = data[0]

        user_data = {
            'connect': {

                'username': x,
                'userimage': user_image['userImage'],

            }}

        status.append(user_data)

    return status

# fetches single userimage from database
@sync_to_async
def singleUserInformation(self, name):

    data = CustomeUserProfile.objects.filter(username=name).values('userImage')
    user_image = data[0]

    user_data = {
        'connect': {

            'username': name,
            'userimage': user_image['userImage'],
            'solo': "true"

        }}


    return user_data

# add username into redis database (set)
@sync_to_async
def userList(self, name):
    user_list = r.sadd(self.room_group_name, name)

    return user_list

# find reciver name given two name where username is logged  usersname 
def reciver_name(username, user1, user2):
    
    reciver = ""

    if user1 == username:
        reciver = user2
    elif user2 == username:
        reciver = user1
    else:
        reciver = "null"

    return reciver









