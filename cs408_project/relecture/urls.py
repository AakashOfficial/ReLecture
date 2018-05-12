from django.conf.urls import url
from . import views
from django.views.generic import RedirectView


urlpatterns = [
    url(r'^$', views.test, name='test'),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),
    url(r'^post_list/$', views.post_list, name='post_list'),
    url(r'^post_list/post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post_list/post/new/$', views.post_new, name='post_new'),
    url(r'^post_list/post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post_list/post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^file_upload/$', views.upload_file, name='file_upload'),
    url(r'^pdf_upload/$', views.pdf_upload, name='pdf_upload'),
    url(r'^pdf_view/$', views.pdf_view, name='pdf_view'),
]