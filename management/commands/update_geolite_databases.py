# pylint: disable=no-member, line-too-long, import-error, wrong-import-order

import tempfile

import requests

from django.core.management.base import BaseCommand # pylint: disable=wrong-import-order
from django.utils import timezone

from ...models import IPAddressDatabase

COUNTRY_URL = 'https://git.io/GeoLite2-Country.mmdb'
ASN_URL = 'https://git.io/GeoLite2-ASN.mmdb'
CITY_URL = 'https://git.io/GeoLite2-City.mmdb'

class Command(BaseCommand):
    help = 'Initializes / updates IPv4 databases with lists from MaxMind\'s GeoLite2 databases.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options): # pylint: disable=too-many-statements
        country_database = IPAddressDatabase.objects.filter(identifier='geolite2_country').first()

        if country_database is None:
            country_database = IPAddressDatabase()
            country_database.name = 'GeoLite2 Country IP Database'
            country_database.identifier = 'geolite2_country'
            country_database.source = 'https://github.com/P3TERX/GeoLite.mmdb'
            country_database.added = timezone.now()
            country_database.updated = country_database.added
            country_database.active = True
            country_database.save()

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            with requests.get(COUNTRY_URL, timeout=120) as response:
                temp_file.write(response.content)
                temp_file.close()

                with open(temp_file.name, 'rb') as db_file:
                    country_database.file.save('GeoLite2_Country.mmdb', db_file)
                    country_database.updated = timezone.now()
                    country_database.save()

        asin_database = IPAddressDatabase.objects.filter(identifier='geolite2_asin').first()

        if asin_database is None:
            asin_database = IPAddressDatabase()
            asin_database.name = 'GeoLite2 ASIN IP Database'
            asin_database.identifier = 'geolite2_asin'
            asin_database.source = 'https://github.com/P3TERX/GeoLite.mmdb'
            asin_database.added = timezone.now()
            asin_database.updated = asin_database.added
            asin_database.active = True
            asin_database.save()

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            with requests.get(ASN_URL, timeout=120) as response:
                temp_file.write(response.content)
                temp_file.close()

                with open(temp_file.name, 'rb') as db_file:
                    asin_database.file.save('GeoLite2_ASIN.mmdb', db_file)
                    asin_database.updated = timezone.now()
                    asin_database.save()

        city_database = IPAddressDatabase.objects.filter(identifier='geolite2_city').first()

        if city_database is None:
            city_database = IPAddressDatabase()
            city_database.name = 'GeoLite2 City IP Database'
            city_database.identifier = 'geolite2_city'
            city_database.source = 'https://github.com/P3TERX/GeoLite.mmdb'
            city_database.added = timezone.now()
            city_database.updated = city_database.added
            city_database.active = True
            city_database.save()

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            with requests.get(CITY_URL, timeout=120) as response:
                temp_file.write(response.content)
                temp_file.close()

                with open(temp_file.name, 'rb') as db_file:
                    city_database.file.save('GeoLite2_City.mmdb', db_file)
                    city_database.updated = timezone.now()
                    city_database.save()
