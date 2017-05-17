from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from .models import Ieraksts, Atvalinajums, Komandejums
import datetime



def index(request):
    if request.method== 'GET':

        online_user = request.user



        ieraksti_saraksts = Ieraksts.objects.filter(lietotajs=online_user).order_by('datums_no')

        paginator_kopejais = Paginator(ieraksti_saraksts, 10)  # Show 25 contacts per page

        table1 = request.GET.get('table1')
        try:
            ieraksti = paginator_kopejais.page(table1)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            ieraksti = paginator_kopejais.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            ieraksti = paginator_kopejais.page(paginator_kopejais.num_pages)




        atvalinajumu_ieraksti_saraksts = Ieraksts.objects.filter(lietotajs=online_user, merkis='atvalinajums').order_by('datums_no')

        paginator_atvalinajums = Paginator(atvalinajumu_ieraksti_saraksts, 5)  # Show 25 contacts per page

        table2 = request.GET.get('table2')
        try:
            atvalinajumu_ieraksti = paginator_atvalinajums.page(table2)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            atvalinajumu_ieraksti = paginator_atvalinajums.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            atvalinajumu_ieraksti = paginator_atvalinajums.page(paginator_atvalinajums.num_pages)




        komandejumu_ieraksti_saraksts = Ieraksts.objects.filter(lietotajs=online_user, merkis='komandejums').order_by('datums_no')

        paginator_komandejums = Paginator(komandejumu_ieraksti_saraksts, 5)  # Show 25 contacts per page

        table3 = request.GET.get('table3')
        try:
            komandejumu_ieraksti = paginator_komandejums.page(table3)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            komandejumu_ieraksti = paginator_komandejums.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            komandejumu_ieraksti = paginator_komandejums.page(paginator_komandejums.num_pages)

        context = {
            'ieraksti' : ieraksti,
            'atvalinajumu_ieraksti': atvalinajumu_ieraksti,
            'komandejumu_ieraksti': komandejumu_ieraksti,
        }
        return render(request, 'mylist/index.html', context)

    if request.method=='POST':

        online_user = request.user

        ieraksti_saraksts = Ieraksts.objects.filter(lietotajs=online_user).order_by('datums_no')

        paginator_kopejais = Paginator(ieraksti_saraksts, 10)  # Show 25 contacts per page

        table1 = request.GET.get('table1')
        try:
            ieraksti = paginator_kopejais.page(table1)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            ieraksti = paginator_kopejais.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            ieraksti = paginator_kopejais.page(paginator_kopejais.num_pages)




        atvalinajumu_ieraksti_saraksts = Ieraksts.objects.filter(lietotajs=online_user, merkis='atvalinajums').order_by('datums_no')

        paginator_atvalinajums = Paginator(atvalinajumu_ieraksti_saraksts, 5)  # Show 25 contacts per page

        table2 = request.GET.get('table2')
        try:
            atvalinajumu_ieraksti = paginator_atvalinajums.page(table2)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            atvalinajumu_ieraksti = paginator_atvalinajums.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            atvalinajumu_ieraksti = paginator_atvalinajums.page(paginator_atvalinajums.num_pages)




        komandejumu_ieraksti_saraksts = Ieraksts.objects.filter(lietotajs=online_user, merkis='komandejums').order_by('datums_no')

        paginator_komandejums = Paginator(komandejumu_ieraksti_saraksts, 5)  # Show 25 contacts per page

        table3 = request.GET.get('table3')
        try:
            komandejumu_ieraksti = paginator_komandejums.page(table3)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            komandejumu_ieraksti = paginator_komandejums.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            komandejumu_ieraksti = paginator_komandejums.page(paginator_komandejums.num_pages)

        merkis=request.POST.get("merkis")
        datums_no = request.POST.get("datums_no")
        datums_lidz = request.POST.get("datums_lidz")
        vieta = request.POST.get("vieta")

        online_user = request.user
        all_users = User.objects.all()

        if merkis:
            object = Ieraksts.objects.create(lietotajs=online_user, merkis=merkis, datums_no=datums_no, datums_lidz=datums_lidz, vieta=vieta)

            if len(request.FILES) != 0:
                iesniegums = request.FILES['iesniegums']

                fs = FileSystemStorage()
                fs.save(iesniegums.name, iesniegums)
                Atvalinajums.objects.create(ieraksts=object, iesniegums=iesniegums)

        context = {
            'ieraksti': ieraksti,
            'atvalinajumu_ieraksti': atvalinajumu_ieraksti,
            'komandejumu_ieraksti': komandejumu_ieraksti,
            'online_user': online_user,
            'all_users': all_users,
            'merkis': merkis,
            'datums_no': datums_no,
            'datums_lidz': datums_lidz,
            'vieta': vieta,
        }
        return render(request, 'mylist/index.html', context)


def all(request):
    if request.method == 'GET':

        # ieraksti_saraksts = Ieraksts.objects.all().order_by('datums_no')

        now = datetime.date.today()
        ieraksti_saraksts = Ieraksts.objects.filter(datums_no__lte=now, datums_lidz__gte=now).order_by('datums_no')

        paginator = Paginator(ieraksti_saraksts, 10)  # Show 25 contacts per page

        page = request.GET.get('page')
        try:
            ieraksti = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            ieraksti = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            ieraksti = paginator.page(paginator.num_pages)

        context = {
            'ieraksti': ieraksti,
        }
        return render(request, 'mylist/all.html', context)
