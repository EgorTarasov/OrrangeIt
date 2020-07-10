import datetime
from random import randint, choice

import requests
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView, DeleteView

from orrangeit.tokens import account_activation_token
from orrangeit_app.models import EventInfo, Comment, Tag, User, GalleryImage
from .forms import SignUpForm, LogInForm, CommentForm, CreateEventForm, UserEditForm


def get_begin_with_offset():
    today = datetime.datetime.now()
    delta_begin = datetime.timedelta(hours=2)
    begin = today + delta_begin
    begin.strftime('%Y-%m-%d %H:%M')
    return begin


def get_end_with_offset():
    today = datetime.datetime.now()
    delta_end = datetime.timedelta(days=1, hours=2)
    end = today + delta_end
    end.strftime('%Y-%m-%d %H:%M')
    return end


def index(request):
    # TODO: Документация Лендинг page
    """
    Регистрация пользователя и возможность зайти в профиль
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        if request.user.is_active:
            return redirect('feed_page')
        else:
            return redirect('email_verification')
    else:
        context = dict()
        if request.method == 'POST':
            if 'sign_up_button' in request.POST:
                form = SignUpForm(request.POST)
                if form.is_valid():
                    context['errors'] = []
                    email = form.cleaned_data.get('email')
                    name = form.cleaned_data.get('name')
                    username = form.cleaned_data.get('username')
                    password = form.cleaned_data.get('password1')
                    password_confirm = form.cleaned_data.get('password2')

                    if User.objects.filter(email=email).count() > 0:
                        context['form'] = form
                        context['errors'].append('This email is already used')
                        return render(request, 'index.html', context)

                    u = User.objects.create(username=username, email=email, first_name=name)
                    u.set_password(password)
                    u.is_active = False
                    u.save()

                    login(request, u)

                    current_site = get_current_site(request)
                    mail_subject = 'Activate your OrrangeIt account.'
                    message = render_to_string('registration/email_activation_letter.html', {
                        'user': u,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(u.pk)),
                        'token': account_activation_token.make_token(u),
                    })
                    email = EmailMessage(
                        mail_subject, message, to=[email]
                    )
                    email.send()
                    # return HttpResponse("We`ve sent you a verification letter")
                    return redirect('email_verification')
                else:
                    context['form'] = form
                    context['login_form'] = LogInForm()

            elif 'log_in_button' in request.POST:
                form = LogInForm(request.POST)
                if form.is_valid():
                    context['login_errors'] = []
                    if form.data['username'] in User.objects.all().values_list('username', flat=True):
                        username = form.cleaned_data.get('username')
                        password = form.cleaned_data.get('password')

                        user = authenticate(username=username, password=password)
                        if user is not None:
                            login(request, User.objects.get(username=username))
                            return redirect('feed_page')
                        else:
                            context['login_errors'].append('Password is incorrect')
                    else:
                        context['login_form'] = LogInForm()
                        context['form'] = SignUpForm()
                        context['login_errors'].append('There is no user with that username')
                context['login_form'] = LogInForm()
                context['form'] = SignUpForm()
        else:
            context['form'] = SignUpForm()
            context['login_form'] = LogInForm()
        return render(request, 'index.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('index')
    else:
        return HttpResponse('Activation link is invalid or something else went wrong ;(')


def email_verification(request):
    # TODO: Документация email_verification
    """
    Подтверждение почты
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        if request.user.is_active:
            return redirect('feed_page')

    return render(request, 'registration/email_verification.html', {})


@login_required
def user_logout(request):
    """
    Функция для выхода из профиля
    :param request:
    :return:
    """
    logout(request)
    return redirect('index')


def event_page(request, event_id):
    # TODO: Документаци event_page
    """
    Отображение данных о мероприятии с чатом и созданием qr_code
    :param request:
    :param event_id:
    :return:
    """
    try:
        context = dict()
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comment(
                    user=request.user,
                    text=form.data['text'],
                    event_id=event_id,
                    date=timezone.now()
                )
                form.full_clean()
                comment.save()

        event = EventInfo.objects.get(pk=event_id)
        event.check_if_repeated()
        context['event'] = event
        context['event_id'] = context['event'].id
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(event_id=event_id).order_by('-date')
        context['participants'] = event.event_participants.all()
        context['gallery'] = event.gallery.all()
        return render(request, 'event_page.html', context)
    except EventInfo.DoesNotExist:
        raise Http404


@login_required
def follow_unfollow_event(request, event_id, action_type):
    event = get_object_or_404(EventInfo, id=event_id)
    if action_type:
        event.event_participants.add(request.user)
    else:
        event.event_participants.remove(request.user)
    event.save()
    return redirect('event_page', event_id=event_id)


