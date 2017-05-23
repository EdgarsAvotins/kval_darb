from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from .models import Ieraksts, Atvalinajums, Komandejums, SaglabatieLietotaji, Norikojums
import datetime

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.views.generic import View
from django.utils.http import is_safe_url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView
from django.http import HttpResponseRedirect


def index(request):
    if request.method == 'GET':

        online_user = request.user

        ieraksti_saraksts = Ieraksts.objects.filter(lietotajs=online_user).order_by('-datums_no')

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




        atvalinajumu_ieraksti_saraksts = Ieraksts.objects.filter(lietotajs=online_user, merkis='atvalinajums').order_by('-datums_no')

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




        komandejumu_ieraksti_saraksts = Ieraksts.objects.filter(lietotajs=online_user, merkis='komandejums').order_by('-datums_no')

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

        ieraksti_id = Ieraksts.objects.filter(lietotajs=online_user, merkis='komandejums').values_list('id', flat=True)
        komandejumu_failu_saraksts = Komandejums.objects.filter(ieraksts__id__in=ieraksti_id)

        context = {
            'ieraksti_saraksts': ieraksti_saraksts,
            'ieraksti' : ieraksti,
            'atvalinajumu_ieraksti': atvalinajumu_ieraksti,
            'komandejumu_ieraksti': komandejumu_ieraksti,
            'online_user': online_user,
            'komandejumu_failu_saraksts': komandejumu_failu_saraksts,
        }
        return render(request, 'mylist/index.html', context)






    if request.method=='POST':

        merkis = request.POST.get("merkis")
        datums_no = request.POST.get("datums_no")
        datums_lidz = request.POST.get("datums_lidz")
        vieta = request.POST.get("vieta")

        iesniegums_labot_id = request.POST.get("iesniegums_labot")
        atskaite_pievienot_id = request.POST.get("atskaite_pievienot")
        atskaite_labot_id = request.POST.get("atskaite_labot")

        online_user = request.user
        all_users = User.objects.all()

        files = request.FILES

        if merkis:
            object = Ieraksts.objects.create(lietotajs=online_user, merkis=merkis, datums_no=datums_no,
                                             datums_lidz=datums_lidz, vieta=vieta)

            if 'iesniegums' in files and merkis == 'atvalinajums':
                iesniegums = request.FILES['iesniegums']
                Atvalinajums.objects.create(ieraksts=object, iesniegums=iesniegums)

        elif iesniegums_labot_id:
            iesniegums_fails = request.FILES['iesniegums']

            pareizais_ieraksts = Ieraksts.objects.get(id=iesniegums_labot_id)
            pareizais_atvalinajums = Atvalinajums.objects.get(ieraksts=pareizais_ieraksts)
            pareizais_atvalinajums.iesniegums = iesniegums_fails
            pareizais_atvalinajums.save()



        elif atskaite_pievienot_id:
            pareizais_ieraksts = Ieraksts.objects.get(id=atskaite_pievienot_id)

            if 'ceks' in files and 'atskaite' in files:
                atskaite_fails = request.FILES['atskaite']
                ceks_fails = request.FILES['ceks']
                Komandejums.objects.create(ieraksts=pareizais_ieraksts, atskaite=atskaite_fails, ceks=ceks_fails)

            elif 'atskaite' in files:
                atskaite_fails = request.FILES['atskaite']
                Komandejums.objects.create(ieraksts=pareizais_ieraksts, atskaite=atskaite_fails)


        elif atskaite_labot_id:

            pareizais_ieraksts = Ieraksts.objects.get(id=atskaite_labot_id)
            pareizais_komandejums = Komandejums.objects.get(ieraksts=pareizais_ieraksts)

            if 'ceks' and 'atskaite' in files:
                atskaite_fails = request.FILES['atskaite']
                ceks_fails = request.FILES['ceks']
                pareizais_komandejums.atskaite = atskaite_fails
                pareizais_komandejums.ceks = ceks_fails
                pareizais_komandejums.save()

            elif 'atskaite' in files:
                atskaite_fails = request.FILES['atskaite']
                pareizais_komandejums.atskaite = atskaite_fails
                pareizais_komandejums.save()

            elif 'ceks' in files:
                ceks_fails = request.FILES['ceks']
                pareizais_komandejums.ceks = ceks_fails
                pareizais_komandejums.save()




        ieraksti_saraksts = Ieraksts.objects.filter(lietotajs=online_user).order_by('-datums_no')

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




        atvalinajumu_ieraksti_saraksts = Ieraksts.objects.filter(lietotajs=online_user, merkis='atvalinajums').order_by('-datums_no')

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




        komandejumu_ieraksti_saraksts = Ieraksts.objects.filter(lietotajs=online_user, merkis='komandejums').order_by('-datums_no')

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



        ieraksti_id = Ieraksts.objects.filter(lietotajs=online_user, merkis='komandejums').values_list('id', flat=True)
        komandejumu_failu_saraksts = Komandejums.objects.filter(ieraksts__id__in=ieraksti_id)

        context = {
            'ieraksti_saraksts': ieraksti_saraksts,
            'ieraksti': ieraksti,
            'atvalinajumu_ieraksti': atvalinajumu_ieraksti,
            'komandejumu_ieraksti': komandejumu_ieraksti,
            'online_user': online_user,
            'all_users': all_users,
            'komandejumu_failu_saraksts': komandejumu_failu_saraksts,
        }
        return render(request, 'mylist/index.html', context)


