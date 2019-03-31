from django.contrib.auth import login, authenticate,logout
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .forms import *
from django.db.models import Q
from django.contrib import messages
from task.models import Taskcreation




def homepage(request):
	return render(request,'usercreation/homepage.html')

def signup_view(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		print(form)
		if form.is_valid():
			form.save()
			#username = form.cleaned_data.get('username')
			#raw_password = form.cleaned_data.get('password1')
			#user = authenticate(username=username, password=raw_password)
			#login(request, user)
			user = form.save(commit=False)
			user.is_active = True
			user.save()

			current_site = get_current_site(request)
			subject = 'Activate Your Account'
			message = render_to_string('usercreation/account_activation_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
				'token': account_activation_token.make_token(user),
			})
			to_email = form.cleaned_data.get('email')
			print(to_email)
			from_email = settings.EMAIL_HOST_USER
			to_list = [to_email,settings.EMAIL_HOST_USER]
			send_mail(
				subject, message, from_email,to_list,fail_silently=True
			)
			return redirect('usercreation:account_activation_sent')
	else:
		form = SignUpForm()
	return render(request, 'usercreation/signup.html', {'form': form})

def account_activation_sent(request):
	return render(request, 'usercreation/account_activation_sent.html')


def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		#user.profile.email_confirmed = True
		user.save()
		login(request, user)
		return redirect('usercreation:nextpage')
	else:
		return render(request, 'usercreation/account_activation_invalid.html')



def login_view(request):
	if request.method=='POST':
		form=AuthenticationForm(data=request.POST)
		if form.is_valid():
			user=form.get_user()
			#us=User.objects.all()
			login(request,user)
			if 'next' in request.POST:
				return redirect('usercreation:nextpage')
			else:
				return redirect('usercreation:nextpage')

	else:
		form = AuthenticationForm()

	return render(request,'usercreation/login.html',{'form':form})

def logout_view(request):
	logout(request)	
	return redirect('/') 


def nextpage(request):
	ob=Taskcreation.objects.all()

	return render(request,'usercreation/nextpage.html',{'ob':ob})

def teamcreation(request):
	if request.method=='POST':
		form=team_info(request.POST)
		if form.is_valid():
			instance=form.save(commit=False)
			instance.teamuser=request.user
			instance.save()
			#messages.success(request,'Congratulations, you have created your Restaurant on Order-Eat')
			return redirect('usercreation:nextpage')
	else:
		form=team_info()
	return render(request,'usercreation/teamcreation.html',{'form':form})


def searchuser(request):
	query=request.GET.get('q')
	ob1=User.objects.filter(
		Q(first_name=query)|
		Q(last_name=query))
	if not ob1:
		messages.error(request,'Sorry, the user is not available')

	return render(request,'usercreation/nextpage.html',{'ob1':ob1})

def adduser(request,usr):
	x=User.objects.get(username=usr)
	z=request.user
	y=Teamcreation.objects.filter(teamuser=z)
	if len(y)!=0:
		y=y[0]

		Teamcreation.objects.create(teamname=y.teamname,teamuser=x,teamslug=y.teamslug)
		return redirect('usercreation:nextpage')
	else:
		messages.error(request,'he must be added in the team by the task owner and then only he canbe added to view tasks ')
		return redirect('usercreation:nextpage')