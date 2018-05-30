from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'login_success/$', views.login_success, name='login_success'),
    url(r'login_success_final/$', views.login_success_final, name='login_success_final'),
   
    
    
]