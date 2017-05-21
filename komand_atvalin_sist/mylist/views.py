from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from .models import Ieraksts, Atvalinajums, Komandejums, SaglabatieLietotaji
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

        # ieraksti_saraksts = Ieraksts.objects.all().order_by('datums_no')

        now = datetime.date.today()
        ieraksti_saraksts = Ieraksts.objects.filter(datums_no__lte=now, datums_lidz__gte=now).order_by('lietotajs')

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


def saved(request):
    if request.method == 'GET':

        online_user = request.user

        saglabatie_lietotaji_saraksts = SaglabatieLietotaji.objects.filter(lietotajs_pats=online_user).values_list('saglabatais_lietotajs', flat=True)
        ieraksti = Ieraksts.objects.filter(lietotajs__in=saglabatie_lietotaji_saraksts)

        users = User.objects.exclude(id=online_user.id).exclude(id__in=saglabatie_lietotaji_saraksts)
        saved_users = User.objects.exclude(id=online_user.id).filter(id__in=saglabatie_lietotaji_saraksts)

        context = {
            'ieraksti': ieraksti,
            'users': users,
            'saved_users': saved_users,
        }
        return render(request, 'mylist/saved.html', context)

    if request.method == 'POST':

        online_user = request.user

        saglabatie_lietotaji_saraksts = SaglabatieLietotaji.objects.filter(lietotajs_pats=online_user).values_list('saglabatais_lietotajs', flat=True)
        ieraksti = Ieraksts.objects.filter(lietotajs__in=saglabatie_lietotaji_saraksts)

        users = User.objects.exclude(id=online_user.id).exclude(id__in=saglabatie_lietotaji_saraksts)
        saved_users = User.objects.exclude(id=online_user.id).filter(id__in=saglabatie_lietotaji_saraksts)

        pievienot_lietotaju = request.POST.get('pievienot_lietotaju')
        iznemt_lietotaju = request.POST.get('iznemt_lietotaju')

        total_user_count = User.objects.latest('id').id + 1
        print total_user_count

        if pievienot_lietotaju:
            counter = 0
            for _ in " " * total_user_count:
                string = 'add_user' + str(counter)
                posted_username = request.POST.get(string)
                if posted_username:
                    user_to_save = User.objects.get(username=posted_username)
                    print user_to_save
                    SaglabatieLietotaji.objects.create(lietotajs_pats=online_user, saglabatais_lietotajs=user_to_save)
                counter += 1

        elif iznemt_lietotaju:
            counter = 0
            for _ in " " * total_user_count:
                string = 'delete_user' + str(counter)
                posted_username = request.POST.get(string)
                if posted_username:
                    user_to_delete = User.objects.get(username=posted_username)
                    print user_to_delete
                    SaglabatieLietotaji.objects.get(lietotajs_pats=online_user, saglabatais_lietotajs=user_to_delete).delete()
                counter += 1


        context = {
            'ieraksti': ieraksti,
            'users': users,
            'saved_users': saved_users,
        }
        return render(request, 'mylist/saved.html', context)


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
                    return index(request)

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
                return index(request)

        context = {
            'login_error': login_error,
            'signup_error': signup_error,
        }
        return render(request, 'mylist/login.html', context)


class LoginView(FormView):
    success_url = '/mylist/'
    form_class = AuthenticationForm
    template_name = 'mylist/login.html'
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.POST.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to



# class UserFormView(View):
#     form_class = UserCreationForm
#     template_name = 'mylist/signup.html'
#
#     # display blank form
#     def get(self, request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#
#         if form.is_valid():
#
#             # create a user
#             user = form.save(commit=False)
#
#             # cleaned data
#
#             user.save()  # save to database
#
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('mylist:index')
#
#         return render(request, self.template_name, {'form': form})
