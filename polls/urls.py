from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Main urls
    url(r'^$', 'poll.views.index'),
    url(r'^poll/(?P<id>[0-9]+)/$', 'poll.views.show'),
    url(r'^poll/vote/(?P<id>[0-9]+)/$', 'poll.views.vote'),
    url(r'^poll/comment/(?P<id>[0-9]+)/$', 'poll.views.comment'),
    url(r'^poll/new/$', 'poll.views.new_poll'),
    url(r'^poll/delete/(?P<id>[0-9]+)/$', 'poll.views.delete'),

    # User auth routes
    url(r'^auth/$', 'poll.views._login'),
    url(r'^reg/$', 'poll.views._register'),
    url(r'^logout/$', 'poll.views._logout'),

    url(r'^profile/(?P<username>[a-zA-Z0-9]+)/$', 'poll.views.profile'),

    # Captcha
    url(r'^captcha/$', 'poll.views.generate_captcha'),

    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
