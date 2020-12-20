from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib import messages,auth
from .models import user_type, freelancer, employer
from django.db.models import Q
import json
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from projects.models import ongoing_projects,completed_projects,project,bids,posted_projects

#----------------------------------------------------------Intiall setup as employer or freelancer-------------------------------------------------
def select_type(request):
	if request.method == 'POST':
		# Note change below
		if 'freelancer' in request.POST:
			freelancer_val = request.POST['freelancer']  # You can use else in here too if there is only 2 submit types.
			try:
				user_data=freelancer.objects.get(user_id=request.user.id)
				return redirect('freelancer_dashboard')

			except freelancer.DoesNotExist:
				create_user=freelancer(user_value=freelancer_val, user_id=request.user.id)
				create_user.save()
				return redirect('freelancer_dashboard')

		# Note change below
		elif 'employer' in request.POST:
			employer_val = request.POST['employer']  # You can use else in here too if there is only 2 submit types.
			try:
				user_data=employer.objects.get(user_id=request.user.id)
				return redirect('employer_dashboard')


			except employer.DoesNotExist:
				create_user=employer(user_value=employer_val, user_id=request.user.id)
				create_user.save()
				return redirect('employer_dashboard')

	#default url
		elif "post_project" in request.POST:
			return redirect('/post_project')

	
	else:
		return render(request,'signupas.html')


#-------------------------------------------------DASHBOARDS-------------------------------------------------------------------------
def freelancer_dashboard(request):
		#find contact of user who is currently logged in
	user=User.objects.filter(id=request.user.id)[0]
	
	freelancer_id=freelancer.objects.get(user_id=request.user.id).id
	
	projects=project.objects.all().exclude(user_id =request.user.id)
	projects=projects.exclude(project_iscompleted=True)
	projects=projects.exclude(project_isongoing=True)
	paginator = Paginator(projects, 4)
	page = request.GET.get('page')
	projects = paginator.get_page(page)
	

	ongoing_projects_data=ongoing_projects.objects.filter(freelancer_id=freelancer_id)
	paginator = Paginator(ongoing_projects_data, 3)
	page = request.GET.get('page')
	ongoing_projects_data = paginator.get_page(page)
	
	completed_projects_data=completed_projects.objects.filter(freelancer_id=freelancer_id)	
	paginator = Paginator(completed_projects_data, 3)
	page = request.GET.get('page')
	completed_projects_data = paginator.get_page(page)

	bid_data=bids.objects.filter(freelancer_id=freelancer_id)
	#print(bid_data.values())
	paginator = Paginator(bid_data, 3)
	page = request.GET.get('page')
	bid_data = paginator.get_page(page)

	data={"data":user,"projects":projects,"ongoing_projects":ongoing_projects_data,"completed_projects":completed_projects_data,"bids":bid_data}

	return render(request,'freelancer_dashboard.html',data)




@csrf_exempt
def employer_dashboard(request):
			#find contact of user who is currently logged in
	user=User.objects.filter(id=request.user.id)[0]
	employer_id=employer.objects.get(user_id=request.user.id).id
	posted_project=posted_projects.objects.filter(employer_id=employer_id)
	paginator = Paginator(posted_project, 3)
	page = request.GET.get('page')
	try:
		posted_project = paginator.get_page(page)
	except PageNotAnInteger:
		posted_project = paginator.page(1)
	except EmptyPage:
		posted_project = paginator.page(paginator.num_pages)

	

	ongoing_projects_data=ongoing_projects.objects.filter(employer_id=employer_id)
	paginator = Paginator(ongoing_projects_data, 3)
	page = request.GET.get('page')
	try:
		ongoing_projects_data = paginator.get_page(page)
	except (PageNotAnInteger, EmptyPage):
		# If page is not an integer or out of range, deliver first page.
		ongoing_projects_data = paginator.page(1)

	

	completed_projects_data=completed_projects.objects.filter(employer_id=employer_id)
	paginator = Paginator(completed_projects_data, 3)
	page = request.GET.get('page')
	completed_projects_data = paginator.get_page(page)
	try:
		completed_projects_data = paginator.get_page(page)
	except (PageNotAnInteger, EmptyPage):
		# If page is not an integer or out of range, deliver first page.
		completed_projects_data = paginator.page(1)



	data={"data":user,"ongoing_projects":ongoing_projects_data,"completed_projects":completed_projects_data,"posted_project":posted_project}

	return render(request,'employer_dashboard.html',data)


