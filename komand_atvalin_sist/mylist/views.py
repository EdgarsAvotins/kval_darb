from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from .models import Ieraksts


def index(request):
    if request.method== 'GET':

        online_user = request.user
        ieraksti_saraksts = Ieraksts.objects.filter(lietotajs=online_user).order_by('datums_no')

        paginator = Paginator(ieraksti_saraksts, 3)  # Show 25 contacts per page

        page = request.GET.get('page')
        try:
            ieraksti = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            ieraksti = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            ieraksti = paginator.page(paginator.num_pages)

        atvalinajumu_ieraksti=Ieraksts.objects.filter(lietotajs=online_user, merkis='atvalinajums').order_by('datums_no')
        komandejumu_ieraksti = Ieraksts.objects.filter(lietotajs=online_user, merkis='komandejums').order_by('datums_no')
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