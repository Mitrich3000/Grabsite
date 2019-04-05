from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'grabsite'

urlpatterns = [
    path('grabsite/<int:pk>/', views.UrlsDetailView.as_view(), name='detail'),
    path('grabsite/list/', views.UrlListView.as_view(), name='list'),
    path('grabsite/weekday_chart_json/', views.WeekDayChartJSONView.as_view(), name='weekday_chart_json'),
    path('grabsite/time_chart_json/', views.TimeChartJSONView.as_view(), name='time_chart_json'),
    path('', views.index, name='index'),
]
