from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class user_type(models.Model):
	"""Database model for users in the system"""
	
	user_id=models.IntegerField(blank=True)
	user_value= models.CharField(max_length=255)
	def __str__(self):
		return self.user_value




class freelancer(models.Model):
	"""Database model for users in the system"""
	
	user=models.OneToOneField(User,on_delete = models.CASCADE,related_name="freelancer")
	user_value = models.CharField(max_length=255)
	def __str__(self):
		return self.user_value
	freelancer_created_at = models.DateTimeField(auto_now_add=True)




class employer(models.Model):
	"""Database model for users in the system"""
	
	user=models.OneToOneField(User,on_delete = models.CASCADE,related_name="employer")
	user_value = models.CharField(max_length=255)
	def __str__(self):
		return self.user_value
	employer_created_at = models.DateTimeField(auto_now_add=True)
