from django.urls import path
from . import views

urlpatterns = [
    path('type', views.select_type, name='type'),
    path('freelancer_dashboard', views.freelancer_dashboard, name='freelancer_dashboard'), 
    path('employer_dashboard', views.employer_dashboard, name='employer_dashboard'), 
    path('switch_dashboard', views.switch_dashboard, name='switch_dashboard'), 
    path('post_project', views.post_project, name='post_project'), 

    path('freelancer_search_project', views.freelancer_search_project, name='freelancer_search_project'), 
    


    path('employer_search_posted_project', views.employer_search_posted_project, name='employer_search_posted_project'), 
    path('employer_search_ongoing_project', views.employer_search_ongoing_project, name='employer_search_ongoing_project'), 
    path('employer_search_completed_project', views.employer_search_completed_project, name='employer_search_completed_project'), 


]
