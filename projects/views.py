from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User # this table already exists in django we import it 
from django.contrib.auth import authenticate, login
from django.urls import reverse

from user_roles.models import user_type, freelancer, employer
from .models import project,bids,ongoing_projects,completed_projects,posted_projects
from django.db.models import Sum


# Create your views here.
def save_project(request):
	user=User.objects.get(id=request.user.id)
	data={'data':user}
	print(data)
	if request.method=='POST':
		#user_id = request.POST['fname']
		project_name=request.POST['project_name'] #request.post[id of the input field]
		project_details = request.POST['project_details']
		project_tags = request.POST["skills"]
		project_payment = request.POST['payment']
		project_deadline=request.POST.get('deadline')
		project_file=request.POST.get('proj_upload_file')
		user_id=request.user.id
		employer_id=employer.objects.get(user_id=request.user.id).id
		if user_id == '':
			 messages.warning(request, 'Kindly sign in as employer to Post Project!')
			 return redirect('save_project')

		if project_name == '':
			 messages.warning(request, 'Please enter Project name!')
			 return redirect('save_project')

		if project_details == '':
			 messages.warning(request, 'Please enter Project Details!')
			 return redirect('save_project')

		if project_tags == '':
			 messages.warning(request, 'Please enter Skills Required!')
			 return redirect('save_project')

		if project_payment == '':
			 messages.warning(request, 'Please enter Project Payment!')
			 return redirect('save_project')

		if project_deadline == '':
			 messages.warning(request, 'Please enter Project Deadline!')
			 return redirect('save_project')
		
		projects,created=project.objects.get_or_create(user_id=user_id,project_tags=project_tags,employer_id=employer_id,project_name=project_name,project_details=project_details,project_payment=project_payment,project_deadline=project_deadline,project_file=project_file) #these are postgres first_name,last_name
		projects.save()


		post_project=posted_projects.objects.create(employer_id=employer_id,project_id=projects.id) #these are postgres first_name,last_name
		post_project.save()	
		

		tags=project.objects.get(id=projects.id).project_tags
		context = {'inputs_list': tags.split(",")}
		print(context)

		messages.success(request,"Successfully Posted Project")
		return redirect('/select/post_project',data)

	return render(request,'post_project.html',data)



def view_project_freelancer(request,project_id):
		project_id=project_id
		print("idddd")
		user=User.objects.get(id=request.user.id)
		proj_data=project.objects.get(id=project_id)
		bid_data=bids.objects.filter(project_id=project_id)
		average_bid=bid_data.aggregate(Sum('bid_payment'))
		average_bid_int=0
		
		for x in average_bid.values():
			if x==None:
				average_bid_int=0
			else:
				average_bid_int=x//len(bid_data)


		data={"project":proj_data,'data':user,"bid_data":bid_data,"average_bid":average_bid_int}

		return render(request,'view_project_freelancer.html',data)


def place_bid(request,project_id):
		if request.method=='POST':

			bid_payment=request.POST.get('bid_amount')
			#print(bid_payment) #request.post[id of the input field]
			bid_estimated_days = request.POST.get('bid_days')
			bid_description = request.POST.get("proposal_details")
			user_id=request.user.id
			freelancer_id=freelancer.objects.get(user_id=request.user.id).id
			project_id=request.POST.get('project_id_val')
			#print('iiddddddd')
			#print(freelancer_id)
			if user_id == '':
				 messages.warning(request, 'Kindly sign in as employer to Post Project!')
				 return redirect('view_project_freelancer' , project_id=project_id)

			if bid_payment == '':
				 messages.warning(request, 'Please enter Bid amount!')
				 return redirect('view_project_freelancer' , project_id=project_id)

			if bid_estimated_days == '':
				 messages.warning(request, 'Please enter Estimated delievery days!')
				 return redirect('view_project_freelancer' , project_id=project_id)

			if bid_description == '':
				 messages.warning(request, 'Please enter Proposal Details!')
				 return redirect('view_project_freelancer' , project_id=project_id)

			try:
				bid=bids.objects.get(user_id=user_id,project_id=project_id,freelancer_id=freelancer_id)
				bids.objects.filter(user_id=user_id,project_id=project_id,freelancer_id=freelancer_id).update(bid_payment=bid_payment,bid_estimated_days=bid_estimated_days,bid_description=bid_description)
				messages.success(request, 'Bid updated Successfully!')

			except:
				bid=bids.objects.create(user_id=user_id,project_id=project_id,bid_payment=bid_payment,bid_estimated_days=bid_estimated_days,bid_description=bid_description,freelancer_id=freelancer_id) #these are postgres first_name,last_name
				bid.save()
				messages.success(request, 'Posted updated Successfully!')
			 
			return redirect('view_project_freelancer' , project_id=project_id)






