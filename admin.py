from django.contrib import admin

from .models import IPAddressDatabase

def activate(modeladmin, request, queryset): # pylint: disable=unused-argument, no-self-use
    queryset.update(active=True)

activate.short_description = 'Activate selected IP address databases'

def deactivate(modeladmin, request, queryset): # pylint: disable=unused-argument, no-self-use
    queryset.update(active=False)

deactivate.short_description = 'Deactivate selected IP address databases'

@admin.register(IPAddressDatabase)
class IPAddressDatabaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier', 'active', 'updated')
    search_fields = ('name', 'identifier', 'source',)
    list_filter = ('active', 'updated', 'added', 'identifier',)

    actions = [activate, deactivate]
