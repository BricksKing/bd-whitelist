import discord
from discord import app_commands
from discord.ext import commands

from ..models import AllowedGuild, WhitelistSettings


OWNER_ID = 1234567890 # Replace with your own user ID


class whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="whitelist",
        description="Enable or disable guild whitelist mode.",
    )
    @app_commands.describe(
        enabled="Set to true to enable whitelist mode, or false to disable it."
    )
    async def whitelist(
        self,
        interaction: discord.Interaction,
        enabled: bool,
    ):
        if interaction.user.id != OWNER_ID:
            return await interaction.response.send_message(
                "Only the bot owner can use this command.",
                ephemeral=True,
            )

        settings = await WhitelistSettings.get_settings()
        settings.enabled = enabled
        await settings.asave()

        status = "enabled" if enabled else "disabled"

        await interaction.response.send_message(
            f"Whitelist mode is now **{status}**.",
            ephemeral=True,
        )

        if enabled:
            await self.leave_unwhitelisted_guilds()

    async def is_guild_allowed(self, guild_id: int) -> bool:
        settings = await WhitelistSettings.get_settings()

        if not settings.enabled:
            return True

        return await AllowedGuild.objects.filter(guild_id=guild_id).aexists()

    async def leave_unwhitelisted_guilds(self):
        for guild in self.bot.guilds:
            allowed = await AllowedGuild.objects.filter(
                guild_id=guild.id
            ).aexists()

            if not allowed:
                await guild.leave()

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        allowed = await self.is_guild_allowed(guild.id)

        if not allowed:
            await guild.leave()

    async def bot_check(self, ctx: commands.Context) -> bool:
        if ctx.guild is None:
            return True

        if ctx.author.id == OWNER_ID:
            return True

        allowed = await self.is_guild_allowed(ctx.guild.id)

        if not allowed:
            await ctx.reply(
                "This bot is not enabled in this server.",
                mention_author=False,
            )

            await ctx.guild.leave()
            return False

        return True


async def setup(bot):
    await bot.add_cog(whitelist(bot))
