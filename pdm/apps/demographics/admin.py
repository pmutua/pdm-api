from django.contrib import admin
from .models import (
    District,
    County,
    SubCounty,
    Parish,
    Village
)

admin.site.register(District)
admin.site.register(County)
admin.site.register(SubCounty)
admin.site.register(Parish)
admin.site.register(Village)

