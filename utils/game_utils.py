import time
import logging

logger = logging.getLogger(__name__)

class GameUtils:
    def __init__(self):
        self.active_games = {}
        self.game_timeout = 600

    async def cleanup_inactive_games(self):
        current_time = time.time()
        games_to_remove = []
        for game_id, game_data in self.active_games.items():
            if hasattr(game_data, 'last_action'):
                if current_time - game_data.last_action > self.game_timeout:
                    games_to_remove.append(game_id)
                    logger.info(f"Juego inactivo removido: {game_id}")
        for game_id in games_to_remove:
            if game_id in self.active_games:
                try:
                    await self.active_games[game_id].end_game()
                except Exception as e:
                    logger.error(f"Error terminando juego {game_id}: {e}")
                finally:
                    del self.active_games[game_id]
        return len(games_to_remove)

    def get_active_game_count(self) -> int:
        return len(self.active_games)

    def is_user_playing(self, user_id: int) -> bool:
        return user_id in self.active_games

    def add_game(self, user_id: int, game_instance):
        self.active_games[user_id] = game_instance

    def remove_game(self, user_id: int):
        if user_id in self.active_games:
            del self.active_games[user_id]

    def get_game(self, user_id: int):
        return self.active_games.get(user_id)
