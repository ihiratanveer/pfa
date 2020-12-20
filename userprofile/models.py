from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User



class intro(models.Model):
	"""Database model for users in the system"""
	
	user=models.ForeignKey(User,on_delete = models.CASCADE)
	user_title = models.CharField(max_length=255)

	user_intro = models.CharField(max_length=255)
	def __str__(self):
		return self.user_title

class portfolio(models.Model):
	"""Database model for users in the system"""
	
	user=models.ForeignKey(User,on_delete = models.CASCADE)
	portfolio_file=models.FileField(upload_to='media/portfolio/%Y/%m/%d/', max_length=254, blank=True)
	def __str__(self):
		return self.user.username

class experience(models.Model):
	"""Database model for users in the system"""
	
	user=models.ForeignKey(User,on_delete = models.CASCADE)
	company_name = models.CharField(max_length=255)
	company_designation = models.CharField(max_length=255)
	company_start_date = models.DateField(auto_now=False, auto_now_add=False)
	company_end_date = models.DateField(auto_now=False, auto_now_add=False)
	def __str__(self):
		return self.user.username

class education(models.Model):
	user=models.ForeignKey(User,on_delete = models.CASCADE)
	institute_name = models.CharField(max_length=255)
	degree_name = models.CharField(max_length=255)
	degree_start_date = models.DateField(auto_now=False, auto_now_add=False)
	degree_end_date = models.DateField(auto_now=False, auto_now_add=False)
	def __str__(self):
		return self.user.username