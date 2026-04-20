from django.contrib import admin

from .models import IPAddressDatabase

@admin.register(IPAddressDatabase)
class IPAddressDatabaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier', 'active', 'updated')
    search_fields = ('name', 'identifier', 'source',)
    list_filter = ('active', 'updated', 'added', 'identifier',)
