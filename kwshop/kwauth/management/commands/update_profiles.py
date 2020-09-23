# -*- coding utf-8 -*-

from django.core.management.base import BaseCommand

from kwauth.models import KWUser, KWUserProfile


class Command(BaseCommand):
    help = 'This command updates kwuser profiles.'

    def handle(self, *args, **kwargs):
        for user in KWUser.objects.filter(kwuserprofile__gender__isnull=True):
            user.kwuserprofile = KWUserProfile.objects.create(user=user)
            user.save()
