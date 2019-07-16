from django.urls import path

from .views import UserPage, AvatarSupActions, PostChange, SearchUsers, SubscribeActions, MessageRoom, AllSubscribes,\
    Chats, MessageActions

urlpatterns = [
    path('', UserPage.as_view(), name="UserPage"),
    path('AvatarSupActions', AvatarSupActions.as_view(), name="AvatarSupActions"),
    path('PostChange/(<int:pk>)', PostChange.as_view(), name="post_change"),
    path('SearchFriends', SearchUsers.as_view(), name='SearchUsers'),
    path('Subscribe', SubscribeActions.as_view(), name="Subscribe"),
    path('Chats/MessageRoom(<int:pk>)', MessageRoom.as_view(), name="MessageRoom"),
    path('AllSubscribes', AllSubscribes.as_view(), name="Subscribes"),
    path('Chats', Chats.as_view(), name="Chats"),
    path('MessageActions', MessageActions.as_view(), name="MessageActions"),
]