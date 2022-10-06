import imp
from django.views.generic import View, TemplateView, FormView, ListView,CreateView,UpdateView
from . forms import RegistrationForm, updateUserRegistratioForm,LoginForm,GroupForm
from . models import CustomeUserProfile,AbstractUser, ChatMessage, ChatNotificationModel, ChatGroup, FriendsList, GroupMessage
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login
from django.core.paginator import  Paginator,InvalidPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from dropbox.base import DropboxBase  
# views 


class index(TemplateView):
    template_name = "index.html"

class usersList(ListView):
    model = CustomeUserProfile
    template_name = "user_list.html"
   
    paginate_by = 12

    def get_queryset(self, *args, **kwargs):
        param = self.request.GET.get('search')
        
        qs = ""
        if  param  :
            qs = CustomeUserProfile.objects.filter(username__icontains = param).values('username','userImage')
        else:
            qs = CustomeUserProfile.objects.values('username','userImage' )
        
        return qs

class groupList(CreateView):
    form_class = GroupForm
    success_url = reverse_lazy('grouplist')
    template_name = 'group_list.html'
    model = ChatGroup
    permission_required = ('shabd.can_view', )

    def post(self, request,*args, **kwargs):
        if request.user.is_authenticated:
            return super(groupList,self).post(request,*args, **kwargs)    
        else:
            return redirect('login')

    def get_context_data(self,**kwargs):
        context = super(groupList,self).get_context_data(**kwargs)
        param =   self.request.GET.get('search')
        page_number =  self.request.GET.get('num')
        context['object_list'] = "" 
        if  param  :
            context['object_list'] = ChatGroup.objects.filter(groupname__icontains=param).values('groupname','groupImage','description')
        else:
            context['object_list'] = ChatGroup.objects.all() #values('groupname','image__groupImage','description')

        context = paginate(context,context['object_list'],page_number)

        return context

class friendList(LoginRequiredMixin,ListView):
    model = FriendsList
    login_url = reverse_lazy("index")
    template_name = "friend_list.html"
    paginate_by = 12

    def get_queryset(self, *args, **kwargs):
        qs = FriendsList.objects.filter(usernm=self.request.user.username).select_related('friends')
        names = []

        for a in qs:
            friend_names = {}
            friend_names['username'] =  a.friends.username
            friend_names['userImage'] = str( a.friends.userImage )
            names.append(friend_names)
        return  names

class register(generic.CreateView):
    form_class = RegistrationForm
    template_name = "registration/register.html"
    #success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.save()
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'],)
        login(self.request, user)
        return HttpResponseRedirect(reverse('index'))
 
class updateResgister(generic.UpdateView):
    template_name= "update_registration.html"
    success_url = reverse_lazy("index")
    model= CustomeUserProfile
    form_class =  updateUserRegistratioForm

    def form_valid(self, form):
        if form.cleaned_data['password']:
            form.instance.set_password(form.cleaned_data['password'])
        else:
            del form.instance.password
        return super().form_valid(form)
 

class LoginView(FormView):
    template_name = "registration/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
       user = authenticate(
           username=self.request.POST['username'], password=self.request.POST['password'])
       login(self.request, user)
       return super(LoginView, self).form_valid(form)

class groupChat(LoginRequiredMixin, TemplateView, DropboxBase):
    template_name = "group_chat.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, *args, **kwargs):
        context = super(groupChat, self).get_context_data(
            *args, **kwargs)
        
        room_name = self.kwargs['room_name']
        group_messages =  GroupMessage.objects.filter(groupName=room_name).values('sender','message','time')[:200]
        extra_context = {'room_name': room_name,'group_messages':group_messages}

        return extra_context

class Active_group_users(LoginRequiredMixin,TemplateView):
    template_name = "active_group_users.html"
    login_url = reverse_lazy("index")

class ChatNotification(LoginRequiredMixin,TemplateView):
    template_name = "notification.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, *args, **kwargs):
        context = super(ChatNotification, self).get_context_data(
            *args, **kwargs)
        data = ChatNotificationModel.objects.all()
        context = {"dt": data}
        return context
class userchat(LoginRequiredMixin,TemplateView):
    template_name = "user_chat.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, *args, **kwargs):
        context = super(userchat, self).get_context_data(*args, **kwargs)
        user = self.request.user.username
        reciver1 = context['user_name1']
        reciver2 = context['user_name2']
        reciver = ""

        if reciver1 == user:
            reciver = reciver2
        elif reciver2 == user:
            reciver = reciver1
        else:
            reciver = "null"

        message1 = ChatMessage.objects.filter(
            Q(sender=user) & Q(reciver=reciver))
        message2 = ChatMessage.objects.filter(
            Q(sender=reciver) & Q(reciver=user))
        message = message1 | message2

        deleteUserNotifications = ChatNotificationModel.objects.filter(
            username=user, sender=reciver).delete()
            
        context = {"user_name": reciver, "message": message}
        return context

@login_required
def AddFriend(request):
        user =  request.user.username
        if request.method == 'POST':
            if request.POST.get('add_friend_name'):
               add_friend = request.POST['add_friend_name']
               friend = CustomeUserProfile.objects.get(username=add_friend)
               addName  = FriendsList.objects.create(usernm=user,friends=friend)
               return HttpResponse("True")
            else:
                if request.POST.get('remove_friend_name'):
                       remove_friend = request.POST['remove_friend_name']
                       friend = CustomeUserProfile.objects.get(username=remove_friend)
                       deleteFriend = FriendsList.objects.get(usernm=user,friends=friend).delete()
                       return HttpResponse(" deleted ")
        else:
            if request.method == 'GET':
               add_friend = request.GET['friend_name']
               friend = CustomeUserProfile.objects.get(username=add_friend)
               check_name =  FriendsList.objects.filter(usernm=user,friends=friend).exists()
               return HttpResponse(check_name)

def paginate(context, list,num):
        context = context
        paginato = Paginator(list,12)
        page = paginato.get_page(num)
                
        context["page_number"] = page
        context["group_list"] = page.object_list
        context["page_range"] = paginato.page_range
        
        context["has_next"] = page.has_next()
        context["current_page"] = page.number
        
        try:
            context["next_page_num"] = page.next_page_number()
        except InvalidPage:
            context["has_next"] = False

        context["has_previous"] = page.has_previous()

        try:
            context["previous_page_num"] = page.previous_page_number()
        except InvalidPage:
            context["has_previous"] = False

        return context
            
        

            
