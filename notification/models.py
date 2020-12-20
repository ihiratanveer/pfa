from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
	bid_item=models.ForeignKey('projects.bids', on_delete=models.CASCADE)
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_from_user")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_to_user")
	text_preview = models.CharField(max_length=90, blank=True, default='has bidded on the project')
	date = models.DateTimeField(auto_now_add=True)
	is_seen = models.BooleanField(default=False)