from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import author, category, article
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .form import createForm, registerUser, createAuthor
from django.contrib import messages


# Create your views here.
def index(request):
    post = article.objects.all()
    search = request.GET.get('q')
    if search:
        post = post.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    paginator = Paginator(post, 12)  # Show 25 contacts per page

    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    context = {
        "post": total_article
    }
    return render(request, "index.html", context)


def getauthor(request, name):
    post_author = get_object_or_404(User, username=name)
    auth = get_object_or_404(author, name=post_author.id)
    post = article.objects.filter(article_author=auth.id)
    context = {
        "auth": auth,
        "post": post
    }
    return render(request, "profile.html", context)


def getsingle(request, id):
    post = get_object_or_404(article, pk=id)
    first = article.objects.first()
    last = article.objects.last()
    related = article.objects.filter(category=post.category).exclude(id=id)[:4]
    context = {
        "post": post,
        "first": first,
        "last": last,
        "related": related
    }
    return render(request, "single.html", context)


def getTopic(request, name):
    cat = get_object_or_404(category, name=name)
    post = article.objects.filter(category=cat.id)
    paginator = Paginator(post, 4)  # Show 25 contacts per page

    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    return render(request, "category.html", {"post": total_article, "cat": cat})


def getLogin(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            user = request.POST.get('user')
            password = request.POST.get('pass')
            auth = authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                return redirect('index')
            else:
                messages.add_message(request, messages.ERROR, 'Username or password mismatch')
                return render(request, "login.html")
    return render(request, "login.html")


def getlogout(request):
    logout(request)
    return redirect('index')


def getcreate(request):
    if request.user.is_authenticated:
        u = get_object_or_404(author, name=request.user.id)
        form = createForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = u
            instance.save()
            return redirect('index')
        return render(request, 'create.html', {"form": form})
    else:
        return redirect('login')







def getProfile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        author_profile = author.objects.filter(name=user.id)
        if author_profile:
            authorUser = get_object_or_404(author, name=request.user.id)
            post = article.objects.filter(article_author=authorUser.id)
            return render(request, 'logged_in_profile.html', {"post": post, "user": authorUser})
        else:
            form = createAuthor(request.POST or None, request.FILES or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.name = user
                instance.save()
                messages.success(request, 'Author profile is created successfully')
                return redirect('profile')
            return render(request, 'createauthor.html', {"form": form})

    else:
        return redirect('login')


def getRegister(request):
    form = registerUser(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Registration successfully completed')
        return redirect('login')
    return render(request, 'register.html', {"form": form})
