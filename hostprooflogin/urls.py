from django.conf.urls import patterns, url

from hostprooflogin import views

urlpatterns = patterns('hostprooflogin.views',
    url('^register/$', view='register', name='hostprooflogin_register'),
)
