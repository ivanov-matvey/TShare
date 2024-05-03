from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Block
from .scripts.url_generator import generate_url
from .forms import BlockForm
from datetime import timedelta, datetime
from django.utils import timezone


def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect(home)

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('index')


def register_page(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "An error occurred during registration")

    context = {'form': form}
    return render(request, 'base/login_register.html', context)


def index(request):

    blocks = []

    if request.user.is_authenticated:
        user_blocks = Block.objects.filter(user=request.user)
        for b in user_blocks:
            lifetime = b.created + timedelta(minutes=int(b.delete_after))
            now = timezone.now()
            if now >= lifetime:
                b.delete()
        blocks = user_blocks

    context = {
        'title': 'Home Page',
        'blocks': blocks,
    }

    return render(request, 'base/base.html', context)


@login_required(login_url='login')
def create_block(request):
    form = BlockForm

    if request.method == 'POST':
        form = BlockForm(request.POST)
        if form.is_valid():
            block = form.save(commit=False)
            block.user = request.user
            block.url = generate_url()
            block.save()
            form.save()
            return redirect('index')

    context = {'form': form}
    return render(request, 'base/block_form.html', context)


@login_required(login_url='login')
def edit_block(request, url):
    block = Block.objects.get(url=url)
    form = BlockForm(instance=block)

    if request.user != block.user:
        return redirect('index')

    if request.method == 'POST':
        form = BlockForm(request.POST, instance=block)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {'form': form}
    return render(request, 'base/block_form.html', context)


@login_required(login_url='login')
def delete_block(request, url):
    block = Block.objects.get(url=url)

    if request.user != block.user:
        return redirect('index')

    if request.method == 'POST':
        block.delete()
        return redirect('index')

    context = {'obj': block}
    return render(request, 'base/delete.html', context)


def block(request, url):
    block = Block.objects.get(url=url)

    context = {'content': block}
    return render(request, 'base/block.html', context)
