import datetime
from django.utils import timezone
from itertools import chain
from django.conf import settings
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models.functions import datetime
from django.http import QueryDict, JsonResponse
from django.views import View
from .forms import AvatarAdd, UserInfo, ChangeStatus, PictureToPostForm, PostForm
from django.shortcuts import redirect
from django.views.generic import TemplateView, DetailView, UpdateView, ListView
from .models import User, Post, Avatar, AvatarUsed, Subscribe, Message, ChatsListCurrentMessage


class UserPage(TemplateView):
    template_name = "MainApp/UserPage.html"

    def __init__(self, **kwargs):
        super(UserPage, self).__init__(**kwargs)
        self.form_avatar_add = AvatarAdd
        self.form_user_info = UserInfo
        self.form_change_status = ChangeStatus
        self.form_post, self.form_post_picture = PostForm, PictureToPostForm

    def get_context_data(self, **kwargs):
        context = super(UserPage, self).get_context_data(**kwargs)
        if not self.request.user.is_anonymous:
            context['user'] = User.objects.prefetch_related('avatar_set').get(id=self.request.user.pk)
        else:
            pass
        context["AvatarForm"] = self.form_avatar_add()
        context["UserInfoForm"] = self.form_user_info(instance=self.request.user).as_table()
        context["StatusForm"] = self.form_change_status(instance=self.request.user).as_p()
        context["AvatarBase"] = context['user'].avatar_set.all().order_by('-date_of_add')
        context['PostForm'] = self.form_post().as_p()
        User_posts = Post.objects.prefetch_related('picturetopost_set').filter(creator=self.request.user)\
            .order_by('date_of_add')
        context['Posts'] = User_posts.order_by('-date_of_add')[:50]
        context['post_from_subscribe'] = Post.objects.none()
        for elem in self.request.user.user_who_subscribe.all():
            context['post_from_subscribe'] = chain(context['post_from_subscribe'],
                                                   elem.user_on_whom_subscribe.post_set.all())
        context['post_from_subscribe'] = list(reversed(sorted(chain(context['post_from_subscribe'], User_posts),
                                                key=lambda instance: instance.date_of_add)))[:50]
        return context

    def get(self, request, **kwargs):
        if request.user.is_anonymous:
            return redirect('login')
        render_to_response = super(UserPage, self).get(request, **kwargs)
        return render_to_response

    def post(self, request):
        if 'avatar' in request.FILES:
            form = self.form_avatar_add(request.POST, request.FILES)
            if form.is_valid():
                image = form.save(commit=False)
                image.user = request.user
                image.date_of_add = datetime.datetime.now()
                image.save()
            return redirect('/')
        elif 'first_name' in request.POST or 'status' in request.POST:
            form = self.form_user_info(request.POST, instance=request.user) if 'first_name' in request.POST \
                else self.form_change_status(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
            return redirect('/')
        elif 'name' in request.POST:
            form = self.form_post(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.creator = request.user
                post.save()
                if request.POST.get('picture') != '':
                    picture_form = self.form_post_picture(request.POST, request.FILES)
                    if picture_form.is_valid():
                        picture = picture_form.save(commit=False)
                        picture.post = Post.objects.get(name=request.POST.get('name'))
                        picture.save()
            return redirect('/')


class AvatarSupActions(View):

    def put(self, request):
        # save avatar as main
        request_data = QueryDict(request.body)
        pk = request_data.get('AvatarManualId')
        # get data about avatar picture and create or update a AvatarUsed model and change status
        # 'is_avatar_add' for user
        try:
            avatar = AvatarUsed.objects.get(user=request.user)
            avatar.avatar = Avatar.objects.get(pk=pk)
            avatar.save()
        except:
            AvatarUsed.objects.create(user=request.user, avatar=Avatar.objects.get(pk=pk))
        finally:
            user = User.objects.get(pk=request.user.id)
            user.is_avatar_add = 1
            user.save()
        return JsonResponse({'status': 'success'})

    def delete(self, request):
        # delete avatar picture from Avatar model
        request_data = QueryDict(request.body)
        avatar_to_dell = Avatar.objects.get(user=request.user, pk=request_data.get('idToDelete'))
        # check if delete avatar picture is a main avatar of user
        if request.user.avatarused.avatar.pk == avatar_to_dell.pk:
            user = User.objects.get(pk=request.user.id)
            user.is_avatar_add = 0
            user.save()
        avatar_to_dell.delete()
        return JsonResponse({'status': 'success'})


class PostChange(UpdateView):
    template_name = 'MainApp/PostChange.html'
    model = Post
    form_class = PostForm


class SearchUsers(ListView):
    template_name = 'MainApp/SearchUsers.html'
    paginate_by = 20
    context_object_name = "users"

    def get_queryset(self):
        question = self.request.GET.get('search')
        if question is not None:
            self.queryset = User.objects.prefetch_related('avatar_set').filter(username__contains=question)
        else:
            self.queryset = User.objects.all().order_by('-date_of_join')
        queryset = super(SearchUsers, self).get_queryset()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchUsers, self).get_context_data(**kwargs)
        question = self.request.GET.get('search')
        context['last_question'] = '?search=%s' % question
        subscribe_list = []
        for elem in self.request.user.user_who_subscribe.all():
            subscribe_list.append(elem.user_on_whom_subscribe.username)
        context['subscribes'] = subscribe_list
        return context


class SubscribeActions(View):

    # def get(self, request):
    #     startwith = int(request.GET.get('startWith'))
    #     user_posts = Post.objects.prefetch_related('picturetopost_set').filter(creator=request.user) \
    #         .order_by('-date_of_add')
    #     post_from_subscribe = Post.objects.none()
    #     for elem in self.request.user.user_who_subscribe.all():
    #         post_from_subscribe = chain(post_from_subscribe, elem.user_on_whom_subscribe.post_set.all())
    #     post_from_subscribe = reversed(sorted(chain(post_from_subscribe, user_posts),
    #                                           key=lambda instance: instance.date_of_add))
    #     posts_after_serialize = serializers.serialize('json', list(post_from_subscribe)[startwith:(startwith + 10)],
    #                                                   fields=('creator', 'name', 'body', 'creator.avatarused.avatar.avatar.url'))
    #     return JsonResponse(posts_after_serialize, safe=False)

    def post(self, request):
        request_data = QueryDict(request.body)
        if 'userId' in request_data:
            Subscribe.objects.get_or_create(user_who_subscribe=request.user,
                                     user_on_whom_subscribe=User.objects.get(pk=request_data.get('userId')))
            subscribes = Subscribe.objects.filter(user_who_subscribe=request.user.id)
            user = User.objects.get(pk=request.user.id)
            if subscribes != "" and user.is_subscribe_to_somebody == 0:
                user.is_subscribe_to_somebody = 1
                user.save()
        return JsonResponse({'status': 'success'})

    def delete(self, request):
        request_data = QueryDict(request.body)
        if 'userId' in request_data:
            Subscribe.objects.filter(user_who_subscribe=request.user,
                                     user_on_whom_subscribe=User.objects.get(pk=request_data.get('userId'))).delete()
            subscribes = Subscribe.objects.filter(user_who_subscribe=request.user.id)
            user = User.objects.get(pk=request.user.id)
            if subscribes == "" and user.is_subscribe_to_somebody == 1:
                user.is_subscribe_to_somebody = 0
                user.save()
        return JsonResponse({'status': 'success'})


class MessageRoom(ListView):
    template_name = 'MainApp/MessageRoom.html'
    context_object_name = 'messages'

    def get_queryset(self):
        interlocutor = User.objects.get(pk=self.kwargs.get('pk'))
        income_message = Message.objects.filter(sender=interlocutor, receiver=self.request.user)
        sent_message = Message.objects.filter(sender=self.request.user, receiver=interlocutor)
        self.queryset = sorted(chain(income_message, sent_message), key=lambda instance: instance.date_of_add)
        queryset = super(MessageRoom, self).get_queryset()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MessageRoom, self).get_context_data(**kwargs)
        context['interlocutor'] = self.kwargs.get('pk')
        return context


    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(MessageRoom, self).get_context_data(**kwargs)
    #     for elem in context['view']:
    #         print(elem)
    #     return context


