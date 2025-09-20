import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'sokobot.db')
    MAX_CONCURRENT_GAMES = int(os.getenv('MAX_CONCURRENT_GAMES', '100'))
    GAME_TIMEOUT_MINUTES = int(os.getenv('GAME_TIMEOUT_MINUTES', '10'))
    DEFAULT_PREFIX = os.getenv('DEFAULT_PREFIX', '!')
    LEADERBOARD_MAX_ENTRIES = int(os.getenv('LEADERBOARD_MAX_ENTRIES', '20'))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'sokobot.log')
    TESTING_MODE = os.getenv('TESTING_MODE', 'false').lower() in ('true', '1', 'yes')
    # Lista de guild IDs separadas por coma (string)
    TEST_GUILDS = [int(g) for g in os.getenv('TEST_GUILDS', '').split(',') if g.strip().isdigit()]
    GITHUB_URL = os.getenv('GITHUB_URL', 'https://github.com/tu-usuario/sokobot-python')
    SUPPORT_SERVER = os.getenv('SUPPORT_SERVER', 'https://discord.gg/tu-servidor')
    INVITE_URL = os.getenv('INVITE_URL', 'https://discord.com/api/oauth2/authorize?client_id=TU_CLIENT_ID&permissions=414464788544&scope=bot%20applications.commands')

    @classmethod
    def validate(cls):
        if not cls.DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN no está configurado en el archivo .env")
        if cls.MAX_CONCURRENT_GAMES <= 0:
            raise ValueError("MAX_CONCURRENT_GAMES debe ser mayor a 0")
        if cls.GAME_TIMEOUT_MINUTES <= 0:
            raise ValueError("GAME_TIMEOUT_MINUTES debe ser mayor a 0")
        return True

class GameEmojis:
    GROUND = "⬛"
    WALL_COLORS = {
        0: "🟥",
        1: "🟧",
        2: "🟨",
        3: "🟩",
        4: "🟦",
        5: "🟪"
    }
    BOX = "📦"
    DESTINATION = "❌"
    DEFAULT_PLAYER = "😎"

class Messages:
    GAME_STARTED = "🎮 ¡Nuevo juego iniciado! Usa los botones o comandos para moverte."
    GAME_STOPPED = "🎮 Juego terminado. ¡Gracias por jugar!"
    LEVEL_COMPLETE = "🎉 ¡Nivel completado! ¿Continuar al siguiente nivel?"
    ALREADY_PLAYING = "❌ Ya tienes un juego activo. Usa `/stop` para terminarlo primero."
    NO_ACTIVE_GAME = "❌ No tienes un juego activo. Usa `/play` para iniciar uno."
