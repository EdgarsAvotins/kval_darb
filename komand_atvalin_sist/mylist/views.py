from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Ieraksts


def index(request):
    if request.method== 'GET':

        online_user = request.user
        ieraksti = Ieraksts.objects.filter(lietotajs=online_user)
        atvalinajumu_ieraksti=Ieraksts.objects.filter(lietotajs=online_user, merkis='atvalinajums')
        komandejumu_ieraksti = Ieraksts.objects.filter(lietotajs=online_user, merkis='komandejums')
        context = {
            'ieraksti' : ieraksti,
            'atvalinajumu_ieraksti': atvalinajumu_ieraksti,
            'komandejumu_ieraksti': komandejumu_ieraksti,

        }
        return render(request, 'mylist/index.html', context)

    if request.method=='POST':
        dati=request.POST.get("dati")
        online_user = request.user
        all_users = User.objects.all()
        context = {
            'online_user': online_user,
            'all_users': all_users,
            'dati': dati,
        }
        return render(request, 'mylist/index.html', context)


def add(request):
    return HttpResponse("<h2>Pievieno jaunu ierakstu</h2>")
