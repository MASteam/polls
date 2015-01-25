#coding: utf8
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from coffin.shortcuts import render_to_response
from django.template import Context, loader
from models import Polls, Options, OptionsVotes, Comments
from utils import get_client_ip
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
import random
import json
from django.core import serializers
from PIL import Image, ImageDraw, ImageFont, ImageOps
import StringIO
import datetime, time
from django.views.decorators.csrf import csrf_protect, requires_csrf_token, csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import re


def profile(request, username):
    x = cache.get('user_filter_%s' % username)
    if x:
        user = x
    else:
        user = User.objects.filter(username=username)
        cache.set('user_filter_%s' % username, user)
    if user.count() < 1:
        c = Context({
            'error': u'Пользователь не найден',
            'user': request.user
        })
        return render_to_response('error.html', c)
    else:
        y = cache.get('user_objects_get_%s' % username)
        if y:
            user = y
        else:
            user = User.objects.get(username=username)
            cache.set('user_objects_get_%s' % username, user)
        u = cache.get('polls_objects_filter_user_%s' % username)
        if u:
            user_polls = u
        else:
            user_polls = Polls.objects.filter(user=user).order_by('-id')
            cache.set('polls_objects_filter_user_%s' % username, user_polls)
        c = Context({
            'user': request.user,
            'profile': user,
            'polls': user_polls
        })
        return render_to_response('profile.html', c)

def delete(request, id):
    poll = Polls.objects.get(id=id)
    if Polls.objects.filter(id=id).count() < 1 or poll.user != request.user:
        return HttpResponseRedirect('/')
    else:
        comments = Comments.objects.filter(poll=poll)
        comments.delete()
        options_votes = OptionsVotes.objects.filter(poll=poll)
        options_votes.delete()
        options = Options.objects.filter(poll=poll)
        options.delete()
        poll.delete()
        cache.delete('all_polls')
        return HttpResponseRedirect('/')


@login_required
def new_poll(request):
    if request.method == "POST":
        option_list = request.POST.getlist('option[]')
        error = []
        options = []
        error2 = []
        if len(option_list) > 10:
            error2.append(u'Слишком много вариантов, хакир')
        if len(option_list) < 2:
            error2.append(u'Слишком мало вариантов, хакир')
        print len(option_list)
        print len(error2)
        for key, value in enumerate(option_list):
            if len(value) < 2 or len(value) > 15:
                error.append(key)
            options.append([key, value])
        if len(error) > 0 or len(error2) > 0:
            c = Context({
                'user': request.user,
                'head_menu': 'vote_new',
                'error': error,
                'error2': error2,
                'options': options,
                'post': 1,
                'poll_name': request.POST.get('poll_name')
            })
            c.update(csrf(request))
            return render_to_response('new_poll.html', c)
        else:
            poll = Polls()
            poll.user = request.user
            poll.name = request.POST.get('poll_name')
            poll.save()

            last_id = Polls.objects.latest('id')

            for key, value in options:
                option = Options()
                option.poll = last_id
                option.name = value
                option.count = 0
                option.save()
                cache.delete('all_polls')
            return HttpResponseRedirect('/poll/%s/' % (last_id.id))
    else:
        options = []
        [options.append(i) for i in xrange(1, 6)]
        c = Context({
            'user': request.user,
            'head_menu': 'vote_new',
            'options': options
        })
        c.update(csrf(request))
        return render_to_response('new_poll.html', c)


def _login(request):
    if request.method == "POST":
        username = request.POST['user']
        password = request.POST['pass']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                c = Context({
                    'user': request.user,
                    'error': u'Пользователь не активирован',
                    'backlink': '/auth/',
                })
                c.update(csrf(request))
                return render_to_response('error.html', c)
        else:
            # Return an 'invalid login' error message.
            c = Context({
                'user': request.user,
                'error': u'Неверный логин или пароль',
                'backlink': '/auth/',
            })
            c.update(csrf(request))
            return render_to_response('error.html', c)
    else:
        c = Context({
            'user': request.user,
        })
        c.update(csrf(request))
        return render_to_response('auth.html', c)


def _logout(request):
    if request.method == "POST":
        logout(request)
        return HttpResponseRedirect('/')
    else:
        c = Context({
            'user': request.user,
        })
        c.update(csrf(request))
        return render_to_response('logout.html', c)


@csrf_exempt
def _register(request):
    error = []
    if request.method == "POST":
        #error = []
        passw = request.POST.get('pass')
        passw2 = request.POST.get('pass2')
        username = request.POST.get('user').strip()
        mail = request.POST.get('mail')
        captcha = request.POST.get('captcha')
        if captcha != request.session['captcha']:
            error.append(u'Код с картинки введён неверно')
        user = User.objects.filter(username=request.POST.get('user'))
        if user.count() > 0:
            error.append(u'Пользователь с таким ником уже существует')
        if len(username) < 4 or len(username) > 15:
            error.append(u'Длинный/короткий ник')
        nickregex = re.compile(r"^([a-z0-9]+)$", re.I | re.M | re.S)
        if not nickregex.match(username):
            error.append(u'В нике присутствуют запрещённые символы')
        if len(passw) < 6 or len(passw) > 16:
            error.append(u'Длинный/короткий пароль')
        if passw != passw2:
            error.append(u'Пароли не совпадают')

        from django.core.exceptions import ValidationError
        from django.core.validators import validate_email
        try:
            validate_email(mail)
        except ValidationError as e:
            error.append(u'Неправильно введён e-mail')

        if len(error) < 1:
            user = User.objects.create_user(username=username, email=mail, password=passw)
            user.save()
            user = authenticate(username=username, password=passw)
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            c = Context({
                'user': request.user,
                'error': error,
                'usernick': username,
                'passw': passw,
                'passw2': passw2,
                'email': mail,
                'captcha': captcha,
            })
            return render_to_response('reg.html', c)
    else:
        c = Context({
            'user': request.user,
            'error': error,
        })
        return render_to_response('reg.html', c)


