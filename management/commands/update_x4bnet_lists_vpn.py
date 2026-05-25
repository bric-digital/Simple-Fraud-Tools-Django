# pylint: disable=no-member, line-too-long, import-error, wrong-import-order

import tempfile

import requests

from mmdb_writer import MMDBWriter
from netaddr import IPSet

from django.core.management.base import BaseCommand # pylint: disable=wrong-import-order
from django.utils import timezone

from ...models import IPAddressDatabase

DATABASE_URL = 'https://raw.githubusercontent.com/X4BNet/lists_vpn/refs/heads/main/output/datacenter/ipv4.txt'
VPN_URL = 'https://raw.githubusercontent.com/X4BNet/lists_vpn/refs/heads/main/output/vpn/ipv4.txt'

class Command(BaseCommand):
    help = 'Initializes / updates IPv4 database with lists from X4BNet/lists_vpn.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        writer = MMDBWriter()

        for i in range(0, 256):
            writer.insert_network(IPSet(['%s.0.0.0/8' % i]), {'endpoint_type': 'Unknown'}) # Unknown by default...

        with requests.get(DATABASE_URL, timeout=120) as response:
            for line in response.text.splitlines():
                line = line.strip()

                if len(line) > 0: # pylint: disable=len-as-condition
                    writer.insert_network(IPSet([line]), {'endpoint_type': 'Datacenter'})

        with requests.get(VPN_URL, timeout=120) as response:
            for line in response.text.splitlines():
                line = line.strip()

                if len(line) > 0: # pylint: disable=len-as-condition
                    writer.insert_network(IPSet([line]), {'endpoint_type': 'VPN'})

        database = IPAddressDatabase.objects.filter(identifier='x4bnet').first()

        if database is None:
            database = IPAddressDatabase()
            database.name = 'X4BNet/lists_vpn List'
            database.identifier = 'x4bnet'
            database.source = 'https://github.com/X4BNet/lists_vpn'
            database.added = timezone.now()
            database.updated = database.added
            database.active = True
            database.save()

        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file.close()

            writer.to_db_file(temp_file.name)

            with open(temp_file.name, 'rb') as db_file:
                database.file.save('X4BNet_lists_vpn.mmdb', db_file)
                database.updated = timezone.now()
                database.save()
