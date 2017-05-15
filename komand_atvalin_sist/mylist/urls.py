from django.conf.urls import url
from . import views

urlpatterns = [
    # /mylist/
    url(r'^$', views.index, name='index'),

    # /mylist/add
    url(r'^add$', views.add, name='index'),
]