from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Block
from .scripts.url_generator import generate_url
from .forms import BlockForm
from datetime import timedelta, datetime
from django.utils import timezone


def index(request):

    blocks = []

    if request.user.is_authenticated:
        user_blocks = Block.objects.filter(user=request.user)
        blocks = user_blocks
        for b in user_blocks:
            lifetime = b.created + timedelta(minutes=int(b.delete_after))
            now = timezone.now()
            if now >= lifetime:
                b.delete()

    context = {
        'title': 'Home Page',
        'blocks': blocks,
    }

    return render(request, 'base/base.html', context)


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
    return render(request, 'base/create_block.html', context)
