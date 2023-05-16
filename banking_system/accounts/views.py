from celery.worker import request
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.core import paginator
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView
from django.shortcuts import render,get_object_or_404

from .forms import UserRegistrationForm, UserAddressForm, UserSignupForm
from accounts.models import Keralabranch, District

User = get_user_model()

class UserFormView(TemplateView):
    model = User
    form_class = UserSignupForm
    template_name = 'accounts/user_form.html'


    def post(self, request, *args, **kwargs):
        signup_form = UserSignupForm(self.request.POST)
        address_form = UserAddressForm(self.request.POST)
        print("signupform", signup_form.is_valid())
        print("addressform", address_form.is_valid())
        if address_form.is_valid():# signup_form.is_valid() and
            user =  signup_form.save()

            address = address_form.save(commit=False)
            address.user = user
            address.save()

            login(self.request, user)
            homepage = reverse_lazy('accounts:user_login')
            messages.success(
                self.request,
                 (
                    f'Thank You For Creating A Bank Account. <a href="{homepage}">Home</a> '
                )
            )

            return HttpResponseRedirect( reverse_lazy('accounts:user_form'))


        return self.render_to_response(
             self.get_context_data(
                    signup_form=signup_form,
                    address_form=address_form
                )
            )

    def get_context_data(self, **kwargs):
        if 'signup_form' not in kwargs:
            kwargs['signup_form'] = UserSignupForm()
        if 'address_form' not in kwargs:
            kwargs['address_form'] = UserAddressForm()

        return super().get_context_data(**kwargs)

def load_branches(request):
        keraladistrict_id = request.GET.get('keraladistrict_id')
        branches = Keralabranch.objects.filter(keraladistrict=keraladistrict_id).order_by('user')
        print("keraladistrict_id", keraladistrict_id)
        print("branches", branches)
        return render(request, 'accounts/user_dropdown.html', {'branches': branches})


class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/user_registration.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy('transactions:transaction_report')
            )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        registration_form = UserRegistrationForm(self.request.POST)
        # address_form = UserAddressForm(self.request.POST)

        if registration_form.is_valid(): #and address_form.is_valid():
            user = registration_form.save()
            return HttpResponseRedirect(reverse_lazy('accounts:user_login'))

            # address = address_form.save(commit=False)
            # address.user = user
            # address.save()

            login(self.request, user)
            messages.success(
                self.request,
                (
                    f'Thank You For Creating A Bank Account. '
                )
            )
            return HttpResponseRedirect( reverse_lazy('accounts:user_registration'))
            # return HttpResponseRedirect(
            #     reverse_lazy('transactions:deposit_money')
            # )

        return self.render_to_response(
            self.get_context_data(
                registration_form=registration_form,
                # address_form=address_form
            )
        )

    def get_context_data(self, **kwargs):
        if 'registration_form' not in kwargs:
            kwargs['registration_form'] = UserRegistrationForm()
        if 'address_form' not in kwargs:
            kwargs['address_form'] = UserAddressForm()

        return super().get_context_data(**kwargs)


class UserLoginView(LoginView):
    template_name='accounts/user_login.html'
    redirect_authenticated_user = True


class LogoutView(RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)

def allbranch(request,d_slug=None):
    d_page=None
    districts_list=None
    if d_slug!=None:
        d_page=get_object_or_404(District,slug=d_slug)
        # print ("d_page",d_page)
        districts_list=District.objects.all().filter(name=d_page)

    else:
         districts_list=District.objects.all()
    # print(districts_list)
    paginator = Paginator(districts_list, 6)
    try:
         page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
         districts = paginator.page(page)

    except  (EmptyPage, InvalidPage):
            districts= paginator.page(paginator.num_pages)
    # # print(districts)

    return render(request,"accounts/user_branches.html", {'districts':districts})




