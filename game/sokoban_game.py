import discord
import time
from typing import Dict, Any, Optional

from .grid import Grid

class SokobanGame:
    def __init__(self, user: discord.User, leaderboard, player_emoji: Optional[str] = None):
        self.user = user
        self.leaderboard = leaderboard
        self.player_emoji = player_emoji or "😎"

        self.level = 1
        self.width = 9
        self.height = 6
        self.game_active = True
        self.last_action = time.time()
        self.start_time = time.time()
        self.moves_count = 0

        self.grid = Grid(self.width, self.height, self.level, self.player_emoji)

    async def handle_input(self, user_input: str) -> Dict[str, Any]:
        self.last_action = time.time()
        if user_input == "stop":
            await self.end_game()
            return {"action": "stop"}
        if not self.game_active:
            return {"action": "inactive"}

        if self.grid.has_won():
            return await self.handle_level_complete()

        moved = False
        if user_input in ["w", "arriba"]:
            moved = self.grid.get_player().move_up()
        elif user_input in ["s", "abajo"]:
            moved = self.grid.get_player().move_down()
        elif user_input in ["a", "izquierda"]:
            moved = self.grid.get_player().move_left()
        elif user_input in ["d", "derecha"]:
            moved = self.grid.get_player().move_right()
        elif user_input == "r":
            self.grid.reset()
            moved = True
        elif user_input == "mr":
            self.grid.reset_map()
            moved = True

        if moved:
            self.moves_count += 1
            self.grid.update_grid()

        if self.grid.has_won():
            return await self.handle_level_complete()

        return {"action": "move", "moved": moved}

    async def handle_level_complete(self) -> Dict[str, Any]:
        time_taken = time.time() - self.start_time
        score = max(1000 - self.moves_count * 10 - int(time_taken), 100)
        await self.leaderboard.update_player_stats(
            self.user.id,
            self.level,
            self.moves_count,
            time_taken,
            score
        )
        return {"action": "win", "score": score, "moves": self.moves_count, "time": time_taken}

    async def next_level(self):
        self.level += 1
        self.moves_count = 0
        self.start_time = time.time()
        self.update_dimensions()
        self.grid = Grid(self.width, self.height, self.level, self.player_emoji)

    def update_dimensions(self):
        if self.width < 13:
            self.width += 2
        if self.height < 8:
            self.height += 1

    async def create_game_embed(self):
        grid_str = str(self.grid)  # Obtener representación en string del tablero

        embed = discord.Embed(
            title=f"🎮 Sokobot | Nivel {self.level}",
            description=f"`\n{grid_str}\n`",  # Mostrar el grid dentro de bloque de código
            color=0x349db
        )
        embed.add_field(
            name="📝 Instrucciones",
            value="Usa los botones o escribe w, a, s, d para moverte\nr para reiniciar, mr para nuevo mapa",
            inline=False
        )
        embed.add_field(
            name="👤 Jugador",
            value=self.user.mention,
            inline=True
        )
        embed.add_field(
            name="📊 Movimientos",
            value=str(self.moves_count),
            inline=True
        )
        embed.add_field(
            name="⏱️ Tiempo",
            value=f"{int(time.time() - self.start_time)}s",
            inline=True
        )
        embed.set_footer(text="Empuja las cajas 📦 hacia los destinos ❌")
        return embed


    async def create_win_embed(self) -> discord.Embed:
        time_taken = int(time.time() - self.start_time)
        score = max(1000 - self.moves_count * 10 - time_taken, 100)
        embed = discord.Embed(
            title="🎉 ¡Nivel Completado!",
            description=f"¡Felicitaciones {self.user.mention}!\nHas completado el nivel {self.level}",
            color=0x00ff00
        )
        embed.add_field(name="📊 Movimientos", value=str(self.moves_count), inline=True)
        embed.add_field(name="⏱️ Tiempo", value=f"{time_taken}s", inline=True)
        embed.add_field(name="🏆 Puntuación", value=str(score), inline=True)
        embed.set_footer(text="¿Continuar al siguiente nivel?")
        return embed

    async def end_game(self):
        self.game_active = False
        if self.level > 1:
            time_taken = time.time() - self.start_time
            await self.leaderboard.update_player_stats(
                self.user.id,
                self.level - 1,
                self.moves_count,
                time_taken,
                0
            )

    def is_active(self) -> bool:
        return self.game_active and (time.time() - self.last_action < 600)

    def get_grid_string(self) -> str:
        return str(self.grid)
