from django.db import models



class WhitelistSettings(models.Model):
    enabled = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    async def get_settings(cls):
        settings, _ = await cls.objects.aget_or_create(id=1)
        return settings

    def __str__(self):
        return "Whitelist enabled" if self.enabled else "Whitelist disabled"


class AllowedGuild(models.Model):
    guild_id = models.BigIntegerField(unique=True,help_text="Set the guild id of what you want to be whitelisted")
    guild_name = models.CharField(max_length=100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    enabled = models.BooleanField(default=True, help_text="if true, the guild will not be kicked out")


    def __str__(self):
        return f"{self.guild_name or 'Unknown Guild'} ({self.guild_id})"
