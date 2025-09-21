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
        self.input_mode = "buttons"  # Control del modo de input
        self.message = None  # Referencia al mensaje del juego

    def set_message(self, message: discord.Message):
        """Establecer la referencia del mensaje para actualizaciones"""
        self.message = message

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "❌ No puedes controlar el juego de otro jugador!",
                ephemeral=True
            )
            return False
        return True

    # FILA 0: Botón UP centrado con decoraciones kawaii  
    @discord.ui.button(emoji='✨', style=discord.ButtonStyle.secondary, row=0)
    async def left_decoration(self, interaction: discord.Interaction, button: discord.ui.Button):
        kawaii_responses = [
            "✨ ¡Solo soy una estrellita decorativa! (◕‿◕)",
            "✨ ¡Brillo brillo! Pero no hago nada más ♪(´▽｀)",
            "✨ ¡Me gusta hacer bonito el Sokoban! ✨(｡◕‿◕｡)",
            "✨ ¡Wuiiiiiiiiiii! ♡"
        ]
        import random
        await interaction.response.send_message(random.choice(kawaii_responses), ephemeral=True)

    @discord.ui.button(emoji='⬆️', style=discord.ButtonStyle.primary, row=0)
    async def move_up(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_move(interaction, 'w')

    @discord.ui.button(emoji='✨', style=discord.ButtonStyle.secondary, row=0) 
    async def right_decoration(self, interaction: discord.Interaction, button: discord.ui.Button):
        kawaii_responses = [
            "✨ ¡Soy la otra estrellita decorativa! (｡◕‿◕｡)",
            "✨ ¡¡Wuiiiiiiiiiii! ♪",
            "✨ ¡Brillamos juntas para Sokoromi! ✨✨",
            "✨ ¡Soy la hermana gemela de la otra estrellita! ♡"
        ]
        import random
        await interaction.response.send_message(random.choice(kawaii_responses), ephemeral=True)

    # FILA 1: LEFT, DOWN, RIGHT en línea
    @discord.ui.button(emoji='⬅️', style=discord.ButtonStyle.primary, row=1)
    async def move_left(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_move(interaction, 'a')

    @discord.ui.button(emoji='⬇️', style=discord.ButtonStyle.primary, row=1)
    async def move_down(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_move(interaction, 's')

    @discord.ui.button(emoji='➡️', style=discord.ButtonStyle.primary, row=1)
    async def move_right(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_move(interaction, 'd')

    # FILA 2: Controles de juego
    @discord.ui.button(emoji='🔄', label='Reset', style=discord.ButtonStyle.secondary, row=2)
    async def reset(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_move(interaction, 'r')

    @discord.ui.button(emoji='🎲', label='Nuevo Mapa', style=discord.ButtonStyle.secondary, row=2)
    async def new_map(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_move(interaction, 'mr')

    # FILA 3: Controles de sesión y modo
    @discord.ui.button(emoji='⌨️', label='Modo Texto', style=discord.ButtonStyle.success, row=3)
    async def toggle_input_mode(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.input_mode == "buttons":
            self.input_mode = "text"
            button.label = "Modo Botones"
            button.emoji = "🖱️"
            button.style = discord.ButtonStyle.secondary
            await interaction.response.edit_message(view=self)
            await interaction.followup.send(
                "💬 **Modo texto activado**\nAhora usa `w`, `a`, `s`, `d` para moverte\nLos botones están desactivados temporalmente", 
                ephemeral=True
            )
        else:
            self.input_mode = "buttons" 
            button.label = "Modo Texto"
            button.emoji = "⌨️"
            button.style = discord.ButtonStyle.success
            await interaction.response.edit_message(view=self)
            await interaction.followup.send(
                "🖱️ **Modo botones activado**\nUsa las flechas para moverte\nLos comandos de texto están desactivados", 
                ephemeral=True
            )

    @discord.ui.button(emoji='🛑', label='Parar', style=discord.ButtonStyle.danger, row=3)
    async def stop_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_move(interaction, 'stop')

    async def handle_move(self, interaction: discord.Interaction, direction: str):
        # Verificar modo de input (excepto para controles especiales)
        if direction in ['w', 'a', 's', 'd'] and self.input_mode == "text":
            await interaction.response.send_message(
                "⌨️ Estás en modo texto. Usa los comandos `w`, `a`, `s`, `d` o cambia a modo botones.", 
                ephemeral=True
            )
            return
            
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

    async def update_from_text_command(self, result):
        """Actualizar el mensaje desde comandos de texto"""
        if not self.message:
            return
            
        try:
            if result['action'] == 'move':
                embed = await self.game_instance.create_game_embed()
                await self.message.edit(embed=embed, view=self)
                
            elif result['action'] == 'win':
                embed = await self.game_instance.create_win_embed()
                new_view = WinView(self.game_instance, self.user_id)
                await self.message.edit(embed=embed, view=new_view)
                
            elif result['action'] == 'stop':
                embed = discord.Embed(
                    title="🎮 Juego Terminado",
                    description="¡Juego terminado desde comando de texto!",
                    color=0x00ff00
                )
                await self.message.edit(embed=embed, view=None)
                
        except Exception as e:
            print(f"Error actualizando desde comando de texto: {e}")

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
        # Establecer la referencia del mensaje en el nuevo view
        view.set_message(interaction.message)
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
            view = GameView(game, user_id)
            
            embed = await game.create_game_embed()
            await interaction.response.send_message(embed=embed, view=view)
            
            # CRÍTICO: Obtener la referencia del mensaje y establecerla en el view
            message = await interaction.original_response()
            view.set_message(message)
            
            # Guardamos tanto el juego como el view
            self.active_games[user_id] = {'game': game, 'view': view, 'message': message}
            
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

    async def handle_text_input_from_message(self, message, direction):
        """Manejar comandos de texto desde el listener on_message"""
        user_id = message.author.id
        
        if user_id not in self.active_games:
            return False  # No hay juego activo
            
        try:
            game_data = self.active_games[user_id]
            game = game_data['game']
            view = game_data['view']
            
            # Verificar si está en modo texto
            if hasattr(view, 'input_mode') and view.input_mode != "text":
                # Eliminar mensaje pero no mostrar error (modo silencioso)
                try:
                    await message.delete()
                except discord.NotFound:
                    pass  # El mensaje ya fue eliminado
                except discord.Forbidden:
                    pass  # No tenemos permisos para eliminar
                except Exception:
                    pass  # Cualquier otro error
                return True  # Procesado (aunque no ejecutado)
            
            # PRIMERO: Eliminar el comando del usuario INMEDIATAMENTE
            delete_success = False
            try:
                await message.delete()
                delete_success = True
            except discord.NotFound:
                delete_success = True  # Ya fue eliminado
            except discord.Forbidden:
                # No tenemos permisos, enviar mensaje temporal
                await message.channel.send(
                    "⚠️ No tengo permisos para eliminar mensajes. Los comandos funcionarán pero quedarán visibles.",
                    delete_after=3
                )
            except Exception as e:
                print(f"Error eliminando mensaje: {e}")
            
            # SEGUNDO: Procesar el movimiento
            result = await game.handle_input(direction)
            
            # TERCERO: Actualizar la interfaz
            await view.update_from_text_command(result)
            
            return True  # Procesado exitosamente
                
        except Exception as e:
            # Si hay error, intentar eliminar el mensaje de todas formas
            try:
                await message.delete()
            except:
                pass
            
            # Enviar mensaje de error temporal
            try:
                await message.channel.send(f"❌ Error procesando comando: {e}", delete_after=5)
            except:
                pass
                
            return True  # Procesado (aunque con error)

    @commands.Cog.listener()
    async def on_message(self, message):
        # Filtros básicos
        if message.author.bot:
            return
        if not isinstance(message.channel, discord.TextChannel):
            return
            
        user_id = message.author.id
        if user_id not in self.active_games:
            return
            
        # Verificar si es un comando de juego
        content = message.content.lower().strip()
        if content in ['w', 'a', 's', 'd', 'r', 'mr']:
            # Procesar el comando y eliminarlo
            processed = await self.handle_text_input_from_message(message, content)
            # Si se procesó, no permitir que otros handlers lo vean
            if processed:
                return

async def setup(bot):
    await bot.add_cog(GameCommands(bot))
