# pylint: disable=no-member, line-too-long, import-error

import tempfile

import requests

from django.core.management.base import BaseCommand # pylint: disable=wrong-import-order
from django.utils import timezone

from ...models import IPAddressDatabase

COUNTRY_URL = 'https://github.com/iplocate/ip-address-databases/raw/refs/heads/main/ip-to-country/ip-to-country.mmdb'
ASN_URL = 'https://github.com/iplocate/ip-address-databases/raw/refs/heads/main/ip-to-asn/ip-to-asn.mmdb'

class Command(BaseCommand):
    help = 'Initializes / updates IPv4 databases with lists from IPLocate.io.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        country_database = IPAddressDatabase.objects.filter(identifier='iplocate_country').first()

        if country_database is None:
            country_database = IPAddressDatabase()
            country_database.name = 'IPLocate.io Country IP Database'
            country_database.identifier = 'iplocate_country'
            country_database.source = 'https://github.com/iplocate/ip-address-databases'
            country_database.added = timezone.now()
            country_database.updated = country_database.added
            country_database.active = True
            country_database.save()

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            with requests.get(COUNTRY_URL, timeout=120) as response:
                temp_file.write(response.content)
                temp_file.close()

                with open(temp_file.name, 'rb') as db_file:
                    country_database.file.save('IPLocate_Country.mmdb', db_file)
                    country_database.updated = timezone.now()
                    country_database.save()

        asin_database = IPAddressDatabase.objects.filter(identifier='iplocate_asin').first()

        if asin_database is None:
            asin_database = IPAddressDatabase()
            asin_database.name = 'IPLocate.io ASIN IP Database'
            asin_database.identifier = 'iplocate_asin'
            asin_database.source = 'https://github.com/iplocate/ip-address-databases'
            asin_database.added = timezone.now()
            asin_database.updated = asin_database.added
            asin_database.active = True
            asin_database.save()

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            with requests.get(ASN_URL, timeout=120) as response:
                temp_file.write(response.content)
                temp_file.close()

                with open(temp_file.name, 'rb') as db_file:
                    asin_database.file.save('IPLocate_ASIN.mmdb', db_file)
                    asin_database.updated = timezone.now()
                    asin_database.save()
