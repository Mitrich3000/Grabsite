from chartjs.views.lines import BaseLineChartView
from django.db.models.aggregates import Count
from django.db.models.functions import ExtractWeekDay, ExtractHour
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from grabsite.models import Advertisement
from .forms import MyForm
from .tasks import parsing


def index(request, **kwargs):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            # launch asynchronous task
            parsing(url=form.cleaned_data['url'])

            return redirect('weekday_chart')
        else:
            print(form.errors)
    else:
        form = MyForm()

    return render(request, 'index.html', {"form": form})


class WeekDayChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

    def get_providers(self):
        """Return names of datasets."""
        return ["День недели"]

    def get_data(self):
        """Return datasets to plot."""

        qs = Advertisement.objects.annotate(weekday=ExtractWeekDay('posted')).values('weekday').annotate(
            count=Count('id')).values_list('weekday', 'count')
        data = {i: 0 for i in range(7)}
        data.update(qs)
        data = [[v for k, v in data.items()]]

        return data


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

        qs = Advertisement.objects.annotate(poptime=ExtractHour('posted')).values('poptime').annotate(
            count=Count('id')).values_list('poptime', 'count')
        data = {i: 0 for i in range(24)}
        data.update(qs)
        data = [[v for k, v in data.items()]]

        return data


weekday_chart = TemplateView.as_view(template_name='weekday.html')
weekday_chart_json = WeekDayChartJSONView.as_view()
time_chart = TemplateView.as_view(template_name='poptime.html')
time_chart_json = TimeChartJSONView.as_view()
