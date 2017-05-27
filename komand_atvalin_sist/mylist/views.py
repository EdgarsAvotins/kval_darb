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


def index(request): # /mylist/
    if request.method == 'GET':

        online_user = request.user  # mana lietotaja objekts

        ieraksti_saraksts = Ieraksts.objects.filter(lietotajs=online_user).order_by('-datums_no')   # saraksts ar online lietotaja ierakstiem, kratoti pec jaunaka datuma

        paginator_kopejais = Paginator(ieraksti_saraksts, 10)  # radit 10 ierakstus katra lapa

        table1 = request.GET.get('table1')  # kopeja tabula
        try:
            ieraksti = paginator_kopejais.page(table1)
        except PageNotAnInteger:
            # ja page nav integer, tad atgriest pirmo
            ieraksti = paginator_kopejais.page(1)
        except EmptyPage:
            # ja page ir arpus meroga, tad atgriest pedejo lapu
            ieraksti = paginator_kopejais.page(paginator_kopejais.num_pages)




        atvalinajumu_ieraksti_saraksts = Ieraksts.objects.filter(lietotajs=online_user, merkis='atvalinajums').order_by('-datums_no')   # visi mani atvalinajumu ieraksti

        paginator_atvalinajums = Paginator(atvalinajumu_ieraksti_saraksts, 5)  # radit piecus ierakstus katra lapa

        table2 = request.GET.get('table2') # atvalinajumu tabula
        try:
            atvalinajumu_ieraksti = paginator_atvalinajums.page(table2)
        except PageNotAnInteger:
            atvalinajumu_ieraksti = paginator_atvalinajums.page(1)
        except EmptyPage:
            atvalinajumu_ieraksti = paginator_atvalinajums.page(paginator_atvalinajums.num_pages)




        komandejumu_ieraksti_saraksts = Ieraksts.objects.filter(lietotajs=online_user, merkis='komandejums').order_by('-datums_no')     # visi mani komandejumi

        paginator_komandejums = Paginator(komandejumu_ieraksti_saraksts, 5)  # radit piecus ierakstus katra lapa

        table3 = request.GET.get('table3')  # komandejumu tabula
        try:
            komandejumu_ieraksti = paginator_komandejums.page(table3)
        except PageNotAnInteger:
            komandejumu_ieraksti = paginator_komandejums.page(1)
        except EmptyPage:
            komandejumu_ieraksti = paginator_komandejums.page(paginator_komandejums.num_pages)

        ieraksti_id = Ieraksts.objects.filter(lietotajs=online_user, merkis='komandejums').values_list('id', flat=True)     # manu komandejumu id
        komandejumu_failu_saraksts = Komandejums.objects.filter(ieraksts__id__in=ieraksti_id)   # manu komandejumu failu saraksts

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

        files = request.FILES   # visu iesutito failu nosaukumi

        if merkis:  # ja ir pievienots jauns ieraksts
            object = Ieraksts.objects.create(lietotajs=online_user, merkis=merkis, datums_no=datums_no,
                                             datums_lidz=datums_lidz, vieta=vieta)  # izveidot jaunu ierakstu. ja iesniegums, tad vieta = null

            if 'iesniegums' in files and merkis == 'atvalinajums':  # ja merkis ir atvalinajums un ir iesutits iesniegums
                iesniegums = request.FILES['iesniegums']            # pieprasa iesnieguma failu
                Atvalinajums.objects.create(ieraksts=object, iesniegums=iesniegums)     # saglaba datu baze sim atvalinajumam iesniegumu

        elif iesniegums_labot_id:   # ja velas labot iesniegumu
            iesniegums_fails = request.FILES['iesniegums']      # iesutitais iesniegums

            pareizais_ieraksts = Ieraksts.objects.get(id=iesniegums_labot_id)   # atrod pareizo ierakstu
            pareizais_atvalinajums = Atvalinajums.objects.get(ieraksts=pareizais_ieraksts)  # atrod pareizo atvalinajumu
            pareizais_atvalinajums.iesniegums = iesniegums_fails    # saglaba jauno failu
            pareizais_atvalinajums.save()   #saglaba izmainas datu baze



        elif atskaite_pievienot_id:   # ja velas pievienot atskaiti
            pareizais_ieraksts = Ieraksts.objects.get(id=atskaite_pievienot_id)

            if 'ceks' in files and 'atskaite' in files:
                atskaite_fails = request.FILES['atskaite']
                ceks_fails = request.FILES['ceks']
                Komandejums.objects.create(ieraksts=pareizais_ieraksts, atskaite=atskaite_fails, ceks=ceks_fails)

            elif 'atskaite' in files:
                atskaite_fails = request.FILES['atskaite']
                Komandejums.objects.create(ieraksts=pareizais_ieraksts, atskaite=atskaite_fails)


        elif atskaite_labot_id:     #ja velas labot atskaiti

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



            # talak tapat ka GET metode
        ieraksti_saraksts = Ieraksts.objects.filter(lietotajs=online_user).order_by('-datums_no')

        paginator_kopejais = Paginator(ieraksti_saraksts, 10)

        table1 = request.GET.get('table1')
        try:
            ieraksti = paginator_kopejais.page(table1)
        except PageNotAnInteger:
            ieraksti = paginator_kopejais.page(1)
        except EmptyPage:
            ieraksti = paginator_kopejais.page(paginator_kopejais.num_pages)




        atvalinajumu_ieraksti_saraksts = Ieraksts.objects.filter(lietotajs=online_user, merkis='atvalinajums').order_by('-datums_no')

        paginator_atvalinajums = Paginator(atvalinajumu_ieraksti_saraksts, 5)

        table2 = request.GET.get('table2')
        try:
            atvalinajumu_ieraksti = paginator_atvalinajums.page(table2)
        except PageNotAnInteger:
            atvalinajumu_ieraksti = paginator_atvalinajums.page(1)
        except EmptyPage:
            atvalinajumu_ieraksti = paginator_atvalinajums.page(paginator_atvalinajums.num_pages)




        komandejumu_ieraksti_saraksts = Ieraksts.objects.filter(lietotajs=online_user, merkis='komandejums').order_by('-datums_no')

        paginator_komandejums = Paginator(komandejumu_ieraksti_saraksts, 5)

        table3 = request.GET.get('table3')
        try:
            komandejumu_ieraksti = paginator_komandejums.page(table3)
        except PageNotAnInteger:
            komandejumu_ieraksti = paginator_komandejums.page(1)
        except EmptyPage:
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
            # atlasam visus aktivos ierakstus. taa, ka datums_no < tagad < datums_lidz
        ieraksti_saraksts = Ieraksts.objects.exclude(lietotajs=online_user).filter(datums_no__lte=now, datums_lidz__gte=now).order_by('lietotajs')

            # atkal dalam lpp
        paginator = Paginator(ieraksti_saraksts, 10)

        page = request.GET.get('page')
        try:
            ieraksti = paginator.page(page)
        except PageNotAnInteger:
            ieraksti = paginator.page(1)
        except EmptyPage:
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

            # atrodam visus savus saglabatos lietotajus
        saglabatie_lietotaji_saraksts = SaglabatieLietotaji.objects.filter(lietotajs_pats=online_user).values_list('saglabatais_lietotajs', flat=True)
        now = datetime.date.today()
            # atlasam visus aktivos ierakstus saviem saglabatajiem lietotajiem
        ieraksti = Ieraksts.objects.filter(lietotajs__in=saglabatie_lietotaji_saraksts).filter(datums_no__lte=now, datums_lidz__gte=now).order_by('lietotajs')

            # atlasam visus lietotajus, iznemot sevi un tos, kas jau ir pie saglabatajiem
        users = User.objects.exclude(id=online_user.id).exclude(id__in=saglabatie_lietotaji_saraksts)
            # atlasam visus saglabatos lietotajus
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

            # atrodam visus savus saglabatos lietotajus
        saglabatie_lietotaji_saraksts = SaglabatieLietotaji.objects.filter(lietotajs_pats=online_user).values_list('saglabatais_lietotajs', flat=True)
        now = datetime.date.today()
            # atlasam visus aktivos ierakstus saviem saglabatajiem lietotajiem
        ieraksti = Ieraksts.objects.filter(lietotajs__in=saglabatie_lietotaji_saraksts).filter(datums_no__lte=now, datums_lidz__gte=now).order_by('lietotajs')
            # atlasam visus lietotajus, iznemot sevi un tos, kas jau ir pie saglabatajiem
        users = User.objects.exclude(id=online_user.id).exclude(id__in=saglabatie_lietotaji_saraksts)
            # atlasam visus saglabatos lietotajus
        saved_users = User.objects.exclude(id=online_user.id).filter(id__in=saglabatie_lietotaji_saraksts)

        pievienot_lietotaju = request.POST.get('pievienot_lietotaju')
        iznemt_lietotaju = request.POST.get('iznemt_lietotaju')

        total_user_count = User.objects.latest('id').id + 1     # lietotaju nevar but vairak neka lielakais id + 1

        if pievienot_lietotaju: # ja megina pievienot lietotaju sagalabajiem
            counter = 0
            for _ in " " * total_user_count:            # iziet ciklam tik reizes cauri, cik ir lietotaju
                string = 'add_user' + str(counter)      # piemeram add_user25
                posted_id = request.POST.get(string)    # apskatamies, vai ir iesutits, ka grib pievienot so lietotaju
                if posted_id:                           # ja atrodam, saglabajam, ja ne, ejam talak
                    user_to_save = User.objects.get(id=counter)
                        # izveidojam jauno "saglabatie" ierakstu pari - es un tas, ko gribeju pievienot
                    SaglabatieLietotaji.objects.create(lietotajs_pats=online_user, saglabatais_lietotajs=user_to_save)
                counter += 1

        elif iznemt_lietotaju:  # tapat, ka meginot pievienot
            counter = 0
            for _ in " " * total_user_count:
                string = 'delete_user' + str(counter)
                posted_id = request.POST.get(string)
                if posted_id:
                    user_to_delete = User.objects.get(id=counter)
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

        correct_user = None     # te saglabasim to lietotaju, kura sarakstu gribam skatities
        online_user = request.user
        users = User.objects.all().order_by('last_name')    # lietotaju saraksts, no kura izvelesimies pievienot

        darbinieks_pieprasit = request.POST.get("darbinieks_pieprasit")
        iesniegums_labot_id = request.POST.get("iesniegums_labot")
        atskaite_pievienot_id = request.POST.get("atskaite_pievienot")
        atskaite_labot_id = request.POST.get("atskaite_labot")
        rikojums_pievienot_id = request.POST.get("rikojums_pievienot")
        rikojums_labot_id = request.POST.get("rikojums_labot")
        statuss_nav_kartiba = request.POST.get("statuss_nav_kartiba")
        statuss_kartiba = request.POST.get("statuss_kartiba")
        izdzest_ierakstu = request.POST.get("izdzest_ierakstu")

        files = request.FILES   # augsupladeto failu nosaukumi

        if darbinieks_pieprasit:    # ja pieprasa apskatit darbinieku
            full_name = darbinieks_pieprasit.split()    # sadalam, lai varetu atrast datu baze lietotaju pec varda, uzvarda
            name = full_name[0]
            surname = full_name[1]
            correct_user = User.objects.get(first_name=name, last_name=surname) # atrodam datu baze

        elif iesniegums_labot_id:
            iesniegums_fails = request.FILES['iesniegums']

            pareizais_ieraksts = Ieraksts.objects.get(id=iesniegums_labot_id)
            pareizais_atvalinajums = Atvalinajums.objects.get(ieraksts=pareizais_ieraksts)
            pareizais_atvalinajums.iesniegums = iesniegums_fails    # saglabajam jauno iesniegumu
            pareizais_atvalinajums.save()   # saglabajam izmainas datu baze

            correct_user = User.objects.get(username=pareizais_ieraksts.lietotajs)

        elif atskaite_pievienot_id:
            pareizais_ieraksts = Ieraksts.objects.get(id=atskaite_pievienot_id)

            if 'ceks' in files and 'atskaite' in files: # ja atsutita gan atskaite, gan ceki
                atskaite_fails = request.FILES['atskaite']
                ceks_fails = request.FILES['ceks']
                    # saglabajam failus, savienojam ar ierakstu
                Komandejums.objects.create(ieraksts=pareizais_ieraksts, atskaite=atskaite_fails, ceks=ceks_fails)

            elif 'atskaite' in files:   # ja tikai atskaite
                atskaite_fails = request.FILES['atskaite']
                Komandejums.objects.create(ieraksts=pareizais_ieraksts, atskaite=atskaite_fails)

            correct_user = User.objects.get(username=pareizais_ieraksts.lietotajs)

        elif atskaite_labot_id:

            pareizais_ieraksts = Ieraksts.objects.get(id=atskaite_labot_id)
            pareizais_komandejums = Komandejums.objects.get(ieraksts=pareizais_ieraksts)

            if 'ceks' and 'atskaite' in files:  # ja atsutija gan cekus, gan atskaiti
                atskaite_fails = request.FILES['atskaite']
                ceks_fails = request.FILES['ceks']
                pareizais_komandejums.atskaite = atskaite_fails
                pareizais_komandejums.ceks = ceks_fails
                pareizais_komandejums.save()

            elif 'atskaite' in files:   # ja tikai atskaite
                atskaite_fails = request.FILES['atskaite']
                pareizais_komandejums.atskaite = atskaite_fails
                pareizais_komandejums.save()

            elif 'ceks' in files:   # ja tikai ceki
                ceks_fails = request.FILES['ceks']
                pareizais_komandejums.ceks = ceks_fails
                pareizais_komandejums.save()

            correct_user = User.objects.get(username=pareizais_ieraksts.lietotajs)

        elif rikojums_pievienot_id:

            rikojums_fails = request.FILES['rikojums']
            pareizais_ieraksts = Ieraksts.objects.get(id=rikojums_pievienot_id)
                # izveidojam jaunu norikojumu, pievienojam ierakstam
            Norikojums.objects.create(ieraksts=pareizais_ieraksts, norikojums=rikojums_fails)

            correct_user = User.objects.get(username=pareizais_ieraksts.lietotajs)

        elif rikojums_labot_id:

            rikojums_fails = request.FILES['rikojums']
            pareizais_ieraksts = Ieraksts.objects.get(id=rikojums_labot_id)
            pareizais_rikojums = Norikojums.objects.get(ieraksts=pareizais_ieraksts)
            pareizais_rikojums.norikojums = rikojums_fails
            pareizais_rikojums.save()   # saglabajam datu baze izmainas ar jauno norikojumu

            correct_user = User.objects.get(username=pareizais_ieraksts.lietotajs)
            print correct_user

        elif statuss_nav_kartiba:   # statuss ir True, bet grib padarit par False, jeb grib uzlikt "Nav kartiba"

            pareizais_ieraksts = Ieraksts.objects.get(id=statuss_nav_kartiba)
            pareizais_ieraksts.statuss = False
            pareizais_ieraksts.save()

            correct_user = User.objects.get(username=pareizais_ieraksts.lietotajs)

        elif statuss_kartiba:   # statuss ir False, bet grib padarit par True, jeb grib uzlikt "Kartiba"

            pareizais_ieraksts = Ieraksts.objects.get(id=statuss_kartiba)
            pareizais_ieraksts.statuss = True
            pareizais_ieraksts.save()

            correct_user = User.objects.get(username=pareizais_ieraksts.lietotajs)

        elif izdzest_ierakstu:

            pareizais_ieraksts = Ieraksts.objects.get(id=izdzest_ierakstu)
            correct_user = User.objects.get(username=pareizais_ieraksts.lietotajs)
            pareizais_ieraksts.delete()     #izdzes pareizo ierakstu


            # visi mani ieraksti, kartoti pec datuma
        ieraksti = Ieraksts.objects.filter(lietotajs=correct_user).order_by('-datums_no')
            # visi manu komandejumu id
        ieraksti_id = Ieraksts.objects.filter(lietotajs=correct_user, merkis='komandejums').values_list('id',
                                                                                                        flat=True)
            # manu ierakstu komandejumu faili, jeb ceki un atskaites
        komandejumu_failu_saraksts = Komandejums.objects.filter(ieraksts__id__in=ieraksti_id)
            # manu ierakstu norikojumu faili
        norikojumu_failu_saraksts = Norikojums.objects.filter(ieraksts__id__in=ieraksti_id)

            # visi manu atvalinajumu id
        ieraksti_id = Ieraksts.objects.filter(lietotajs=correct_user, merkis='atvalinajums').values_list('id',
                                                                                                        flat=True)
            # manu ierakstu atvalinajumu faili, jeb iesniegumi
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

    def get(self, request, *args, **kwargs):    # pienem visus mainigos, taja skaita manus datus, lai izrakstities
        auth_logout(request)        # izrakstities
        return super(LogoutView, self).get(request, *args, **kwargs)    #pariet uz login skatu


