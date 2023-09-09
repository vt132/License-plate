from django.contrib import admin
from .models import Plate


@admin.register(Plate)
class PlateAdmin(admin.ModelAdmin):
    fields = (
        "number",
        "wanted",
    )