class MessageActions(View):

    def post(self, request):
        request_data = QueryDict(request.body)
        # take user receiver
        receiver = User.objects.get(pk=request_data.get('interlocutor'))
        # create message
        message = Message.objects.create(sender=request.user, receiver=receiver,
                               text=request_data.get('text'), date_of_add=datetime.datetime.now())
        # add this massage as last to this user
        try:
            last_message = ChatsListCurrentMessage.objects.get(sender=request.user, receiver=receiver)
        except ObjectDoesNotExist:
            ChatsListCurrentMessage.objects.create(sender=request.user, receiver=receiver, message=message)
        else:
            last_message.message = message
            last_message.save()
        # convert date to format
        our = datetime.datetime.now().strftime('%I')
        our = list(our)[1] if list(our)[0] == '0' else our
        am_or_pm = ' a.m.'if int(datetime.datetime.now().strftime('%H')) < 12 else ' p.m.'
        date = datetime.datetime.now().strftime('%B %d, %Y, i:%M')
        date = date.split('i')[0] + our + date.split('i')[1] + am_or_pm
        return JsonResponse({'date': date, 'id': message.pk})

    def put(self, request):
        request_data = QueryDict(request.body)
        # change message
        message = Message.objects.get(pk=request_data.get('messageId'))
        message.text = request_data.get('text')
        message.save()
        return JsonResponse({'status': 'success'})

    def delete(self, request):
        request_data = QueryDict(request.body)
        # take message
        message = Message.objects.get(pk=request_data.get('idToDelete'))
        # take last message throw special model
        last_message = ChatsListCurrentMessage.objects.get(sender=request.user,
                                                           receiver_id=int(request_data.get('interlocutor')))
        # change related field ChatsListCurrentMessage model if OneToOne field connected with delete message
        if message == last_message.message:
            messages = Message.objects.filter(sender=request.user, receiver_id=int(request_data.get('interlocutor')))
            last_message.message = messages[(len(messages)-2)]
            last_message.save()
        message.delete()
        return JsonResponse({'status': 'success'})


