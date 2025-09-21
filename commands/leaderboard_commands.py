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

        embed = await self.bot.leaderboard.create_leaderboard_embed(sort_by, limite)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(LeaderboardCommands(bot))

