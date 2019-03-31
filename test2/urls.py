from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from grabsite import views
from grabsite.views import WeekDayChartJSONView, TimeChartJSONView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('weekday_chart/', TemplateView.as_view(template_name='weekday.html'), name='weekday_chart'),
    path('weekday_chart_json/', WeekDayChartJSONView.as_view(), name='weekday_chart_json'),
    path('time_chart/', TemplateView.as_view(template_name='poptime.html'), name='time_chart'),
    path('time_chart_json/', TimeChartJSONView.as_view(), name='time_chart_json'),
    path('', views.index, name='index'),
]
