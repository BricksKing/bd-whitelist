from django.contrib import admin
from .models import AllowedGuild, WhitelistSettings

@admin.register(AllowedGuild)
class AllowedGuildAdmin(admin.ModelAdmin):
    list_display = ("guild_id", "guild_name", "created_at",)
    list_filter = ("enabled",)
    search_fields = ("guild_name",)


@admin.register(WhitelistSettings)
class WhitelistSettingsAdmin(admin.ModelAdmin):
    list_display = ("enabled", "updated_at",)
    readonly_fields = ("updated_at",)

    def has_add_permission(self, request):
        return not WhitelistSettings.objects.exists()
