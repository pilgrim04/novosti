from django.conf.urls import patterns, include, url

from django.contrib import admin
from apps.views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'novosti.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),


    url(r'^$',
        OurNews.as_view(),
        name='our_news'),
    url(r'^news/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<article>[A-Za-z0-9]+)',
        ArticleView.as_view(),
        name='article'),
    url(r'^news/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$',
        AllNewsView.as_view(),
        name='allnews')

)
