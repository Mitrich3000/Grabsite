from django.shortcuts import render, redirect
from .forms import MyForm
from .tasks import mail_sent, parsing


def index(request, **kwargs):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            # launch asynchronous task
            parsing()
            # mail_sent()
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = MyForm()

    return render(request, 'index.html', {"form": form})
