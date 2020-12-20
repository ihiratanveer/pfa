from django.contrib import admin

# Register your models here.
from .models import project,bids,ongoing_projects,completed_projects,posted_projects
admin.site.register(project)
admin.site.register(bids)
admin.site.register(ongoing_projects)
admin.site.register(completed_projects)
admin.site.register(posted_projects)