def view_project_employer(request,project_id):
		project_id=project_id
		user=User.objects.get(id=request.user.id)
		employer_data=employer.objects.get(user_id=request.user.id)
		proj_data=project.objects.get(id=project_id)
		bid_data=bids.objects.filter(project_id=project_id)
		data={"project":proj_data,'employer_data':employer_data,"bid_data":bid_data,"data":user}
		return render(request,'view_project_employer.html',data)


def assign_project(request):
		if request.method=='POST':
			project_id=request.POST['project_id']
			freelancers_id=request.POST.get('get_freelancers_id', None)
			employer_id=request.POST['employer_id']
			ongoing_project, created=ongoing_projects.objects.get_or_create(freelancer_id=freelancers_id,employer_id=employer_id,project_id=project_id) #these are postgres first_name,last_name
			ongoing_project.save()	
			project.objects.filter(id=project_id).update(project_isongoing=True)
			project.objects.filter(id=project_id).update(project_isassigned=True)
			posted_projects.objects.filter(project_id=project_id).delete()
			bids.objects.filter(project_id=project_id).delete()

		return redirect('view_project_employer' , project_id=project_id)


def done_project(request,project_id):
		project_id=project_id
		ongoing_project=ongoing_projects.objects.get(project_id=project_id)
		employer_id=ongoing_project.employer_id
		freelancer_id=ongoing_project.freelancer_id
		completed_project, created=completed_projects.objects.get_or_create(freelancer_id=freelancer_id,employer_id=employer_id,project_id=project_id) #these are postgres first_name,last_name
		completed_project.save()
		project.objects.filter(id=project_id).update(project_iscompleted=True)
		ongoing_projects.objects.filter(project_id=project_id).delete()
		return redirect('employer_dashboard')




def view_wip_project_employer(request,project_id):
			project_id=project_id
			ongoing_project=ongoing_projects.objects.get(id=project_id)
			user=User.objects.get(id=request.user.id)
			data={"ongoing_project":ongoing_project,'data':user}
			return render(request,'view_wip_project_employer.html' , data)


def view_wip_project_freelancer(request,project_id):
			project_id=project_id
			ongoing_project=ongoing_projects.objects.get(id=project_id)
			user=User.objects.get(id=request.user.id)
			data={"ongoing_project":ongoing_project,'data':user}
			return render(request,'view_wip_project_freelancer.html' , data)



def view_completed_project(request,project_id):
			project_id=project_id
			completed_project=completed_projects.objects.get(id=project_id)
			user=User.objects.get(id=request.user.id)
			data={"completed_project":completed_project,'data':user}
			return render(request,'view_completed_project.html' , data)




def delete_project(request,project_id):
			project_id=project_id
			project.objects.filter(id=project_id).delete()
			return redirect('employer_dashboard')

def delete_ongoing_project(request,project_id):
			project_id=project_id
			ongoing_projects.objects.filter(project_id=project_id).delete()
			return redirect('employer_dashboard')

def delete_completed_project(request,project_id):
			project_id=project_id
			completed_projects.objects.filter(project_id=project_id).delete()
			return redirect('employer_dashboard')

def delete_bid(request,project_id):
			project_id=project_id
			bids.objects.filter(project_id=project_id).delete()
			return redirect('employer_dashboard')


