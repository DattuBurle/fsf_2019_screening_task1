from django.conf.urls import url
from django.urls import path,include
from .import views
from .views import *
app_name='task'
urlpatterns = [
    path('taskcreation/',views.taskcreation,name='taskcreation'),
    url(r'^taskupdate/(?P<taskslug>[\w-]+)/$',views.taskupdate,name='taskupdate'),
    url(r'^taskview/(?P<taskslug1>[\w-]+)/$',views.taskview,name='taskview'),
    url(r'^taskcomment/(?P<taskslug2>[\w-]+)/$',views.taskcomment,name='taskcomment'),
  
    
]