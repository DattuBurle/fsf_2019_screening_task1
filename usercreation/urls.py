from django.conf.urls import url
from django.urls import path,include
from .import views
from .views import *
app_name='usercreation'
urlpatterns = [
   path('',views.homepage,name='homepage'),
   path('signup/',views.signup_view,name='signup'),
   url(r'^addddduser/(?P<usr>[\w-]+)/$',views.adduser,name='add'),
   url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),

   path('login/',views.login_view,name='login'),
   path('logout/',views.logout_view,name='logout'),
   path('nextpage/',views.nextpage,name='nextpage'),

   path('teamcreation/',views.teamcreation,name='teamcreation'),
   path('search/',views.searchuser,name='searchuser'),
   
  
    
]