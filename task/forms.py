from django import forms
from .models import Taskcreation,Comment


class task_info(forms.ModelForm):
	class Meta:
		model=Taskcreation
		fields=['taskname','taskdescription','taskassignee','taskstatus','taskteamname']

class comment_info(forms.ModelForm):
	class Meta:
		model=Comment
		fields=['comment_text']