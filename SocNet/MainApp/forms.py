from django import forms
from django_registration.forms import RegistrationForm
from .models import User, Avatar, PictureToPost, Post


class UserForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User


class AvatarAdd(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['avatar']


class UserInfo(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'surname', 'country', 'city', 'hobby', 'sex']


class ChangeStatus(forms.ModelForm):
    class Meta:
        model = User
        fields = ['status']


class PictureToPostForm(forms.ModelForm):
    class Meta:
        model = PictureToPost
        fields = ['picture']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'body']