def login_page(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'mylist/login.html', context)

    if request.method == 'POST':

        login_form = request.POST.get("login_form")
        signup_form = request.POST.get("signup_form")
        login_error = ''
        signup_error = ''

        if login_form:  # ja meginu pieslegties
            username = request.POST.get("username").lower()
            found_user = User.objects.filter(username=username)

            if found_user:  # ja eksiste lietotajvards
                    # atgriez None, ja nesakrit parole vai lietotaja objektu, ja viss pareizi
                user = authenticate(username=username, password=request.POST.get("password"))

                if user is not None:    # ja pareizi dati
                    login(request, user)    # pieslegties
                    # return index(request)
                    return HttpResponseRedirect('/mylist/') # pariet uz mana saraksta skatu

                else:   # ja nepareiza parole
                    login_error = 'Nepareiza parole'

            else:   # ja neeksiste lietotajvards
                login_error = 'Lietotajvards neeksiste'

        if signup_form: # ja megina pierakstities
            first_name = request.POST.get("first_name").title()
            last_name = request.POST.get("last_name").title()
            username = request.POST.get("username").lower()
            password = request.POST.get("password")

            found_user = User.objects.filter(username=username)

            if found_user:  # ja eksiste jau lietotajs
                signup_error = 'Lietotajvards jau eksiste'

            else:   # ja neeksiste
                    # izveidojam jaunu lietotaju
                User.objects.create_user(first_name=first_name, last_name=last_name,
                                         username=username, password=password)

                user = authenticate(username=username, password=password)
                login(request, user)    # piesledzamies
                # return index(request)
                return HttpResponseRedirect('/mylist/')     # parejam uz mana saraksta skatu

        context = {
            'login_error': login_error,
            'signup_error': signup_error,
        }
        return render(request, 'mylist/login.html', context)
