import django_filters
from projects.models import project


class Employer_Poster_Project_Filter(django_filters.FilterSet):
	class Meta:
		model=project
		fields=['project_name']