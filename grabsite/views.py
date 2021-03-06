import json

from chartjs.views.lines import BaseLineChartView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, FormView

from grabsite.models import Urls
from .forms import MyForm
from .tasks import parsing


@login_required
def index(request, **kwargs):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            # launch asynchronous task
            # parsing.delay(url=form.cleaned_data['url'])
            parsing(user=request.user, url=form.cleaned_data['url'])

            return redirect('grabsite:list')
        else:
            print(form.errors)
    else:
        form = MyForm()

    return render(request, 'index.html', {"form": form})


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/"
    template_name = "registration/register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


class UrlsDetailView(LoginRequiredMixin, DetailView):
    model = Urls
    template_name = 'charts.html'


class UrlListView(LoginRequiredMixin, ListView):
    model = Urls
    template_name = 'list.html'

    def get_queryset(self):
        queryset = Urls.objects.all().order_by("-grabed")
        return queryset


class WeekDayChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

    def get_providers(self):
        """Return names of datasets."""
        return ["День недели"]

    def get_data(self):
        """Return datasets to plot."""

        data = json.loads(Urls.objects.get(pk=self.kwargs['pk']).weekday)

        return data

    def get_colors(self):
        yield (255, 0, 0)


class TimeChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        labels = [i for i in range(24)]
        return labels

    def get_providers(self):
        """Return names of datasets."""
        return ["Популярный час"]

    def get_data(self):
        """Return datasets to plot."""

        data = json.loads(Urls.objects.get(pk=self.kwargs['pk']).poptime)

        return data

    def get_colors(self):
        yield (255, 0, 132)


charts = TemplateView.as_view(template_name='charts.html')
weekday_chart_json = WeekDayChartJSONView.as_view()
time_chart_json = TimeChartJSONView.as_view()