class DeleteEventView(DeleteView):
    model = EventInfo
    success_url = reverse_lazy('feed_page')
    template_name = 'eventinfo_confirm_delete.html'


class EditEventView(UpdateView):
    # TODO: Документаци
    model = EventInfo
    template_name = 'event_creation.html'
    form_class = CreateEventForm

    def get_object(self):
        event_id = self.kwargs.get("event_id")
        return get_object_or_404(EventInfo, id=event_id)

    def form_valid(self, form):
        context = dict()
        context['tags'] = Tag.objects.all()
        context['errors'] = []
        event_people_participating = 0
        event_begin = form.data['event_begin']
        event_end = form.data['event_end']
        event_begin = datetime.datetime.strptime(event_begin, '%Y-%m-%d %H:%M')
        event_end = datetime.datetime.strptime(event_end, '%Y-%m-%d %H:%M')
        cur_datetime = datetime.datetime.today()
        img = form.cleaned_data.get("image")
        if event_begin < cur_datetime:
            context['errors'].append('You cannot arrange an event in the past')
            context['form'] = form
            return render(self.request, 'event_creation.html', context)

        print(event_end.date, event_begin.date)
        if event_end < event_begin:
            context['errors'].append('Event can`t finish before it begins')
            context['form'] = form
            return render(self.request, 'event_creation.html', context)

        event = EventInfo(
            event_begin=event_begin,
            event_end=event_end,
            event_name=form.cleaned_data['event_name'],
            event_description=form.cleaned_data['event_description'],
            event_people_needed=form.cleaned_data['event_people_needed'] if form.data['event_people_needed'] else -1,
            event_address=form.cleaned_data['event_address'],
            event_author=self.request.user,
            event_people_participating=event_people_participating,
            image=img
        )

        tagname = form.data['new_tagname'].lower().split(' ')
        if tagname != '':
            for tag in tagname:
                try:
                    new_tag = Tag.objects.get(tag=tag)
                    event.event_tags.add(new_tag)
                except:
                    pass
            event.save()
        return redirect('event_page', event_id=event.id)

    def form_invalid(self, form):
        context = dict()
        context['tags'] = Tag.objects.all()
        context['errors'] = []
        context['form'] = form
        return render(self.request, 'event_creation.html', context)


class CreateEventView(CreateView):
    template_name = 'event_creation.html'
    form_class = CreateEventForm
    success_url = 'feed/'
    model = EventInfo

    def form_valid(self, form):
        context = dict()
        context['errors'] = []
        if EventInfo.objects.filter(event_name=form.data['event_name']).count() > 0:
            context['errors'].append('Event with this name already exists')
            context['form'] = form
            return render(self.request, 'event_creation.html', context)
        event_begin = form.data['event_begin']
        event_end = form.data['event_end']

        event_begin = datetime.datetime.strptime(event_begin, '%Y-%m-%d %H:%M')
        event_end = datetime.datetime.strptime(event_end, '%Y-%m-%d %H:%M')
        cur_datetime = datetime.datetime.today()
        img = form.cleaned_data.get("image")

        if event_begin < cur_datetime:
            context['errors'].append('You cannot arrange an event in the past')
            context['form'] = form
            return render(self.request, 'event_creation.html', context)

        if event_end < event_begin:
            context['errors'].append('Event can`t finish before it begins')
            context['form'] = form
            return render(self.request, 'event_creation.html', context)

        event = EventInfo(
            event_begin=event_begin,
            event_end=event_end,
            event_name=form.cleaned_data['event_name'],
            event_description=form.cleaned_data['event_description'],
            event_people_needed=form.cleaned_data['event_people_needed'] if form.data['event_people_needed'] else -1,
            event_address=form.cleaned_data['event_address'],
            event_author=self.request.user,
            image=img
        )

        if 'telegram_group_link' in form.cleaned_data.keys():
            event.telegram_chat = form.cleaned_data['telegram_group_link']
            print()

        event.save()

        if 'gallery_images' in form.cleaned_data.keys():
            for img in self.request.FILES.getlist('gallery_images'):
                img = GalleryImage.objects.create(
                    image=img
                )
                img.save()
                event.gallery.add(img.id)

        event.save()

        event.event_participants.add(self.request.user)
        tags = form.data['event_tags'].lower().split()
        for tag in tags:
            if not Tag.objects.filter(tag=tag).exists():
                current_tag = Tag(tag=tag)
                current_tag.save()
            else:
                current_tag = Tag.objects.get(tag=tag)
            event.event_tags.add(current_tag.id)
            event.save()
        return redirect('event_page', event_id=event.id)

    def form_invalid(self, form):
        context = dict()
        context['errors'] = []
        context['form'] = form
        return render(self.request, 'event_creation.html', context)


