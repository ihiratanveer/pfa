from django.urls import path
from . import views

urlpatterns = [
    path('view_project_employer/<int:project_id>', views.view_project_employer, name='view_project_employer'),  
    path('save_project', views.save_project, name='save_project'), 
    path('view_project_freelancer/<int:project_id>', views.view_project_freelancer, name='view_project_freelancer'),  
    path('place_bid/<int:project_id>', views.place_bid, name='place_bid'),  
    path('assign_project', views.assign_project, name='assign_project'),  
    path('done_project/<int:project_id>', views.done_project, name='done_project'),  
    

    path('view_wip_project_employer/<int:project_id>', views.view_wip_project_employer, name='view_wip_project_employer'),  
    path('view_wip_project_freelancer/<int:project_id>', views.view_wip_project_freelancer, name='view_wip_project_freelancer'),  
    path('view_completed_project/<int:project_id>', views.view_completed_project, name='view_completed_project'),  

   

    path('delete_project/<int:project_id>', views.delete_project, name='delete_project'),  
    path('delete_ongoing_project/<int:project_id>', views.delete_ongoing_project, name='delete_ongoing_project'),  
    path('delete_completed_project/<int:project_id>', views.delete_completed_project, name='delete_completed_project'),  
    path('delete_bid/<int:project_id>', views.delete_bid, name='delete_bid'),  

]
