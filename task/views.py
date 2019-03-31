from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from.models import *
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from usercreation.models import Teamcreation
# Create your views here.
def taskcreation(request):
	if request.method=='POST':
		form=task_info(request.POST)
		if form.is_valid():
			instance=form.save(commit=False)
			instance.taskuser=request.user
			instance.taskleader=True
			instance.save()
			messages.success(request,'You have created a new task')
			#messages.success(request,'Congratulations, you have created your Restaurant on Order-Eat')
			return redirect('usercreation:nextpage')
	else:
		form=task_info()
	return render(request,'task/taskcreation.html',{'form':form})


def taskupdate(request,taskslug):
	instance=get_object_or_404(Taskcreation,taskslug=taskslug)
	form=task_info(request.POST or None,request.FILES or None,instance=instance)
	b=request.user
	ob1=Taskcreation.objects.filter(taskuser=b)
	#ob=Taskcreation.objects.get(taskslug=taskslug)
	if len(ob1)!=0:
		if form.is_valid():
			instance=form.save(commit=False)
			instance.owner=request.user
			instance.save()
			messages.success(request,'Task details have beeen successfully updated')
			return redirect('usercreation:nextpage')
		context={
		      "instance":instance,
		      "form":form
		}
		return render(request,'task/taskupdate.html',context)
	else:
		messages.error(request,'Dont have rights to edit the task')
		return redirect('usercreation:nextpage')

def taskview(request,taskslug1):
	a=Taskcreation.objects.get(taskslug=taskslug1)
	b=a.taskteamname
	c=a.taskuser
	d=request.user
	f=Teamcreation.objects.filter(teamuser=c)
	e=Teamcreation.objects.filter(teamuser=d)
	if len(e)==0:
		messages.error(request,'Dont have rights to view the task')
		return redirect('usercreation:nextpage')
	else:
		#e=Teamcreation.objects.get(teamuser=d)
		if e[0].teamslug==f[0].teamslug:
			
			return render(request,'task/view.html',{'a':a})
		else:
			messages.error(request,'Dont have rights to view the task')
			return redirect('usercreation:nextpage')


	
def taskcomment(request,taskslug2):
	a=Taskcreation.objects.get(taskslug=taskslug2)
	b=a.taskteamname
	c=a.taskuser
	d=request.user
	f=Teamcreation.objects.filter(teamuser=c)
	e=Teamcreation.objects.filter(teamuser=d)
	if len(e)==0:
		messages.error(request,'Dont have rights to view the comments')
		return redirect('usercreation:nextpage')
	else:
		#e=Teamcreation.objects.get(teamuser=d)
		ob3=Comment.objects.all()
		if e[0].teamslug==f[0].teamslug:
			if request.method=='POST':
				form=comment_info(request.POST)
				if form.is_valid():
					instance=form.save(commit=False)
					instance.commentuser=request.user
					instance.commentteamname=a
					instance.save()
					form=comment_info(request.POST)
					#messages.success(request,'Congratulations, you have created your Restaurant on Order-Eat')
					return render(request,'task/taskcomment.html',{'a':a,'ob3':ob3,'form':form})
			else:
				form=comment_info()
			return render(request,'task/taskcomment.html',{'a':a,'form':form,'ob3':ob3})
		else:
			messages.error(request,'Dont have rights to view the comments')
			return redirect('usercreation:nextpage')
