from django.contrib import admin
from django.urls import path, include

import grabsite

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('grabsite.urls')),

]
