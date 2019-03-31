from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save
from django.utils.text import slugify
from usercreation.models import Teamcreation

class Taskcreation(models.Model):
	taskname=models.CharField(max_length=20,blank=False)
	taskleader=models.BooleanField(default=False)
	taskuser=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='taskuser')
	taskteamname=models.ForeignKey(Teamcreation,on_delete=models.SET_NULL,null=True,related_name='teamtaskname')
	taskslug=models.SlugField(blank=True)
	taskdescription=models.TextField(blank=True)
	taskassignee=models.CharField(blank=True,max_length=255)
	taskstatus=models.CharField(default=None,max_length=40)

	def __str__(self):
		return self.taskteamname

def create_taskslug(instance,new_slug=None):
	taskslug=slugify(instance.taskname)
	if new_slug is not None:
		taskslug=new_slug
	queryset=Taskcreation.objects.filter(taskslug=taskslug).order_by('id')
	exists=queryset.exists()
	if exists:
		new_slug='%s-%s' %(taskslug,queryset.first().id)
		return create_taskslug(instance,new_slug=new_slug)
	return taskslug


def pre_save_taskdetails_receiver(sender,instance,*args,**kwargs):
	if not instance.taskslug:
		instance.taskslug=create_taskslug(instance)

pre_save.connect(pre_save_taskdetails_receiver,sender=Taskcreation)


class Comment(models.Model):
	commentuser=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='commentuser')
	commentteamname=models.ForeignKey(Taskcreation,on_delete=models.SET_NULL,null=True,related_name='commentteamname')
	comment_text=models.TextField(blank=True)

