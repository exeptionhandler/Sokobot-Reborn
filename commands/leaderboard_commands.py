import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional


class LeaderboardCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="leaderboard",
        description="Mostrar la clasificación global"
    )
    @app_commands.describe(
        tipo="Tipo de orden: nivel, puntuacion, promedio, partidas",
        limite="Cantidad de jugadores a mostrar (máximo 20)"
    )
    @app_commands.allowed_installs(guilds=True, users=True)  # ← AGREGAR: Permite instalación en usuarios
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)  # ← AGREGAR: Permite uso en DMs
    async def leaderboard(self, interaction: discord.Interaction, tipo: Optional[str] = "nivel", limite: Optional[int] = 10):
        sort_options = {
            "nivel": "best_level",
            "puntuacion": "total_score",
            "promedio": "average_score",
            "partidas": "total_games"
        }
        tipo = tipo.lower()
        sort_by = sort_options.get(tipo, "best_level")
        limite = max(1, min(limite, 20))

        try:
            embed = await self.bot.leaderboard.create_leaderboard_embed(sort_by, limite)
            
            # Agregar contexto al footer según dónde se usa
            if interaction.guild is None:
                embed.set_footer(text="📱 Leaderboard global • Vista desde DM")
            else:
                embed.set_footer(text=f"📊 Leaderboard global • Vista desde {interaction.guild.name}")
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            # Manejo de errores mejorado
            error_embed = discord.Embed(
                title="❌ Error del Leaderboard",
                description="No se pudo cargar la clasificación. Intenta de nuevo en unos momentos.",
                color=0xff0000
            )
            
            if interaction.guild is None:
                error_embed.set_footer(text="📱 Error en DM • Contacta al desarrollador si persiste")
            else:
                error_embed.set_footer(text=f"❌ Error en {interaction.guild.name}")
                
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            print(f"Error en leaderboard: {e}")

async def setup(bot):
    await bot.add_cog(LeaderboardCommands(bot))
