from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from grabsite import views
from grabsite.views import WeekDayChartJSONView, TimeChartJSONView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('charts/', TemplateView.as_view(template_name='charts.html'), name='charts'),
    path('weekday_chart_json/', WeekDayChartJSONView.as_view(), name='weekday_chart_json'),
    path('time_chart_json/', TimeChartJSONView.as_view(), name='time_chart_json'),
    path('', views.index, name='index'),
]
