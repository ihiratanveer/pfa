from django.shortcuts import render

from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from .models import Notification
# Create your views here.
from projects.models import bids

def show_notify(request):
	user = request.user
	notifications = Notification.objects.filter(user=user).order_by('-date')
	Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)


	data = {'notifications': notifications, 'data':user}

	return render(request,'notification/notification.html',data)




