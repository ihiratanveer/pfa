from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User # this table already exists in django we import it 
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .models import intro, portfolio, experience, education





def save_info(request):
	user=User.objects.get(id=request.user.id)
	context={'data':user}
	if request.method=='POST':
		#user_id = request.POST['fname']
		user_title=request.POST['title'] #request.post[id of the input field]
		user_intro = request.POST['introduction']
		user_id=request.user.id
		print('POSSSSSSSSSSSSTEEEEEEEEEDDDDDDDDDDDD')
		if user_id == '':
			 messages.warning(request, 'Kindly sign in to save profile')
			 return redirect('save_info')
		try:
			intro_data=intro.objects.get(user_id=user_id)
			intro.objects.filter(user_id=user_id).update(user_title=user_title,user_intro=user_intro)
			messages.success(request, 'Profile updated Successfully!')

		except:
			intro_data=intro.objects.create(user_id=user_id,user_title=user_title,user_intro=user_intro) 
			intro_data.save()
			messages.success(request, 'Profile created Successfully!')
	
		return redirect('save_info')
	return render(request,'profile/add_user_info_form.html',context)


def save_portfolio(request):
	user=User.objects.get(id=request.user.id)
	context={'data':user}

	if request.method=='POST':
		#user_id = request.POST['fname']
		user_portfolio=request.POST['proj_portfolio_item'] #request.post[id of the input field]
		user_id=request.user.id
		if user_id == '':
			 messages.warning(request, 'Kindly sign in to save profile')
			 return redirect('save_info')

		portfolio_data=portfolio.objects.create(user_id=user_id,portfolio_file=user_portfolio) 
		portfolio_data.save()
		messages.success(request, 'Portfolio added Successfully!')
		return redirect('save_portfolio')
	return render(request,'profile/add_user_info_form.html',context)


def save_experience(request):
	user=User.objects.get(id=request.user.id)
	context={'data':user}

	if request.method=='POST':
		#user_id = request.POST['fname']
		company_name=request.POST['company_name'] #request.post[id of the input field]
		designation=request.POST['designation'] #request.post[id of the input field]
		from_date=request.POST['from_date'] #request.post[id of the input field]
		to_date=request.POST['to_date'] #request.post[id of the input field]
		user_id=request.user.id
		if user_id == '':
			 messages.warning(request, 'Kindly sign in to save profile')
			 return redirect('save_info')

		experience_data=experience.objects.create(user_id=user_id,company_name=company_name,company_designation=designation,company_start_date=from_date,company_end_date=to_date )
		experience_data.save()
		messages.success(request, 'Experience added Successfully!')
		return redirect('save_experience')
	return render(request,'profile/add_user_info_form.html',context)



def save_education(request):
	user=User.objects.get(id=request.user.id)
	context={'data':user}

	if request.method=='POST':
		#user_id = request.POST['fname']
		institute=request.POST['institute'] #request.post[id of the input field]
		degreen=request.POST['degreen'] #request.post[id of the input field]
		from_date=request.POST['from_date'] #request.post[id of the input field]
		to_date=request.POST['to_date'] #request.post[id of the input field]

		user_id=request.user.id
		if user_id == '':
			 messages.warning(request, 'Kindly sign in to save profile')
			 return redirect('save_info')

		education_data=education.objects.create(user_id=user_id,institute_name=institute,degree_name=degreen,degree_start_date=from_date,degree_end_date=to_date) 
		education_data.save()
		messages.success(request, 'Education added Successfully!')
		return redirect('save_education')
	return render(request,'profile/add_user_info_form.html',context)



def show_profile(request):
	user_id=request.user.id
	user=User.objects.get(id=request.user.id)
	intros=intro.objects.filter(user_id=user_id)[0]
	port=portfolio.objects.filter(user_id=user_id)
	exp=experience.objects.filter(user_id=user_id)
	edu=education.objects.filter(user_id=user_id)
	data={'edu':edu,'user':user,'intro':intros,'exp':exp,'port':port,'first_email':user.username.split("@")[0],'data':user}
	print(data)
	return render(request,'profile/profile.html',data)
