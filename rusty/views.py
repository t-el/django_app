from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Relation
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.exceptions import ObjectDoesNotExist
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from .forms import PostForm

# Create your views here.
def home(request):
    return render(request, "index.html", {'title': "Rusty"})


def __register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        try:
            userfdb = User.objects.get(username=username)
            if userfdb is not None:
                return render(request, "register.html", {'title': "register", 'error': 'username already exist'})
        except Exception as e:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            profile = Profile(user=user)
            profile.statu = 0
            profile.save()
            return HttpResponseRedirect("login")

    else:
        return render(request, "register.html", {'title': "register"})


def __login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            profile = Profile.objects.get(user=user)
            if profile.statu == 0:
                return HttpResponseRedirect('completeprofile')
            else:
                return HttpResponseRedirect("/")
        else:
            return render(request, 'login.html', {'title': "login page"})
    elif request.method == "GET":
        return render(request, 'login.html', {'title': "login page"})


def articles(request):
    return render(request, "articles.html", {'title': "Articles"})


def __profile(request, username):
    if request.method == "POST":
        user = User.objects.get(username=username)
        if user:
            profile = Profile.objects.get(user=user)
            if request.FILES.get('img',None):
                path = default_storage.save(request.user.username+"_"+request.FILES['img'].name, ContentFile(request.FILES['img'].read()))
                tmp_file = os.path.join(settings.MEDIA_ROOT, path)
                profile.img = path
            profile.fullname = request.POST['fullname']
            profile.about = request.POST['about']
            profile.email = request.POST['email']
            location = request.POST['location']
            company = request.POST['company']
            profile.location = location
            profile.company = company
            profile.save()
            return HttpResponseRedirect(str(request.user))
    else:
        user = User.objects.get(username=username)
        if user:
            profile = Profile.objects.get(user=user)
            r = Relation.objects.filter(from_user=user)
            r2 = Relation.objects.filter(to_user=user)
            followers = Relation.objects.filter(from_user=request.user, to_user=profile.user).count()
            print(followers)
            st = "Follow"
            if followers > 0:
                st = "Unfollow"

            return render(request, "profile.html",
                          {'title': 'Profile', 'profile': profile, 'me': r, 'them': r2, 'st': st})
        else:
            return render(request, "index.html", {'title': 'Home'})


def __logout(request):
    logout(request)
    return HttpResponseRedirect("login")


def __cp(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("login")
    if request.method == "POST":
        fullname = request.POST['fullname']
        about = request.POST['about']
        profile = Profile.objects.get(user=request.user)
        profile.fullname = fullname
        profile.about = about
        profile.statu = 1
        profile.save()

        return HttpResponseRedirect("profile/" + request.user.username)
    return render(request, "complete_profile.html", {'title': 'Complete profile'})


@csrf_protect
def __relation(request):
    if request.is_ajax and request.method == "POST":
        if request.POST['st'] == "Follow":
            new_relation = Relation()
            to_user = User.objects.get(username=request.POST['to_user'])
            profile = Profile.objects.get(user = to_user )
            new_relation.profile = profile
            new_relation.from_user = request.user
            new_relation.to_user = to_user
            new_relation.statu = 'y'
            new_relation.save()
        else:
            to_user = User.objects.get(username=request.POST['to_user'])
            relation = Relation.objects.get(from_user=request.user, to_user=to_user)
            relation.delete()
        return JsonResponse({})
    else:
        following = Relation.objects.filter(from_user=request.user)
        followers = Relation.objects.filter(to_user=request.user)

        return render(request, "relations.html", {'title': 'Relations', 'followers': followers, 'following': following})


def __upload(request):
    if request.is_ajax and request.method == "Post":
        img = request.FILES['img']
        return JsonResponse({'img': img})
    else:
        return JsonResponse({})


def __add_post(request):
    if request.method == "POST":
        formset = PostForm(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
    else:
        formset = PostForm()
    return render(request, 'add_post.html', {'formset': formset})