def switch_dashboard(request):
	if request.method == 'POST':
		# Note change below
		if 'as_freelancer' in request.POST:
			print('FREELANCER EXISTS')
			as_freelancer = request.POST.get('as_freelancer')
			print(as_freelancer)

			try:
				user_data=freelancer.objects.get(user_id=request.user.id)
				return redirect('freelancer_dashboard')


			except freelancer.DoesNotExist:
				print(as_freelancer)
				create_user=freelancer(user_value='freelancer', user_id=request.user.id)
				create_user.save()
				return redirect('freelancer_dashboard')

		elif 'as_employer' in request.POST:

			as_employer = request.POST['as_employer']
			try:
				user_data=employer.objects.get(user_id=request.user.id)
				return redirect('employer_dashboard')


			except employer.DoesNotExist:
				create_user=employer(user_value='employer', user_id=request.user.id)
				create_user.save()
				return redirect('employer_dashboard')

		elif 'post_project' in request.POST:
			
			return redirect('post_project')
	



def post_project(request):
		user=User.objects.filter(id=request.user.id)[0]

		data={"data":user}

		return render(request,'post_project.html',data)






#-------------------------------------------------SEARCHHINGG FOR PROJECTS------------------------------------------------------------


#---------------------------FREELANCER SEARCH---------------------------------------------------------------------------------------------
def freelancer_search_project(request):
				user=User.objects.filter(id=request.user.id)[0]
				freelancer_id=freelancer.objects.get(user_id=request.user.id).id
				

				ongoing_projects_data=ongoing_projects.objects.filter(freelancer_id=freelancer_id)
				paginator = Paginator(ongoing_projects_data, 3)
				page = request.GET.get('page')
				ongoing_projects_data = paginator.get_page(page)
				

				completed_projects_data=completed_projects.objects.filter(freelancer_id=freelancer_id)	
				paginator = Paginator(completed_projects_data, 3)
				page = request.GET.get('page')
				completed_projects_data = paginator.get_page(page)


				bid_data=bids.objects.filter(freelancer_id=freelancer_id)
				paginator = Paginator(bid_data, 3)
				page = request.GET.get('page')
				bid_data = paginator.get_page(page)	

				projects_data_new=project.objects.all()
				projects_data_new=projects_data_new.exclude(user_id =request.user.id)
				projects_data_new=projects_data_new.exclude(project_iscompleted=True)
				projects_data_new=projects_data_new.exclude(project_isongoing=True)
				
				query_string = ''


				
				field_name=request.GET['select_field']
				if not field_name:
					field_name=''

				
				input_field=request.GET['browse_proj_search']
				if not input_field:
					input_field=''	
				
				query_string += '&select_field={0}'.format(field_name)
				query_string += '&browse_proj_search={0}'.format(input_field)

				
				if field_name=='name':
			  		projects_data_new = projects_data_new.filter(project_name__icontains= input_field) #filter applied on item to be send 

				if field_name== 'skills':
						projects_data_new=projects_data_new.filter(Q(project_tags__icontains= input_field))

				if field_name== 'budget':
						projects_data_new=projects_data_new.extra(order_by=('-project_payment',))

				if field_name== 'all':
						projects_data_new=projects_data_new.filter( Q(project_name__icontains= input_field) | Q(project_tags__iexact= input_field) | Q(project_payment__icontains= input_field))
					
				paginator = Paginator(projects_data_new, 3)
				page = request.GET.get('page')
				try:
					projects_data_new = paginator.get_page(page)
				except (PageNotAnInteger, EmptyPage):
					projects_data_new = paginator.page(1)

				data={"projects":projects_data_new,"data":user,"ongoing_projects":ongoing_projects_data,"completed_projects":completed_projects_data,"bids":bid_data,'query_string':query_string }
				return render(request,'freelancer_dashboard.html',data)



def is_valid_queryparam(param):
	return param != '' and param is not None




def project_search_freelancer(request):
	freelancer_id=employer.objects.get(user_id=request.user.id).id

	bid = bids.objects.filter(freelancer_id=freelancer_id)
	title_contains_query = request.GET.get('projsearch_mb')
	if is_valid_queryparam(title_contains_query):
		bid = bid.filter(project__project_name__icontains=title_contains_query)    

	paginator = Paginator(bid, 4)
	page = request.GET.get('page')
	bid = paginator.get_page(page)
	data={"bids":bid}
	return render(request,"freelancer_dashboard.html",data)






#---------------------------Employersss SEARCH---------------------------------------------------------------------------------------------

