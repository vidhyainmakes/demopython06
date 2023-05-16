from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.urls import reverse

from .models import User, BankAccountType, UserBankAccount, UserAddress,  Keralabranch, Keraladistrict
from .constants import GENDER_CHOICE,  CHECKBOX_CHOICE


class UserAddressForm(forms.ModelForm):

    class Meta:
        model = UserAddress
        fields = [
            'street_address',
            'city',
            'postal_code',
            'country'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })

class UserRegistrationForm(UserCreationForm):
    # account_type = forms.ModelChoiceField(
    #     queryset=BankAccountType.objects.all()
    # )
    # gender = forms.ChoiceField(choices=GENDER_CHOICE,widget=forms.RadioSelect)
    # birth_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = [
            # 'first_name',
            # 'last_name',
            'email',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field != 'gender':
                self.fields[field].widget.attrs.update({
                    'class': (
                        'appearance-none block w-full bg-gray-200 '
                        'text-gray-700 border border-gray-200 '
                        'rounded py-3 px-4 leading-tight '
                        'focus:outline-none focus:bg-white '
                        'focus:border-gray-500'
                    )
                })

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            account_type = self.cleaned_data.get('account_type')
            gender = self.cleaned_data.get('gender')
            birth_date = self.cleaned_data.get('birth_date')

            UserBankAccount.objectUserSignupForms.create(
                user=user,
                gender=gender,
                birth_date=birth_date,
                account_type=account_type,
                account_no=(
                    user.id +
                    settings.ACCOUNT_NUMBER_START_FROM
                )
            )
        return user

class UserSignupForm(UserCreationForm):
    account_type = forms.ModelChoiceField(
        queryset=BankAccountType.objects.all()
    )
    # name = forms.CharField(max_length=200)
    gender = forms.ChoiceField(choices=GENDER_CHOICE,widget=forms.RadioSelect)
    age = forms.IntegerField()
    birth_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    phone_number = forms.IntegerField()
    keraladistrict = forms.ModelChoiceField(queryset=Keraladistrict.objects.all())
    keralabranch = forms.ModelChoiceField(queryset=Keralabranch.objects.all())
    materials=forms.ChoiceField(choices=CHECKBOX_CHOICE)

    class Meta:
        model = User
        fields = [
            'email',
            'password1',
            'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['keralabranch'].queryset = Keralabranch.objects.none()

        if 'keraladistrict' in self.data:
            try:
                keraladistrict_id = int(self.data.get('keraladistrict'))
                self.fields['keralabranch'].queryset = Keralabranch.objects.filter(keraladistrict=keraladistrict_id).order_by('user')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['keralabranch'].queryset = self.instance.keraladistrict.keralabranch_set.order_by('user')

        for field in self.fields:
            if field != 'gender':
                self.fields[field].widget.attrs.update({
                    'class': (
                        'appearance-none block w-full bg-gray-200 '
                        'text-gray-700 border border-gray-200 '
                        'rounded py-3 px-4 leading-tight '
                        'focus:outline-none focus:bg-white '
                        'focus:border-gray-500'
                    )
                })

    @transaction.atomic
    def save(self, commit=True):
        print("am i coming here?")
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            account_type = self.cleaned_data.get('account_type')
            gender = self.cleaned_data.get('gender')
            birth_date = self.cleaned_data.get('birth_date')

            UserBankAccount.objects.create(
                user=user,
                gender=gender,
                birth_date=birth_date,
                account_type=account_type,
                account_no=(
                    user.id +
                    settings.ACCOUNT_NUMBER_START_FROM
                )
            )
        return user



