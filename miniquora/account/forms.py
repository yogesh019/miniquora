from django import forms
from .models import MyUser
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username=forms.CharField(max_length=25);
    password=forms.CharField(widget=forms.PasswordInput)

    def __init__(self,*args,**kwargs):
        self.authenticated_user=None;
        super(LoginForm,self).__init__(*args,**kwargs);

    #gets called automatically when isvalid is called
    def clean_username(self): 
        username=self.cleaned_data['username']
        if MyUser.objects.filter(username=username).count()!=1:
            raise forms.ValidationError('Invalid Username');
        return username;
  
    def clean(self):
        username=self.cleaned_data.get('username','');
        passwd=self.cleaned_data.get('password','');
        user=authenticate(username=username,password=passwd);
        if(username and passwd and not user):
            raise forms.ValidationError('Username/Password does not match')
        if user and user.is_active==False:
            raise forms.ValidationError('Inactive User')
        self.authenticated_user=user;
        return self.cleaned_data;

class ForgotPassword(forms.Form):
    username=forms.CharField(max_length=100)

    def clean_username(self):
        data_username=self.cleaned_data.get('username','')
        if data_username and not MyUser.objects.filter(username=data_username).exists():
            raise forms.ValidationError("Invalid Username")
        return data_username

class SetPassword(forms.Form):
    new_password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)

    def clean_confirm_password(self):
        data_new_password=self.cleaned_data.get('new_password')
        data_confirm_password=self.cleaned_data.get('confirm_password')
        if(data_new_password and data_confirm_password and data_new_password!=data_confirm_password):
            raise forms.ValidationError("The 2 password fields didn't match")
        return data_confirm_password


class SignupForm(forms.ModelForm):
    password=forms.CharField(max_length=20,widget=forms.PasswordInput)
    confirm_password=forms.CharField(max_length=20,widget=forms.PasswordInput)
    
    def clean_email(self):
        data_email=self.cleaned_data.get('email','')
        if not data_email:
            raise forms.ValidationError("This field is required!")
        if MyUser.objects.filter(email=data_email).exists():
            raise forms.ValidationError('User with this email already exists')
        return data_email

    def clean_confirm_password(self):
        data_password=self.cleaned_data.get('password')
        data_confirm_password=self.cleaned_data.get('confirm_password')
        if(data_password and data_confirm_password and data_password!=data_confirm_password):
            raise forms.ValidationError("The 2 password fields didn't match")
        return data_confirm_password
    
    class Meta:
        model=MyUser
        fields=['username','email','phone','first_name','last_name','profile_pic']