def all(request):
    if request.method == 'GET':

        online_user = request.user
        users = User.objects.all()

        now = datetime.date.today()
        ieraksti_saraksts = Ieraksts.objects.exclude(lietotajs=online_user).filter(datums_no__lte=now, datums_lidz__gte=now).order_by('lietotajs')

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
            'online_user': online_user,
            'users': users,
        }
        return render(request, 'mylist/all.html', context)


def saved(request):
    if request.method == 'GET':

        online_user = request.user
        all_users = User.objects.all()

        saglabatie_lietotaji_saraksts = SaglabatieLietotaji.objects.filter(lietotajs_pats=online_user).values_list('saglabatais_lietotajs', flat=True)
        ieraksti = Ieraksts.objects.filter(lietotajs__in=saglabatie_lietotaji_saraksts)

        users = User.objects.exclude(id=online_user.id).exclude(id__in=saglabatie_lietotaji_saraksts)
        saved_users = User.objects.exclude(id=online_user.id).filter(id__in=saglabatie_lietotaji_saraksts)

        context = {
            'ieraksti': ieraksti,
            'users': users,
            'all_users': all_users,
            'saved_users': saved_users,
            'online_user': online_user,
        }
        return render(request, 'mylist/saved.html', context)

    if request.method == 'POST':

        online_user = request.user
        all_users = User.objects.all()

        saglabatie_lietotaji_saraksts = SaglabatieLietotaji.objects.filter(lietotajs_pats=online_user).values_list('saglabatais_lietotajs', flat=True)
        ieraksti = Ieraksts.objects.filter(lietotajs__in=saglabatie_lietotaji_saraksts)

        users = User.objects.exclude(id=online_user.id).exclude(id__in=saglabatie_lietotaji_saraksts)
        saved_users = User.objects.exclude(id=online_user.id).filter(id__in=saglabatie_lietotaji_saraksts)

        pievienot_lietotaju = request.POST.get('pievienot_lietotaju')
        iznemt_lietotaju = request.POST.get('iznemt_lietotaju')

        total_user_count = User.objects.latest('id').id + 1

        if pievienot_lietotaju:
            counter = 0
            for _ in " " * total_user_count:
                string = 'add_user' + str(counter)
                posted_username = request.POST.get(string)
                if posted_username:
                    user_to_save = User.objects.get(username=posted_username)
                    SaglabatieLietotaji.objects.create(lietotajs_pats=online_user, saglabatais_lietotajs=user_to_save)
                counter += 1

        elif iznemt_lietotaju:
            counter = 0
            for _ in " " * total_user_count:
                string = 'delete_user' + str(counter)
                posted_username = request.POST.get(string)
                if posted_username:
                    user_to_delete = User.objects.get(username=posted_username)
                    SaglabatieLietotaji.objects.get(lietotajs_pats=online_user, saglabatais_lietotajs=user_to_delete).delete()
                counter += 1


        context = {
            'ieraksti': ieraksti,
            'users': users,
            'all_users': all_users,
            'saved_users': saved_users,
            'online_user': online_user,
        }
        return render(request, 'mylist/saved.html', context)


