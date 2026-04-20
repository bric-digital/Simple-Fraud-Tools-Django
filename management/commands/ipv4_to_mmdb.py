# pylint: disable=no-member, line-too-long, import-error

from mmdb_writer import MMDBWriter
from netaddr import IPSet

from django.core.management.base import BaseCommand # pylint: disable=wrong-import-order

class Command(BaseCommand):
    help = 'Converts an ipv4 text files to a mmdb file.'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('datacenter_list', type=str)
        parser.add_argument('vpn_list', type=str)
        parser.add_argument('destination', type=str)

    def handle(self, *args, **options):
        print('args: %s' % options)

        writer = MMDBWriter()

        for i in range(0, 256):
            writer.insert_network(IPSet(['%s.0.0.0/8' % i]), {'endpoint_type': 'Unknown'}) # Unknown by default...

        with open(options['datacenter_list'], encoding='utf-8') as ip_txt:
            for line in ip_txt:
                line = line.strip()

                if len(line) > 0: # pylint: disable=len-as-condition
                    writer.insert_network(IPSet([line]), {'endpoint_type': 'Datacenter'})

        with open(options['vpn_list'], encoding='utf-8') as ip_txt:
            for line in ip_txt:
                line = line.strip()

                if len(line) > 0: # pylint: disable=len-as-condition
                    writer.insert_network(IPSet([line]), {'endpoint_type': 'VPN'})

        writer.to_db_file(options['destination'])
