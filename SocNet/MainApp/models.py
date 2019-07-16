from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    NOT_ADDED = 0
    MALE = 1
    FEMALE = 2

    SEX_OF_USER = (
        (NOT_ADDED, 'Not added'),
        (MALE, "Male"),
        (FEMALE, 'Female')
    )

    NO = 0
    YES = 1

    FIELD_YES_NO = (
        (NO, 'Not added'),
        (YES, "added"),
    )

    status = models.CharField(max_length=40, default='', blank=True)
    surname = models.CharField(max_length=40, default='', blank=True, verbose_name="patronymic", help_text='(optional)')
    country = models.CharField(max_length=60, default='', blank=True)
    city = models.CharField(max_length=60, default='', blank=True)
    hobby = models.TextField(max_length=200, default='', blank=True)
    sex = models.PositiveSmallIntegerField(choices=SEX_OF_USER, default=NOT_ADDED, null=True)
    date_of_join = models.DateTimeField(auto_now=True)
    is_avatar_add = models.PositiveSmallIntegerField(choices=FIELD_YES_NO, default=NO, null=True)
    is_subscribe_to_somebody = models.PositiveSmallIntegerField(choices=FIELD_YES_NO, default=NO, null=True)

    def get_full_name(self):
        name = f'{self.surname} {self.first_name} {self.last_name}'
        return name


class Subscribe(models.Model):
    ON_BLACK_LIST_TRUE = 1
    ON_BLACK_LIST_FALSE = 0

    USING_YES_NO = (
        (ON_BLACK_LIST_TRUE, 'Using'),
        (ON_BLACK_LIST_FALSE, "Doesn't use")
    )
    user_who_subscribe = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_subscribe")
    user_on_whom_subscribe = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_on_whom_subscribe")
    on_black_list = models.PositiveSmallIntegerField(choices=USING_YES_NO, default=ON_BLACK_LIST_FALSE, null=True)


class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=80, verbose_name='Name of Post', unique=True)
    body = models.TextField(verbose_name='Text of Post')
    rating = models.IntegerField(default=0)
    date_of_add = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PictureToPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='picture/')


class Avatar(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatar/')
    date_of_add = models.DateTimeField()

    def __str__(self):
        return str(self.user) + ": " + str(self.avatar)


class AvatarUsed(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.OneToOneField(Avatar, on_delete=models.SET_NULL, null=True)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="message_sender", null=True)
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="message_receiver", null=True)
    text = models.TextField(max_length=300)
    date_of_add = models.DateTimeField()


class ChatsListCurrentMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="chat_last_message_sender", null=True)
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="chat_last_message_receiver", null=True)
    message = models.OneToOneField(Message, on_delete=models.CASCADE, related_name="chat_last_message")
    date_of_add = models.DateTimeField(auto_now=True)