class AllSubscribes(ListView):
    template_name = 'MainApp/Subscribes.html'
    paginate_by = 20
    context_object_name = "subscribes"

    def get_queryset(self):
        if self.request.user.is_subscribe_to_somebody:
            self.queryset = Subscribe.objects.prefetch_related('user_on_whom_subscribe')\
                .filter(user_who_subscribe=self.request.user)
        else:
            self.queryset = Subscribe.objects.none()
        queryset = super(AllSubscribes, self).get_queryset()
        return queryset


class Chats(TemplateView):
    template_name = 'MainApp/Chats.html'

    def get_context_data(self, **kwargs):
        context = super(Chats, self).get_context_data()
        send_message = list(ChatsListCurrentMessage.objects.select_related('message').prefetch_related('receiver')
                            .filter(sender=self.request.user).order_by('-date_of_add'))
        income_message = list(ChatsListCurrentMessage.objects.select_related('message').prefetch_related('sender')
                              .filter(receiver=self.request.user).order_by('-date_of_add'))
        send_message_dict = {}
        list_elem_num = 0
        for elem in send_message:
            send_message_dict.update({str(elem.receiver): [elem.id, list_elem_num]})
            list_elem_num += 1
        list_elem_num = 0
        for elem in income_message:
            if str(elem.sender) in send_message_dict.keys():
                if elem.id > send_message_dict[str(elem.sender)][0]:
                    send_message.pop(send_message_dict[str(elem.sender)][1])
                else:
                    send_message.pop(list_elem_num)
            list_elem_num += 1
        context['chats'] = chain(income_message, send_message)
        return context


if settings.DEBUG:
    try:
        spamer = User.objects.create_user(username='Spamer', password='n660676')
    except IntegrityError:
        spamer = User.objects.get(username='Spamer')
    if spamer.post_set.all():
        pass
    else:
        for elem in range(30):
            spamer.post_set.create(creator=spamer, name=(f"Name{elem}" * 3), body=(f" Body{elem}" * 10))


