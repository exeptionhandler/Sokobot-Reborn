import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

class LeaderboardView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
        self.current_sort = 'best_level'

    @discord.ui.select(
        placeholder="Elegir tipo de clasificación...",
        options=[
            discord.SelectOption(label="Mejor Nivel", value="best_level", description="Ordenar por el nivel más alto alcanzado", emoji="🏔️"),
            discord.SelectOption(label="Puntuación Total", value="total_score", description="Ordenar por puntuación total acumulada", emoji="📈"),
            discord.SelectOption(label="Puntuación Promedio", value="average_score", description="Ordenar por puntuación promedio por partida", emoji="⭐"),
            discord.SelectOption(label="Partidas Jugadas", value="total_games", description="Ordenar por número de partidas jugadas", emoji="🎮")
        ]
    )
    async def sort_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.current_sort = select.values[0]
        embed = await self.bot.leaderboard.create_leaderboard_embed(self.current_sort)
        await interaction.response.edit_message(embed=embed, view=self)

class InfoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="info", description="Información sobre Sokobot y cómo jugar")
    async def info_slash(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 Sokobot Python",
            description="Bot de Discord para jugar Sokoban, el clásico juego de rompecabezas de empujar cajas.",
            color=0x3498db
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.add_field(
            name="🎯 Cómo Jugar",
            value="Eres un **Sokoban** 😎\nTu trabajo es empujar **cajas** 📦 hacia su **destino** ❌.\n¡Completa todos los niveles que puedas!",
            inline=False
        )
        embed.add_field(
            name="🎮 Características",
            value="✅ **Niveles Infinitos** - Mapas generados aleatoriamente\n✅ **Controles Duales** - Botones interactivos y comandos de texto\n✅ **Sistema de Puntuación** - Compite en el leaderboard global\n✅ **Estadísticas Detalladas** - Rastrea tu progreso\n✅ **Juegos Simultáneos** - Varios jugadores a la vez",
            inline=False
        )
        embed.add_field(
            name="⚡ Comandos Principales",
            value="`/play` - Iniciar nueva partida\n`/stop` - Terminar partida actual\n`/stats` - Ver tus estadísticas\n`/leaderboard` - Ver clasificación global\n`/info` - Mostrar esta información",
            inline=True
        )
        embed.add_field(
            name="🕹️ Controles en Juego",
            value="**Botones:** Usa los botones debajo del juego\n**Texto:** Escribe `w`, `a`, `s`, `d` para moverte\n`r` - Reiniciar nivel\n`mr` - Generar nuevo mapa",
            inline=True
        )
        embed.add_field(
            name="🏆 Sistema de Puntuación",
            value="• Más puntos por completar niveles rápido\n• Menos movimientos = más puntos\n• Compite en el leaderboard global\n• Estadísticas detalladas de progreso",
            inline=False
        )
        embed.set_footer(text="¡Creado con ❤️ para la comunidad de Discord!")
        await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if self.bot.user in message.mentions:
            embed = discord.Embed(
                title=f"Hola {message.author.display_name}, soy {self.bot.user.name}!",
                description="Usa `/play` para comenzar una partida de Sokoban.\nUsa `/info` para más información y ayuda.",
                color=0x3498db
            )
            embed.set_footer(text="También puedes usar los comandos slash directamente.")
            await message.channel.send(embed=embed)
            try:
                await message.delete()
            except:
                pass

async def setup(bot):
    await bot.add_cog(InfoCommands(bot))
