from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Block
from .scripts.urlgenerator import generate_url
from .forms import BlockForm


def index(request):
    context = {'title': 'Home Page'}
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
