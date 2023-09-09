from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    fields = (
        "uuid",
        "username",
        "password",
    )
    readonly_fields = (
        "uuid",
    )
