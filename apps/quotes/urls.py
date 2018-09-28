from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^signin$', views.signin),
    url(r'^quotes$', views.quotes),
    url(r'^add_new_quotes$', views.add_new_quotes),
    url(r'^add_likes/(?P<id>\d+)$', views.add_likes),
    url(r'^remove/(?P<id>\d+)$', views.remove_quote),
    url(r'^user/(?P<id>\d+)$', views.user_id),
    url(r'^myaccount/(?P<id>\d+)$', views.myaccount_id),
    url(r'^logout$', views.logout),
    url(r'^edit$', views.edit),
]