def employees(request):
    if request.method == 'GET':

        online_user = request.user
        users = User.objects.all().order_by('last_name')

        context = {
            'online_user': online_user,
            'users': users,
        }
        return render(request, 'mylist/employees.html', context)


    if request.method == 'POST':

        correct_user = None
        online_user = request.user
        users = User.objects.all().order_by('last_name')

        darbinieks_pieprasit = request.POST.get("darbinieks_pieprasit")
        iesniegums_labot_id = request.POST.get("iesniegums_labot")
        atskaite_pievienot_id = request.POST.get("atskaite_pievienot")
        atskaite_labot_id = request.POST.get("atskaite_labot")
        rikojums_pievienot_id = request.POST.get("rikojums_pievienot")
        rikojums_labot_id = request.POST.get("rikojums_labot")
        statuss_nav_kartiba = request.POST.get("statuss_nav_kartiba")
        statuss_kartiba = request.POST.get("statuss_kartiba")
        izdzest_ierakstu = request.POST.get("izdzest_ierakstu")

        files = request.FILES

        if darbinieks_pieprasit:
            full_name = darbinieks_pieprasit.split()
            name = full_name[0]
            surname = full_name[1]
            correct_user = User.objects.get(first_name=name, last_name=surname)

        elif iesniegums_labot_id:
            iesniegums_fails = request.FILES['iesniegums']

            pareizais_ieraksts = Ieraksts.objects.get(id=iesniegums_labot_id)
            pareizais_atvalinajums = Atvalinajums.objects.get(ieraksts=pareizais_ieraksts)
            pareizais_atvalinajums.iesniegums = iesniegums_fails
            pareizais_atvalinajums.save()

            correct_user = User.objects.get(username=pareizais_ieraksts.lietotajs)

        elif atskaite_pievienot_id:
            pareizais_ieraksts = Ieraksts.objects.get(id=atskaite_pievienot_id)

            if 'ceks' in files and 'atskaite' in files:
                atskaite_fails = request.FILES['atskaite']
                ceks_fails = request.FILES['ceks']
                Komandejums.objects.create(ieraksts=pareizais_ieraksts, atskaite=atskaite_fails, ceks=ceks_fails)

            elif 'atskaite' in files:
                atskaite_fails = request.FILES['atskaite']
                Komandejums.objects.create(ieraksts=pareizais_ieraksts, atskaite=atskaite_fails)

            correct_user = User.objects.get(username=pareizais_ieraksts.lietotajs)

        elif atskaite_labot_id:

            pareizais_ieraksts = Ieraksts.objects.get(id=atskaite_labot_id)
            pareizais_komandejums = Komandejums.objects.get(ieraksts=pareizais_ieraksts)

            if 'ceks' and 'atskaite' in files:
                atskaite_fails = request.FILES['atskaite']
                ceks_fails = request.FILES['ceks']
                pareizais_komandejums.atskaite = atskaite_fails
                pareizais_komandejums.ceks = ceks_fails
                pareizais_komandejums.save()

            elif 'atskaite' in files:
                atskaite_fails = request.FILES['atskaite']
                pareizais_komandejums.atskaite = atskaite_fails
                pareizais_komandejums.save()

            elif 'ceks' in files:
                ceks_fails = request.FILES['ceks']
                pareizais_komandejums.ceks = ceks_fails
                pareizais_komandejums.save()

            correct_user = User.objects.get(username=pareizais_ieraksts.lietotajs)

        elif rikojums_pievienot_id:

            rikojums_fails = request.FILES['rikojums']
            pareizais_ieraksts = Ieraksts.objects.get(id=rikojums_pievienot_id)
            Norikojums.objects.create(ieraksts=pareizais_ieraksts, norikojums=rikojums_fails)

            correct_user = User.objects.get(username=pareizais_ieraksts.lietotajs)

        elif rikojums_labot_id:

            rikojums_fails = request.FILES['rikojums']
            pareizais_ieraksts = Ieraksts.objects.get(id=rikojums_labot_id)
            pareizais_rikojums = Norikojums.objects.get(ieraksts=pareizais_ieraksts)
            pareizais_rikojums.norikojums = rikojums_fails
            pareizais_rikojums.save()

            correct_user = User.objects.get(username=pareizais_ieraksts.lietotajs)
            print correct_user

        elif statuss_nav_kartiba:

            pareizais_ieraksts = Ieraksts.objects.get(id=statuss_nav_kartiba)
            pareizais_ieraksts.statuss = False
            pareizais_ieraksts.save()

            correct_user = User.objects.get(username=pareizais_ieraksts.lietotajs)

        elif statuss_kartiba:

            pareizais_ieraksts = Ieraksts.objects.get(id=statuss_kartiba)
            pareizais_ieraksts.statuss = True
            pareizais_ieraksts.save()

            correct_user = User.objects.get(username=pareizais_ieraksts.lietotajs)

        elif izdzest_ierakstu:

            pareizais_ieraksts = Ieraksts.objects.get(id=izdzest_ierakstu)
            correct_user = User.objects.get(username=pareizais_ieraksts.lietotajs)
            pareizais_ieraksts.delete()



        ieraksti = Ieraksts.objects.filter(lietotajs=correct_user).order_by('-datums_no')
        ieraksti_id = Ieraksts.objects.filter(lietotajs=correct_user, merkis='komandejums').values_list('id',
                                                                                                        flat=True)
        komandejumu_failu_saraksts = Komandejums.objects.filter(ieraksts__id__in=ieraksti_id)
        norikojumu_failu_saraksts = Norikojums.objects.filter(ieraksts__id__in=ieraksti_id)

        ieraksti_id = Ieraksts.objects.filter(lietotajs=correct_user, merkis='atvalinajums').values_list('id',
                                                                                                        flat=True)
        atvalinajumu_failu_saraksts = Atvalinajums.objects.filter(ieraksts__id__in=ieraksti_id)

        context = {
            'online_user': online_user,
            'users': users,
            'ieraksti': ieraksti,
            'komandejumu_failu_saraksts': komandejumu_failu_saraksts,
            'norikojumu_failu_saraksts': norikojumu_failu_saraksts,
            'atvalinajumu_failu_saraksts': atvalinajumu_failu_saraksts,
            'correct_user': correct_user,
        }
        return render(request, 'mylist/employees.html', context)


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/mylist/login/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


def login_page(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'mylist/login.html', context)

    if request.method == 'POST':

        login_form = request.POST.get("login_form")
        signup_form = request.POST.get("signup_form")
        login_error = ''
        signup_error = ''

        if login_form:
            username = request.POST.get("username")
            found_user = User.objects.filter(username=username)

            if found_user:
                user = authenticate(username=username, password=request.POST.get("password"))

                if user is not None:
                    login(request, user)
                    # return index(request)
                    return HttpResponseRedirect('/mylist/')

                else:
                    login_error = 'Incorrect password'

            else:
                login_error = 'Username does not exist'

        if signup_form:
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            username = request.POST.get("username")
            password = request.POST.get("password")

            found_user = User.objects.filter(username=username)

            if found_user:
                signup_error = 'Username already taken'

            else:
                User.objects.create_user(first_name=first_name, last_name=last_name,
                                         username=username, password=password)

                user = authenticate(username=username, password=password)
                login(request, user)
                # return index(request)
                return HttpResponseRedirect('/mylist/')

        context = {
            'login_error': login_error,
            'signup_error': signup_error,
        }
        return render(request, 'mylist/login.html', context)
