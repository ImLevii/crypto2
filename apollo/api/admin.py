from django.contrib import admin

from apollo.api.models import StoreTransaction, StoreVariables

admin.site.register(StoreTransaction)
admin.site.register(StoreVariables)
