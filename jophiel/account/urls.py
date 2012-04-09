from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url

urlpatterns = patterns("account",
    url(r'^$', 'views.show', name = 'account-show'),
    url(r'^logout/$', 'views.logout', name = 'account-logout'),
    url(r'^login/$', 'views.login', name = 'account-login'),
    url(r'^signup/$', 'views.signup',  name = 'account-signup'),
    url(r'^reset/$', 'views.send_reset_password_link',  name = 'account-send_reset_password_link'),
    url(r'^change_password/$', 'views.change_password', name = 'account-change_password'),
    url(r'^confirm/(?P<user_id>\d+)/(?P<secret>\w{32})/$', 'views.confirm',  name = 'account-confirm'),
    url(r'^confirm/(?P<user_id>\d+)/(?P<request_id>\d+)/(?P<secret>\w{32})/$', 'views.confirm',  name = 'account-confirm'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'views.password_reset_confirm',  name = 'account-password_reset_confirm'),
    url(r'^go/(?P<user_id>\d+)/(?P<secret>\w{32})(?P<url>/.*)$', 'views.go',  name = 'account-go'),

)
