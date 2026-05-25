from django.contrib import admin

from .models import IPAddressDatabase

@admin.register(IPAddressDatabase)
class IPAddressDatabaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier', 'active', 'updated')
    search_fields = ('name', 'identifier', 'source',)
    list_filter = ('active', 'updated', 'added', 'identifier',)

    actions = ['activate', 'deactivate']

    @admin.action(description='Activate selected databases')
    def activate(self, request, queryset): # pylint: disable=unused-argument
        queryset.update(active=True)

    @admin.action(description='Deactivate selected databases')
    def deactivate(self, request, queryset): # pylint: disable=unused-argument
        queryset.update(active=False)
