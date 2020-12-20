from django.urls import path
from . import views

urlpatterns = [
	path('save_info', views.save_info, name='save_info'),  
	path('save_portfolio', views.save_portfolio, name='save_portfolio'),  
	path('save_experience', views.save_experience, name='save_experience'),  
	path('save_education', views.save_education, name='save_education'),  
	path('show_profile', views.show_profile, name='show_profile'),  

]
