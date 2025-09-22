import time
import logging
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
        self.logger = logging.getLogger(__name__)  # ← AGREGAR: Logger para ping command

    @app_commands.command(name="info", description="Información sobre Sokoromi y cómo jugar")
    @app_commands.allowed_installs(guilds=True, users=True)  # ← AGREGAR: User App support
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)  # ← AGREGAR: DM support
    async def info_slash(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 Sokoromi - Bot de Sokoban Kawaii",  # ← CAMBIAR: Nombre actualizado
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
            value="✅ **Niveles Infinitos** - Mapas generados aleatoriamente\n✅ **Controles Duales** - Botones interactivos y comandos de texto\n✅ **Sistema de Puntuación** - Compite en el leaderboard global\n✅ **Estadísticas Detalladas** - Rastrea tu progreso\n✅ **User App** - Disponible en cualquier lugar",  # ← ACTUALIZAR: Nueva característica
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
        
        # ← AGREGAR: Info específica del contexto
        if interaction.guild is None:
            embed.add_field(
                name="📱 Jugando en DM",
                value="¡Perfecto! Puedes jugar Sokoromi privadamente\nTambién funciona en cualquier servidor donde estés\n¡Instálame como User App para máxima portabilidad!",
                inline=False
            )
            embed.set_footer(
                text="✨ Sokoromi instalado como User App - ¡Disponible en todas partes!",
                icon_url=self.bot.user.display_avatar.url
            )
        else:
            embed.add_field(
                name="🏰 Jugando en servidor",
                value=f"Estás en: **{interaction.guild.name}**\n¡También puedes jugar en DM conmigo!\nPuedes instalarme como User App para jugar en cualquier lugar",
                inline=False
            )
            embed.set_footer(
                text=f"🎮 Sokoromi en {interaction.guild.name} • ¡Creado con ❤️ por @fabb!",
                icon_url=self.bot.user.display_avatar.url
            )
        
        embed.add_field(
            name="🏆 Sistema de Puntuación",
            value="• Más puntos por completar niveles rápido\n• Menos movimientos = más puntos\n• Compite en el leaderboard global\n• Estadísticas detalladas de progreso",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="ping", description="Muestra la latencia del bot y estado de conexión")
    @app_commands.allowed_installs(guilds=True, users=True)  # ← AGREGAR: User App support
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)  # ← AGREGAR: DM support
    async def ping(self, interaction: discord.Interaction):
        try:
            # Medir latencia de la API
            start_time = time.time()
            await interaction.response.defer()
            api_latency = (time.time() - start_time) * 1000
            
            # Latencia del websocket
            websocket_latency = self.bot.latency * 1000
            
            # Determinar el estado basado en la latencia
            if websocket_latency < 100:
                status_emoji = "💚"
                status_text = "Excelente"
                color = 0x00ff00
            elif websocket_latency < 200:
                status_emoji = "💛" 
                status_text = "Buena"
                color = 0xffff00
            elif websocket_latency < 500:
                status_emoji = "🧡"
                status_text = "Regular"
                color = 0xff8800
            else:
                status_emoji = "❤️"
                status_text = "Lenta"
                color = 0xff0000
            
            # Crear embed kawaii
            embed = discord.Embed(
                title="🏓 Pong! ✨",
                description=f"Estado de conexión: **{status_text}** {status_emoji}",
                color=color,
                timestamp=discord.utils.utcnow()
            )
            
            embed.add_field(
                name="🌐 Latencia WebSocket", 
                value=f"`{websocket_latency:.0f}ms`", 
                inline=True
            )
            
            embed.add_field(
                name="📡 Latencia API", 
                value=f"`{api_latency:.0f}ms`", 
                inline=True
            )
            
            embed.add_field(
                name="📊 Estado General", 
                value=f"{status_text} {status_emoji}", 
                inline=True
            )
            
            # Información adicional del bot
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
            
            embed.add_field(
                name="🎯 Juegos Activos", 
                value=f"`{len(getattr(self.bot.get_cog('GameCommands'), 'active_games', {}))}`", 
                inline=True
            )

            # ← MODIFICAR: Footer contextual kawaii
            if interaction.guild is None:
                embed.set_footer(
                    text="📱 Ping desde DM • Sokoromi está contigo en todas partes! (◕‿◕)", 
                    icon_url=self.bot.user.display_avatar.url
                )
            else:
                embed.set_footer(
                    text=f"🎮 Ping desde {interaction.guild.name} • Funcionando perfectamente! (◕‿◕)", 
                    icon_url=self.bot.user.display_avatar.url
                )
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            self.logger.error(f"Error in ping command: {e}")
            
            # ← AGREGAR: Manejo de error contextual
            error_msg = "❌ Error obteniendo información del ping. Intenta de nuevo."
            if interaction.guild is None:
                error_msg += "\n📱 Si el error persiste en DM, contacta al desarrollador."
            
            await interaction.followup.send(error_msg, ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        
        # ← MODIFICAR: Soporte para DMs también
        if not isinstance(message.channel, (discord.TextChannel, discord.DMChannel)):
            return
            
        if self.bot.user in message.mentions:
            embed = discord.Embed(
                title=f"¡Hola {message.author.display_name}, soy {self.bot.user.name}! ✨",
                description="Usa `/play` para comenzar una partida de Sokoban.\nUsa `/info` para más información y ayuda.",
                color=0x3498db
            )
            
            # ← AGREGAR: Mensaje contextual
            if isinstance(message.channel, discord.DMChannel):
                embed.add_field(
                    name="📱 Estás en DM",
                    value="¡Perfecto! Todos mis comandos funcionan aquí también.\n¡Gracias por instalarme como User App!",
                    inline=False
                )
                embed.set_footer(text="✨ User App • Disponible en cualquier lugar")
            else:
                embed.add_field(
                    name="🎮 Comandos disponibles",
                    value="También puedes usarme en DM instalándome como User App",
                    inline=False
                )
                embed.set_footer(text="También puedes usar los comandos slash directamente.")
            
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            
            await message.channel.send(embed=embed)
            
            try:
                await message.delete()
            except:
                pass  # No hay permisos o el mensaje ya fue eliminado

async def setup(bot):
    await bot.add_cog(InfoCommands(bot))