from django.conf.urls import patterns, include, url

from django.contrib import admin
from apps.views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'novosti.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', MyPageView.as_view(), name='page'),
    url(r'^our-news/$', OurNews.as_view(), name='our_news'),

)
