from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.test, name='test'),
    url(r'^post_list/$', views.post_list, name='post_list'),
    url(r'^post_list/post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post_list/post/new/$', views.post_new, name='post_new'),
    url(r'^post_list/post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post_list/post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^file_upload/$', views.upload_file, name='file_upload'),
]