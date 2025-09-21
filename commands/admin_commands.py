import discord
import time
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
            
    @app_commands.command(name="ping", description="Muestra la latencia del bot y estado de conexión")
    async def ping(self, interaction: discord.Interaction):
        # Medir latencia de la API
        start_time = time.time()
        await interaction.response.defer()
        api_latency = (time.time() - start_time) * 1000
        
        # Latencia del websocket
        websocket_latency = self.bot.latency * 1000
        
        # Crear embed kawaii
        embed = discord.Embed(
            title="🏓 Pong! ✨",
            color=0xFF69B4,  # Rosa kawaii
            timestamp=discord.utils.utcnow()
        )
        
        # Determinar el estado basado en la latencia
        if websocket_latency < 100:
            status_emoji = "💚"
            status_text = "Excelente"
        elif websocket_latency < 200:
            status_emoji = "💛" 
            status_text = "Buena"
        elif websocket_latency < 500:
            status_emoji = "🧡"
            status_text = "Regular" 
        else:
            status_emoji = "❤️"
            status_text = "Lenta"
        
        embed.add_field(
            name="🌐 Latencia WebSocket", 
            value=f"`{websocket_latency:.0f}ms` {status_emoji}", 
            inline=True
        )
        
        embed.add_field(
            name="📡 Latencia API", 
            value=f"`{api_latency:.0f}ms`", 
            inline=True
        )
        
        embed.add_field(
            name="📊 Estado", 
            value=f"{status_text}", 
            inline=True
        )
        
        # Agregar al embed información adicional
        embed.add_field(
            name="🎮 Servidores", 
            value=f"`{len(self.bot.guilds)}`", 
            inline=True
        )

        embed.add_field(
            name="👥 Usuarios", 
            value=f"`{len(self.bot.users)}`", 
            inline=True
        )

        # Información adicional kawaii
        embed.set_footer(
            text="Sokoromi está funcionando perfectamente! (◕‿◕)", 
            icon_url=self.bot.user.display_avatar.url
        )
        
        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
