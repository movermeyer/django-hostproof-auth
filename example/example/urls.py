from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^auth/', include('hostproof_auth.urls')),
)
