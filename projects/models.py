from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from notification.models import Notification
from user_roles.models import employer,freelancer
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver



class project(models.Model):
	"""Database model for users in the system"""
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	employer=models.ForeignKey(employer, on_delete=models.CASCADE)

	project_name=models.CharField(max_length=255)
	project_details=models.CharField(max_length=255)
	project_tags=models.CharField(max_length=255,default='', blank=True)
	project_created_at = models.DateTimeField(auto_now_add=True)

	project_payment=models.IntegerField()

	project_deadline=models.DateField(auto_now=False, auto_now_add=False)

	project_file=models.FileField(upload_to='media/project/%Y/%m/%d/', max_length=254, blank=True)
	project_iscompleted=models.BooleanField(default=False) 
	project_isongoing=models.BooleanField(default=False) 
	project_isassigned=models.BooleanField(default=False) 
	def __str__(self):
		return self.project_name

#split the tags on comma seperated
	def project_tags_as_list(self):
		return self.project_tags.split(',')




class bids(models.Model):
	"""Database model for users in the system"""
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	freelancer=models.ForeignKey(freelancer, on_delete=models.CASCADE)
	project=models.ForeignKey(project, on_delete=models.CASCADE)
	bid_payment=models.IntegerField()
	bid_estimated_days=models.IntegerField()
	bid_description=models.CharField(max_length=255,default='')
	bid_created_at = models.DateTimeField(auto_now_add=True)
    
	def notify_user_bid(sender, instance, *args, **kwargs):
		bid = instance
		sender = bid.user
		user=bid.project.user
		Notification.objects.create(sender=sender, user=user,bid_item=bid)
		print("called")

class ongoing_projects(models.Model):
	"""Database model for users in the system"""
	project=models.ForeignKey(project, on_delete=models.CASCADE)
	employer=models.ForeignKey(employer, on_delete=models.CASCADE)
	freelancer=models.ForeignKey(freelancer, on_delete=models.CASCADE)
	isCompleted=models.BooleanField(default=False) 
	project_ongoing_at=models.DateTimeField(auto_now_add=True)


class completed_projects(models.Model):
	project=models.ForeignKey(project, on_delete=models.CASCADE)
	employer=models.ForeignKey(employer, on_delete=models.CASCADE)
	freelancer=models.ForeignKey(freelancer, on_delete=models.CASCADE)
	isCompleted=models.BooleanField(default=True) 
	project_completed_at = models.DateTimeField(auto_now_add=True)



class posted_projects(models.Model):
	"""Database model for users in the system"""
	project=models.ForeignKey(project, on_delete=models.CASCADE)
	employer=models.ForeignKey(employer, on_delete=models.CASCADE)
	project_posted_at = models.DateTimeField(auto_now_add=True)




post_save.connect(bids.notify_user_bid, sender=bids)
