# pylint: disable=no-member

import pytz

from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone

from .models import IPAddressDatabase

def ip_info(request):
    fields = request.GET.get('fields', request.POST.get('fields', None))

    here_tz = pytz.timezone(settings.TIME_ZONE)

    payload = {
        'date': timezone.now().astimezone(here_tz).isoformat()
    }

    requester = request.GET.get('ip', request.POST.get('ip', None))

    if requester is not None:
        payload['via'] = 'Request GET or POST parameter'
    else:
        requester = request.META.get('HTTP_X_FORWARDED_FOR', None)

        if requester is not None:
            payload['via'] = 'X-Forwarded-For header'

            chain = requester.split(',')

            requester = chain[0].strip()
        else:
            payload['via'] = 'Django remote address'

            requester = request.META.get('REMOTE_ADDR', None)

    payload['requester'] = requester

    for database in IPAddressDatabase.objects.filter(active=True):
        db_payload = {}

        for key, value in database.fetch_details(requester).items():
            if fields is None or (key in fields):
                db_payload[key] = value

        payload[database.identifier] = db_payload

    return JsonResponse(payload)
