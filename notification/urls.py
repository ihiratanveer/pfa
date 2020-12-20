from django.urls import path
from . import views

urlpatterns = [
    path('show_notify', views.show_notify, name='show_notify'),  

]