def employer_search_posted_project(request):
	user=User.objects.filter(id=request.user.id)[0]
	employer_id=employer.objects.get(user_id=request.user.id).id

	ongoing_projects_data=ongoing_projects.objects.filter(employer_id=employer_id)
	paginator = Paginator(ongoing_projects_data, 3)
	page = request.GET.get('page')
	try:
		ongoing_projects_data = paginator.get_page(page)
	except (PageNotAnInteger, EmptyPage):
		# If page is not an integer or out of range, deliver first page.
		ongoing_projects_data = paginator.page(1)

	

	completed_projects_data=completed_projects.objects.filter(employer_id=employer_id)
	paginator = Paginator(completed_projects_data, 3)
	page = request.GET.get('page')
	completed_projects_data = paginator.get_page(page)
	try:
		completed_projects_data = paginator.get_page(page)
	except (PageNotAnInteger, EmptyPage):
		# If page is not an integer or out of range, deliver first page.
		completed_projects_data = paginator.page(1)






	posted_project_data=posted_projects.objects.filter(employer_id=employer_id)
	name = request.GET.get('projsearch_mb')
	print(name)
	if not name:
		name=""
	
	
	posted_project_data = posted_project_data.filter(project__project_name__icontains=name)    
	print('filtering')
	
	query_string = ''
	query_string += '&projsearch_mb={0}'.format(name)

	paginator = Paginator(posted_project_data, 3)
	page = request.GET.get('page')
	posted_project_data = paginator.get_page(page)
	data={"data":user,"ongoing_projects":ongoing_projects_data,"completed_projects":completed_projects_data,"posted_project":posted_project_data,'query_string':query_string}
	return render(request,"employer_dashboard.html",data)






def employer_search_ongoing_project(request):
	user=User.objects.filter(id=request.user.id)[0]
	employer_id=employer.objects.get(user_id=request.user.id).id
	
	posted_project=posted_projects.objects.filter(employer_id=employer_id)
	paginator = Paginator(posted_project, 3)
	page = request.GET.get('page')
	try:
		posted_project = paginator.get_page(page)
	except PageNotAnInteger:
		posted_project = paginator.page(1)
	except EmptyPage:
		posted_project = paginator.page(paginator.num_pages)


	completed_projects_data=completed_projects.objects.filter(employer_id=employer_id)
	paginator = Paginator(completed_projects_data, 3)
	page = request.GET.get('page')
	completed_projects_data = paginator.get_page(page)
	try:
		completed_projects_data = paginator.get_page(page)
	except (PageNotAnInteger, EmptyPage):
		# If page is not an integer or out of range, deliver first page.
		completed_projects_data = paginator.page(1)

	
	ongoing_projects_data=ongoing_projects.objects.filter(employer_id=employer_id)
	name = request.GET.get('projsearch_wip')
	print(name)
	if not name:
		name=""
	ongoing_projects_data = ongoing_projects_data.filter(project__project_name__icontains=name)   
	
	query_string = ''
	query_string += '&projsearch_wip={0}'.format(name)	




	paginator = Paginator(ongoing_projects_data, 3)
	page = request.GET.get('page')
	ongoing_projects_data = paginator.get_page(page)
	
	data={"data":user,"ongoing_projects":ongoing_projects_data,"completed_projects":completed_projects_data,"posted_project":posted_project,'query_string':query_string}
	return render(request,"employer_dashboard.html",data)




def employer_search_completed_project(request):
	user=User.objects.filter(id=request.user.id)[0]
	employer_id=employer.objects.get(user_id=request.user.id).id
	
	posted_project=posted_projects.objects.filter(employer_id=employer_id)
	paginator = Paginator(posted_project, 3)
	page = request.GET.get('page')
	try:
		posted_project = paginator.get_page(page)
	except PageNotAnInteger:
		posted_project = paginator.page(1)
	except EmptyPage:
		posted_project = paginator.page(paginator.num_pages)


	ongoing_projects_data=ongoing_projects.objects.filter(employer_id=employer_id)
	paginator = Paginator(ongoing_projects_data, 3)
	page = request.GET.get('page')
	ongoing_projects_data = paginator.get_page(page)



	completed_projects_data=completed_projects.objects.filter(employer_id=employer_id)
	name = request.GET.get('projsearch_cp')
	if not name:
		name=""

	completed_projects_data = completed_projects_data.filter(project__project_name__icontains=name)    
	query_string = ''
	query_string += '&projsearch_cp={0}'.format(name)	
	paginator = Paginator(completed_projects_data, 3)
	page = request.GET.get('page')
	completed_projects_data = paginator.get_page(page)
	try:
		completed_projects_data = paginator.get_page(page)
	except (PageNotAnInteger, EmptyPage):
		# If page is not an integer or out of range, deliver first page.
		completed_projects_data = paginator.page(1)

	
	data={"data":user,"ongoing_projects":ongoing_projects_data,"completed_projects":completed_projects_data,"posted_project":posted_project,'query_string':query_string}
	return render(request,"employer_dashboard.html",data)