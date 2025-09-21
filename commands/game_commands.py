import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from typing import Optional

from game.sokoban_game import SokobanGame
from utils.game_utils import GameUtils

class GameView(discord.ui.View):
    def __init__(self, game_instance, user_id):
        print("Game Commands cog cargado")
        super().__init__(timeout=300)
        self.game_instance = game_instance
        self.user_id = user_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "❌ No puedes controlar el juego de otro jugador!",
                ephemeral=True
            )
            return False
        return True

    @discord.ui.button(label='↑', style=discord.ButtonStyle.primary, row=0)
    async def move_up(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_move(interaction, 'w')

    @discord.ui.button(label='←', style=discord.ButtonStyle.primary, row=1)
    async def move_left(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_move(interaction, 'a')

    @discord.ui.button(label='🔄', style=discord.ButtonStyle.secondary, row=1)
    async def reset(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_move(interaction, 'r')

    @discord.ui.button(label='→', style=discord.ButtonStyle.primary, row=1)
    async def move_right(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_move(interaction, 'd')

    @discord.ui.button(label='↓', style=discord.ButtonStyle.primary, row=2)
    async def move_down(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_move(interaction, 's')

    @discord.ui.button(label='🛑 Parar', style=discord.ButtonStyle.danger, row=3)
    async def stop_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_move(interaction, 'stop')

    @discord.ui.button(label='🎲 Nuevo Mapa', style=discord.ButtonStyle.secondary, row=3)
    async def new_map(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_move(interaction, 'mr')

    async def handle_move(self, interaction: discord.Interaction, direction: str):
        try:
            result = await self.game_instance.handle_input(direction)

            if result['action'] == 'move':
                embed = await self.game_instance.create_game_embed()
                await interaction.response.edit_message(embed=embed, view=self)

            elif result['action'] == 'win':
                embed = await self.game_instance.create_win_embed()
                new_view = WinView(self.game_instance, self.user_id)
                await interaction.response.edit_message(embed=embed, view=new_view)

            elif result['action'] == 'stop':
                embed = discord.Embed(
                    title="🎮 Juego Terminado",
                    description=f"¡Gracias por jugar, {interaction.user.mention}!",
                    color=0x00ff00
                )
                await interaction.response.edit_message(embed=embed, view=None)

        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error procesando movimiento: {e}",
                ephemeral=True
            )

class WinView(discord.ui.View):
    def __init__(self, game_instance, user_id):
        super().__init__(timeout=60)
        self.game_instance = game_instance
        self.user_id = user_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "❌ No puedes controlar el juego de otro jugador!",
                ephemeral=True
            )
            return False
        return True

    @discord.ui.button(label='➡️ Continuar', style=discord.ButtonStyle.green)
    async def continue_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.game_instance.next_level()
        embed = await self.game_instance.create_game_embed()
        view = GameView(self.game_instance, self.user_id)
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label='🛑 Parar', style=discord.ButtonStyle.red)
    async def stop_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🎮 Juego Terminado",
            description=f"¡Gracias por jugar, {interaction.user.mention}!",
            color=0x00ff00
        )
        await interaction.response.edit_message(embed=embed, view=None)

class GameCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}

    @app_commands.command(name="play", description="Iniciar una nueva partida de Sokoban")
    @app_commands.describe(emoji="Emoji personalizado para tu personaje (opcional)")
    async def play_slash(self, interaction: discord.Interaction, emoji: Optional[str] = None):
        user_id = interaction.user.id
        if user_id in self.active_games:
            await interaction.response.send_message(
                "❌ Ya tienes un juego activo. Usa `/stop` para terminarlo primero.",
                ephemeral=True
            )
            return
        try:
            user = interaction.user if isinstance(interaction.user, discord.User) else await interaction.client.fetch_user(interaction.user.id)
            game = SokobanGame(user, self.bot.leaderboard, emoji)
            self.active_games[user_id] = game
            embed = await game.create_game_embed()
            view = GameView(game, user_id)
            await interaction.response.send_message(embed=embed, view=view)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error iniciando el juego: {e}", ephemeral=True)

    @app_commands.command(name="stop", description="Terminar tu partida actual de Sokoban")
    async def stop_slash(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        if user_id not in self.active_games:
            await interaction.response.send_message("❌ No tienes un juego activo.", ephemeral=True)
            return
        del self.active_games[user_id]
        embed = discord.Embed(
            title="🎮 Juego Terminado",
            description=f"¡Gracias por jugar, {interaction.user.mention}!",
            color=0x00ff00
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="stats", description="Ver tus estadísticas de Sokoban")
    async def stats_slash(self, interaction: discord.Interaction):
        try:
            stats = await self.bot.leaderboard.get_player_stats(interaction.user.id)
            embed = discord.Embed(
                title=f"📊 Estadísticas de {interaction.user.display_name}",
                color=0x3498db
            )
            if stats:
                embed.add_field(name="🏆 Mejor Nivel", value=stats['best_level'], inline=True)
                embed.add_field(name="🎮 Partidas Jugadas", value=stats['total_games'], inline=True)
                embed.add_field(name="⏱️ Tiempo Total", value=f"{stats['total_time']:.1f} s", inline=True)
                embed.add_field(name="📈 Puntuación Total", value=stats['total_score'], inline=True)
            else:
                embed.description = "No tienes estadísticas aún. ¡Juega tu primera partida!"
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error obteniendo estadísticas: {e}", ephemeral=True)

    @commands.command(name="w", aliases=["arriba"])
    async def move_up_text(self, ctx):
        await self.handle_text_input(ctx, 'w')

    @commands.command(name="s", aliases=["abajo"])
    async def move_down_text(self, ctx):
        await self.handle_text_input(ctx, 's')

    @commands.command(name="a", aliases=["izquierda"])
    async def move_left_text(self, ctx):
        await self.handle_text_input(ctx, 'a')

    @commands.command(name="d", aliases=["derecha"])
    async def move_right_text(self, ctx):
        await self.handle_text_input(ctx, 'd')

    @commands.command(name="r")
    async def reset_text(self, ctx):
        await self.handle_text_input(ctx, 'r')

    @commands.command(name="mr")
    async def new_map_text(self, ctx):
        await self.handle_text_input(ctx, 'mr')

    async def handle_text_input(self, ctx, direction):
        user_id = ctx.author.id
        if user_id not in self.active_games:
            return
        try:
            game = self.active_games[user_id]
            result = await game.handle_input(direction)
            try:
                await ctx.message.delete()
            except:
                pass
        except Exception as e:
            await ctx.send(f"❌ Error: {e}", delete_after=5)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not isinstance(message.channel, discord.TextChannel):
            return
        user_id = message.author.id
        if user_id not in self.active_games:
            return
        content = message.content.lower().strip()
        if content in ['w', 'a', 's', 'd', 'r', 'mr']:
            ctx = await self.bot.get_context(message)
            await self.handle_text_input(ctx, content)

async def setup(bot):
    await bot.add_cog(GameCommands(bot))
