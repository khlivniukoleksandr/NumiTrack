from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from items.models import Collector, Banknote, Coin


@admin.register(Collector)
class CollectorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("bio", "avatar_preview",)
    fieldsets = UserAdmin.fieldsets + (("Additional info", {"fields": ("bio", "avatar",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("first_name", "last_name", "bio", "avatar",)}),)
    readonly_fields = ("avatar_preview",)

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="40" style="border-radius:50%;" />', obj.avatar.url)
        return "(No image)"
    avatar_preview.short_description = "Avatar"


admin.site.register(Coin)
admin.site.register(Banknote)