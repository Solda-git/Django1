# -*- coding utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from kwauth.models import KWUser


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
        fields = ('username', 'first_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
            print(f'field_name={field_name}, field={field}')


class KWProfileForm(UserChangeForm):
    class Meta:
        model = KWUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
            print(f'field_name={field_name}, field={field}')
