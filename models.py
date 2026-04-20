# pylint: disable=no-member, line-too-long
# -*- coding: utf-8 -*-

import socket

import maxminddb

from django.db import models

class IPAddressDatabase(models.Model):
    class Meta: # pylint: disable=too-few-public-methods, old-style-class, no-init
        verbose_name = 'IP address database'
        verbose_name_plural = 'IP address databases'

    name = models.CharField(max_length=1024, unique=True)
    identifier = models.SlugField(max_length=1024)
    source = models.URLField(max_length=1024, null=True, blank=True)

    file = models.FileField(upload_to='sft_ip_address_databases', null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField()

    active = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % self.name

    def fetch_details(self, ip_address):
        details = {}

        ip_address = socket.gethostbyname(ip_address)

        details['ip-address'] = ip_address

        print('PATH: %s' % self.file.path)
        print('ip_address: %s' % ip_address)

        with maxminddb.open_database(self.file.path) as reader:
            print('READER: %s' % reader)

            lookup = reader.get(ip_address)

            if lookup is not None:
                details.update(lookup)

        return details
