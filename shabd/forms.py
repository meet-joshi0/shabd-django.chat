from django import forms
from django.contrib.auth import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from . models import ChatGroup, CustomeUserProfile
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm, fields
from django.core.validators import RegexValidator,MinLengthValidator

alphanumeric = RegexValidator(r'^[\w]+$')
minimum_length = MinLengthValidator(3)




class RegistrationForm(UserCreationForm):

    name = forms.CharField( label="name", max_length=100 ,widget=forms.TextInput(
        attrs={"class": 'form-control mt-2 mb-2  border border-1 border-dark',  'data-toggle':"tooltip", 'data-placement':"bottom", 'title':" please enter your name "  }))

    username = forms.CharField(label="username", max_length=100,validators=[alphanumeric] ,widget=forms.TextInput(
        attrs={"class":"form-control mt-2 mb-2 text-lowercase border border-1 border-dark",'data-toggle':"tooltip", 'data-placement':"bottom",'pattern':"[\w]+" ,'title':" please enter your username ",'minlength':"3"}))

    email = forms.EmailField(label="email", help_text="please enter valid email address",
                             max_length=200, widget=forms.EmailInput(attrs={"class": 'form-control mt-2 mb-2 border border-1 border-dark',  'data-toggle':"tooltip", 'data-placement':"bottom", 'title':" please enter your email address "  }))


    DoB = forms.DateField(label="dob", required=True,widget=forms.TextInput(attrs={'type': 'date',"class": 'form-control mt-2 my-2 border border-1 border-dark',  'data-toggle':"tooltip", 'data-placement':"bottom", 'title':" please enter your birthday "  }))


    userImage = forms.ImageField(label="userimage", required=False, widget=forms.FileInput(
        attrs={"class": 'form-control mt-2 mb-2 border border-1 border-dark',  'data-toggle':"tooltip", 'data-placement':"bottom", 'title':" please upload your profile picture "  }))
   

    class Meta(UserCreationForm.Meta):
        model = CustomeUserProfile
        fields = ('name', 'username', 'email',  'DoB',
                  'password1', 'password2', 'userImage')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs['class'] = "form-control text-dark mt-2 mb-2 border border-1 border-dark"
        self.fields['password1'].widget.attrs['data-toggle'] = "tooltip"
        self.fields['password1'].widget.attrs['data-placement'] = "bottom"
        self.fields['password1'].widget.attrs['title'] = "please enter password"
        self.fields['password1'].widget.attrs['minlength'] = 8


        self.fields['password2'].widget.attrs['class'] = "form-control mt-2 mb-2 border border-1 border-dark"
        self.fields['password2'].widget.attrs['data-toggle'] = "tooltip"
        self.fields['password2'].widget.attrs['data-placement'] = "bottom"
        self.fields['password2'].widget.attrs['title'] = "please repeat password"
        self.fields['password2'].widget.attrs['minlength'] = 8


    
    def clean_username(self):
        cleaned_data = self.cleaned_data["username"]
        return cleaned_data.lower()
    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password != confirm_password:
            raise forms.ValidationError(
                "passwords  does not match"
            )


class updateUserRegistratioForm(UserChangeForm):
    
    
    username = forms.CharField(max_length=100,disabled=True, widget=forms.TextInput(
        attrs={ "class": 'form-control text-lowercase mb-2 border border-1 border-dark '}))
 
   
    name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": 'form-control mb-2 border border-1 border-dark'}))

    password = forms.CharField(max_length=400,required=False ,widget=forms.PasswordInput(
    attrs={"class": 'form-control mb-2 border border-1 border-dark'}))
   

   
    email = forms.EmailField(help_text="please enter valid email address",
                             max_length=200, widget=forms.EmailInput(attrs={"class": 'form-control mb-2 border border-1 border-dark'}))


    DoB = forms.DateField(required=True,widget=forms.TextInput(attrs={'type': 'date',"class": 'form-control  mb-2 border border-1 border-dark'}))


    userImage = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={"class": 'form-control mb-2 border border-1 border-dark'}))

    class Meta:
        model = User
        fields = ('username','name','password', 'email',  'DoB','userImage')
   



# ----------------------------------------


class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']

      

 
      
# ------------------------------------------



class GroupForm(ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['groupname', 'groupImage','description']
        
        widgets = {
            'groupname':forms.TextInput(
                attrs={
                    'class':'form-control fst-italic fs-3 '
                }
            )
            ,
            'groupImage': forms.FileInput(
				attrs={
					'class': 'form-control  form-control-lg'
					}
				),
            'description':forms.Textarea(
                    attrs=
                    {
                        'class' : 'form-check-input h-25 w-100 fst-italic fs-4 '
                    }

            ),
                }

    def clean_groupname(self):
        cleaned_data = self.cleaned_data["groupname"]
        return cleaned_data.lower()


        






