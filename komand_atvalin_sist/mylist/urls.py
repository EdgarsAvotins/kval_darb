from django.conf.urls import url
from . import views
app_name = 'mylist'

urlpatterns = [
    # /mylist/
    url(r'^$', views.index, name='index'),

    # /mylist/all
    url(r'^all$', views.all, name='all'),

    # logout
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),

    # login
    url(r'^login/$', views.LoginView.as_view(), name='login'),
]