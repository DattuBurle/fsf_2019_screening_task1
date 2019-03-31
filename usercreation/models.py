from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save
from django.utils.text import slugify

class Teamcreation(models.Model):
	teamname=models.CharField(max_length=20,blank=False)
	teamleader=models.BooleanField(default=False)
	teamuser=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='teamuser')
	teamslug=models.SlugField(blank=True)

	def __str__(self):
		return self.teamname

def create_teamslug(instance,new_slug=None):
	teamslug=slugify(instance.teamname)
	if new_slug is not None:
		teamslug=new_slug
	queryset=Teamcreation.objects.filter(teamslug=teamslug).order_by('id')
	exists=queryset.exists()
	if exists:
		new_slug='%s-%s' %(teamslug,queryset.first().id)
		return create_teamslug(instance,new_slug=new_slug)
	return teamslug


def pre_save_teamdetails_receiver(sender,instance,*args,**kwargs):
	if not instance.teamslug:
		instance.teamslug=create_teamslug(instance)

pre_save.connect(pre_save_teamdetails_receiver,sender=Teamcreation)



