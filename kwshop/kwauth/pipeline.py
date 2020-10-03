from collections import OrderedDict
from urllib.parse import urlunparse, urlencode
from datetime import datetime, timedelta
from urllib.request import urlopen

from django.core.files.base import ContentFile
from django.utils import timezone
from django.utils.timezone import now
from social_core.exceptions import AuthForbidden

from kwauth.models import KWUserProfile
import requests

def save_user_profile(backend, user, response, *args, **kwargs):
    print(f'request: {response}')
    if backend.name == 'vk-oauth2':
    #     api_url = urlunparse(
    #         (
    #             'https','api.vk.com','/method/users.get', None,
    #             urlencode(
    #                 OrderedDict(fields= ','.join(('bdate', 'sex', 'about')),
    #                             access_token=response['access_token'],
    #                             v='5.124')),
    #             None
    #         )
    #     )
    # resp = requests.get(api_url)
    # if resp.status_code != 200:
    #     return
    # data = resp.json()[response][0]
    # if data['sex']:
    #     user.kwuserprofile.gender = KWUserProfile.MALE if data['sex'] == 2 else KWUserProfile.FEMALE
    # if data['about']:
    #     user.kwuserprofile.aboutMe = data['about']
    # if data['bdate']:
    #     bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
    #     age = timezone.now().date().year - bdate.year
    # if  age <  18:
    #     user.delete()
    #     raise  AuthForbidden(  'social_core.backends.vk.VKOAuth2'  )
    # user.kwuserprofile.gender = KWUserProfile.MALE if response['sex'] == 2 else KWUserProfile.FEMALE
        print(f'response.keys:  {response.keys}')
        if 'sex' in response.keys():
            user.kwuserprofile.gender = KWUserProfile.MALE if response['sex'] == 2 else KWUserProfile.FEMALE
        if 'about' in response.keys():
            user.kwuserprofile.aboutMe = response['about']
        if 'bdate' in response.keys():
            user.age = response['bdate']
            if now() - response['bdate'] < timedelta(years=18):
                user.delete()
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        if 'email' in response.keys():
            user.email = response['email']
        if 'photo' in response.keys():
            if not user.avatar:
                url = response['photo']
                user.avatar.save(f'{user.username}_ava.jpg', ContentFile(urlopen(url).read()))
    user.save()
