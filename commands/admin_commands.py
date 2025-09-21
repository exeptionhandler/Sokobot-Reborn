import discord
from discord.ext import commands
from discord import app_commands

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        print("Admin Commands cog cargado")

        self.bot = bot

    @app_commands.command(name="prefix", description="Cambiar el prefijo del bot en este servidor")
    @app_commands.describe(nuevo_prefijo="Nuevo prefijo (1 a 5 caracteres)")
    @app_commands.default_permissions(administrator=True)
    async def prefix_slash(self, interaction: discord.Interaction, nuevo_prefijo: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Solo los administradores pueden cambiar el prefijo.", ephemeral=True)
            return
        if len(nuevo_prefijo) < 1 or len(nuevo_prefijo) > 5:
            await interaction.response.send_message("❌ El prefijo debe tener entre 1 y 5 caracteres.", ephemeral=True)
            return
        forbidden_chars = ['@', '#', ':', '`', '\\', '/', ' ']
        if any(char in forbidden_chars for char in nuevo_prefijo):
            await interaction.response.send_message(f"❌ El prefijo contiene caracteres no permitidos: {forbidden_chars}", ephemeral=True)
            return
        try:
            await self.bot.db.set_guild_prefix(interaction.guild.id, nuevo_prefijo)
            self.bot.prefixes[interaction.guild.id] = nuevo_prefijo
            embed = discord.Embed(title="✅ Prefijo Actualizado", description=f"El prefijo del servidor ha sido cambiado a: `{nuevo_prefijo}`", color=0x00ff00)
            embed.add_field(name="💡 Nota", value="Los comandos slash (/) seguirán funcionando normalmente.", inline=False)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error cambiando el prefijo: {e}", ephemeral=True)

    @app_commands.command(name="reset-prefix", description="Restaurar el prefijo por defecto (!)")
    @app_commands.default_permissions(administrator=True)
    async def reset_prefix_slash(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Solo los administradores pueden cambiar el prefijo.", ephemeral=True)
            return
        try:
            await self.bot.db.set_guild_prefix(interaction.guild.id, '!')
            self.bot.prefixes[interaction.guild.id] = '!'
            embed = discord.Embed(title="🔄 Prefijo Restaurado", description="El prefijo del servidor ha sido restaurado a: `!`", color=0x3498db)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error restaurando el prefijo: {e}", ephemeral=True)
    


async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
