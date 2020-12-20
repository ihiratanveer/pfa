from django.contrib import admin

# Register your models here.
from user_roles import models 
admin.site.register(models.user_type)
admin.site.register(models.freelancer)
admin.site.register(models.employer)