def index(request):
    x = cache.get('all_polls')
    if x:
        polls = x
    else:
        polls = Polls.objects.all().order_by('-id')
        cache.set('all_polls', polls, 60)
        cache.close()

    c = Context({
        'polls': polls,
        'user': request.user
    })
    return render_to_response('index.html', c)


def generate_captcha(request):
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    img = Image.new('RGBA', (160, 80), color)
    imgDrawer = ImageDraw.Draw(img)
    textImg = Image.new('RGBA', (160, 80))
    tmpDraw = ImageDraw.Draw(textImg)
    font = ImageFont.truetype("resources/UbuntuMono-RI.ttf", 26)
    i = 15
    key = []
    for x in xrange(1, 7):
        r = str(random.randint(0, 9))
        key.append(r)
        tmpDraw.text((i, random.randint(20, 30)), r,
                     font=font, fill=(0, 0, 0))
        i += 22
    request.session['captcha'] = ''.join(key)
    for o in xrange((80 * 160) / 500):
        imgDrawer.line((random.randint(0, 160), random.randint(0, 80), random.randint(0, 160), random.randint(0, 80)),
                       fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    output = StringIO.StringIO()
    textImg = textImg.rotate(random.randint(-20, 20))
    mask = Image.new('RGBA', (160, 80), (0, 0, 0))
    mask.paste(textImg, (0, 0))
    img.paste(textImg, (0, 0), mask)
    img.save(output, format='png')
    return StreamingHttpResponse([output.getvalue()], content_type="image/png")


def show(request, id):
    x = cache.get('poll_id__' + id)
    if x:
        poll = x
    else:
        poll = Polls.objects.filter(id=id)
        cache.set('poll_id__' + id, poll)
        cache.close()
    if poll.count() < 1:
        return HttpResponse('Not found')
    else:
        x = cache.get('polls_objects_get_id_%s' % id)
        if x:
            poll = x
        else:
            poll = Polls.objects.get(id=id)
            cache.set('polls_objects_get_id_%s' % id, poll)
        y = cache.get('options_objects_filter_poll_id_%s_order_by_-count' % id)
        if y:
            options = y
        else:
            options = Options.objects.filter(poll_id=id).order_by('-count')
            cache.set('options_objects_filter_poll_id_%s_order_by_-count' % id, options)
        c_cache = cache.get('comments_poll_id__' + id)
        if c_cache:
            comments = c_cache
        else:
            comments = Comments.objects.filter(poll_id=id).order_by('-id')
            cache.set('comments_poll_id__' + id, comments)

        paginator = Paginator(comments, 10)

        page = request.GET.get('p')
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        u = cache.get('optionsvotes_objects_filter_poll_poll.id_%s' % poll.id)
        if u:
            options_c = u
        else:
            options_c = OptionsVotes.objects.filter(poll=poll.id).count()
            cache.set('optionsvotes_objects_filter_poll_poll.id_%s' % poll.id, options_c)

        c = Context({
            'poll': poll,
            'options': options,
            'options_c': options_c,
            'comments': comments,
            'user': request.user
        })
        c.update(csrf(request))

        return render_to_response('show.html', c)


def vote(request, id):
    option = Options.objects.get(id=id)
    poll = Polls.objects.get(id=option.poll_id)
    option_vote = OptionsVotes.objects.filter(poll_id=poll.id, user_ip=get_client_ip(request))

    if option_vote.count() > 0:
        c = Context({
            'error': u'Вы уже голосовали в этом опросе',
            'user': request.user,
            'backlink': '/poll/%i/' % poll.id
        })
        print poll.id
        return render_to_response('error.html', c)
    else:
        option.count += 1
        option.save()

        ov = OptionsVotes()
        ov.poll_id = poll.id
        ov.vote_id = option.id
        ov.user_ip = get_client_ip(request)
        ov.save()
        
        cache.delete('polls_objects_get_id_%s' % poll.id)
        

        return HttpResponseRedirect('/poll/%i' % poll.id)


@login_required()
def comment(request, id):
    if len(request.POST['text']) < 1:
        c = Context({'error': u'Вы не ввели текст', 'user': request.user})
        return render_to_response('error.html', c)

    poll = Polls.objects.filter(id=id)
    if poll.count() < 1:
        c = Context({'error': u'Опрос не найден', 'user': request.user})
        return render_to_response('error.html', c)
    else:
        if not 'last_msg' in request.session:
            ts = time.time()
            request.session['last_msg'] = 0

        ts = time.time()
        if request.session['last_msg'] + 15 > ts:
            c = Context({
                'user': request.user,
                'error': u'Не так быстро. Попробуйте написать сообщение через %i сек.' % (
                int(request.session['last_msg']) - ts + 15),
                'backlink': '/poll/%s/' % (id),
            })
            return render_to_response('error.html', c)
        else:
            page = request.GET.get('p')
            if not page:
                page = 1

            c = Comments()
            c.poll_id = id
            #c.name = request.POST['name']
            c.user = request.user
            c.text = request.POST['text']
            c.user_ip = get_client_ip(request)
            c.time = datetime.datetime.now()
            c.save()

            cache.delete('comments_poll_id__' + id)

            request.session['last_msg'] = int(time.time())

            return HttpResponseRedirect('/poll/%s/?p=%s' % (id, page))
