# -*- coding utf-8 -*-
import hashlib
import random
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from kwauth.models import KWUser, KWUserProfile


class KWAuthenticationForm(AuthenticationForm):
    class Meta:
        model = KWUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
            print(f'field_name={field_name}, field={field}')


class KWRegisterForm(UserCreationForm):
    class Meta:
        model = KWUser
        fields = ('username', 'first_name', 'last_name', 'age', 'sex', 'avatar', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
            field.help_text = ''

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 10:
            raise forms.ValidationError("В таком возрасте слишком рано сидеть за комьютером!")
        return data

    def clean_sex(self):
        data = self.cleaned_data['sex']
        if data not in ['м', 'М', 'ж', 'Ж', 'm', 'M', 'f', 'F']:
            raise forms.ValidationError('Допустимые значения: "м" или "ж".')
        return data

    def save(self, commit = True):
        user = super().save(commit)
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()
        return user


class KWProfileForm(UserChangeForm):
    class Meta:
        model = KWUser
        fields = ('username', 'first_name', 'last_name',
                  'age', #'sex',
                  'avatar', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 10:
            raise forms.ValidationError("В таком возрасте слишком рано сидеть за комьютером!")
        return data
    #
    # def clean_sex(self):
    #     data = self.cleaned_data['sex']
    #     if data not in ['м', 'М', 'ж', 'Ж', 'm', 'M', 'f', 'F']:
    #         raise forms.ValidationError('Допустимые значения: "м" или "ж".')
    #     return data


class KWUserExtendedProfileForm(forms.ModelForm):
    class Meta:
        model = KWUserProfile
        fields = ('tagline', 'aboutMe', 'gender')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
