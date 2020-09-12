# -*- coding utf-8 -*-
# from django import forms
from kwauth.forms import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from kwauth.models import KWUser


class KWAdminUserCreateForm (UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
             'username', 'first_name', 'last_name', 'age', 'sex', 'avatar',
              'email', 'password1', 'password2', 'is_staff', 'is_superuser'
        )

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