@login_required
def feed(request):

    """
    Главная страница с мероприятиями
    :param request:
    :return:
    """
    if request.user.is_active:
        context = dict()
        context['events'] = EventInfo.objects.all()
        context['tags'] = Tag.objects.all()
        return render(request, 'feed.html', context)
    else:
        return redirect('email_verification')


@login_required
def search_tags(request, tag_id):
    """
    Функция поиска тегов из БД
    :param request:
    :param tag_id:
    :return:
    """
    if request.user.is_active:
        context = dict()
        context['events'] = EventInfo.objects.filter(event_tags__in=[tag_id])
        context['tags'] = Tag.objects.all()
        return render(request, 'feed.html', context)
    else:
        return redirect('email_verification')


@login_required
def search_view(request):
    """
    Функция поиска мероприятия по запросу
    :param request:
    :return:
    """
    context = dict()
    question = request.GET.get('q')
    if question is not None:
        context['events'] = EventInfo.objects.filter(
            Q(event_name__icontains=question) | Q(event_author__first_name=question)
        )

    return render(request, 'search_results.html', context)


def user_page(request, username):
    """
    Профиль польщователя
    :param request:
    :param username:
    :return:
    """
    context = dict()
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = UserEditForm(request.POST)
        if bool(request.FILES) == True:
            user.user_avatar = request.FILES['user_avatar']
            user.save()
        else:
            pass
            # form['user_avatar'] = user.user_avatar
        if form.is_valid() and request.user.is_authenticated:
            for key in request.POST.keys():
                if key != 'csrfmiddlewaretoken' and request.POST[key] != '':
                    setattr(user, key, request.POST[key])
                    user.save()
            return redirect('user_page', username=user.username)

    if request.user == user:
        new_form = UserEditForm
        new_form.first_name = user.first_name
        new_form.email = user.email
        context['edit_info'] = new_form

    context['events'] = EventInfo.objects.filter(event_author=user)

    return render(request, 'profile.html', context)


URL = 'https://kudago.com/public-api/v1.4/events/?lang=en&fields=name,title,dates,location,place,tags,description,images&expand=images&order_by=&text_format=&ids=&location=msk&actual_since=1590883200&actual_until=1591747200'
IMAGES_ROUTE = 'images/'
IMAGES = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg', '9.jpg', '10.jpg']
responce = requests.get(URL)
RESPONCE_JSON = responce.json()


def generate(request):
    responce = requests.get(URL)
    responce_json = responce.json()
    for result in responce_json['results']:
        state = True
        print('+++++++++++++++++++++++++++++++++++')
        event_tags = result['tags']
        for tag in event_tags:
            if tag == '18+' or tag == 'с парнем':
                print('-----------------------------------')
                print('+++++++++++++++++++++++++++++++++++')
                state = False
        dates = result['dates']

        date_start = datetime.datetime.fromtimestamp(dates[0]['start'])
        if date_start < datetime.datetime.now():
            date_start = datetime.datetime.now()
        date_end = datetime.datetime.fromtimestamp(dates[0]['end'])
        if date_end <= date_start or date_end > datetime.datetime(2020, 6, 12, 0, 0, 0):
            date_end = datetime.datetime(2020, 6, 11, 0, 0, 0)
        event_name = result['title']

        event_description = result['description']
        event_people_needed = randint(0, 100)
        event_author = 1
        event_image_url = result['images'][0]['image']
        image = IMAGES_ROUTE + IMAGES[randint(0, 9)]
        if state:
            new_event = EventInfo(
                event_name=event_name,
                event_author=request.user,
                event_description=event_description,
                image=choice(IMAGES),
                event_people_needed=event_people_needed

            )
            new_event.save()
            print('event_name: ' + event_name)
            print('event_description: ' + event_description)
            print('event_author_id: ' + str(event_author))
            print('event_tags: ' + str(event_tags))
            print('event_begin: ' + str(date_start))  # .strftime('%Y-%m-%d %H:%M:%S')
            print('event_end: ' + date_end.strftime('%Y-%m-%d %H:%M:%S'))
            print('event_image: ' + str(result['images']))
            print('event_address: ' + str(result['place']))
            print('+++++++++++++++++++++++++++++++++++')
        if not state:
            print('bad event')

            pass

        input()
