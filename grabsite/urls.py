from django.urls import path, include

from . import views

app_name = 'grabsite'

urlpatterns = [
    path('grabsite/<int:pk>/', views.UrlsDetailView.as_view(), name='detail'),
    path('grabsite/list/', views.UrlListView.as_view(), name='list'),
    path('grabsite/weekday_chart_json/<int:pk>/', views.WeekDayChartJSONView.as_view(), name='weekday_chart_json'),
    path('grabsite/time_chart_json/<int:pk>/', views.TimeChartJSONView.as_view(), name='time_chart_json'),
    path('register/', views.RegisterFormView.as_view(), 'signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
]
