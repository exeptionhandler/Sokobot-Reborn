import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import logging

from dotenv import load_dotenv
import os

from utils.game_utils import GameUtils
from commands.game_commands import GameCommands
from commands.info_commands import InfoCommands
from commands.admin_commands import AdminCommands
from commands.leaderboard_commands import LeaderboardCommands
from database.database import Database
from database.leaderboard import Leaderboard
from config import Config
from typing import Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class SokoromiBot(Bot):  # ← CAMBIAR: SokobotPython → SokoromiBot
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guild_messages = True
        intents.guild_reactions = True

        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            intents=intents,
            description="Sokoromi - Bot de Sokoban para Discord ❤️"  # ← CAMBIAR: Descripción actualizada
        )

        self.db = Database()
        self.leaderboard = Leaderboard(self.db, self)
        self.game_utils = GameUtils()
        self.prefixes = {}

        self.debug = False

        # Usar configuración centralizada
        self.testing_mode = Config.TESTING_MODE
        self.test_guilds = Config.TEST_GUILDS

    async def get_prefix(self, message):
        if not message.guild:
            return "!"
        guild_id = message.guild.id
        if guild_id in self.prefixes:
            return self.prefixes[guild_id]
        prefix = await self.db.get_guild_prefix(guild_id)
        self.prefixes[guild_id] = prefix
        return prefix

    async def on_message(self, message):
        if message.author.bot:
            return
        ctx = await self.get_context(message)
        if ctx.prefix is not None and message.guild:
            guild_id = message.guild.id
            if guild_id not in self.prefixes:
                prefix = await self.db.get_guild_prefix(guild_id)
                self.prefixes[guild_id] = prefix
        await self.process_commands(message)

    async def setup_hook(self):
        logger.info("Configurando bot...")
        print("Comandos actuales en árbol antes de cargar cogs:", [cmd.name for cmd in self.tree.get_commands()])

        await self.db.initialize()
        await self.leaderboard.initialize()

        await self.load_cogs()
        
        print("Comandos actuales en árbol después de cargar cogs:", [cmd.name for cmd in self.tree.get_commands()])

        # ← MEJORAR: Logging más detallado para User Apps
        if self.testing_mode and self.test_guilds:
            for guild_id in self.test_guilds:
                guild = discord.Object(id=guild_id)
                try:
                    synced = await self.tree.sync(guild=guild)
                    logger.info(f"Sincronizados {len(synced)} comandos slash en servidor de prueba {guild_id}")
                    logger.info(f"Comandos disponibles: {[cmd.name for cmd in synced]}")
                except Exception as e:
                    logger.error(f"Error sincronizando comandos en servidor de prueba {guild_id}: {e}")
        else:
            try:
                synced = await self.tree.sync()
                logger.info(f"Sincronizados {len(synced)} comandos slash globalmente")
                logger.info(f"Comandos User App listos: {[cmd.name for cmd in synced if getattr(cmd, 'allowed_installs', None)]}")
            except Exception as e:
                logger.error(f"Error sincronizando comandos: {e}")

    async def load_cogs(self):
        try:
            await self.add_cog(GameCommands(self))
            await self.add_cog(InfoCommands(self))
            await self.add_cog(AdminCommands(self))
            await self.add_cog(LeaderboardCommands(self))

            logger.info("Comandos cargados exitosamente")
        except Exception as e:
            logger.error(f"Error cargando comandos: {e}")

    async def on_ready(self):
        logger.info(f'{self.user} está conectado y listo!')
        logger.info(f'Conectado a {len(self.guilds)} servidores')
        
        # ← CAMBIAR: Actividad actualizada
        activity = discord.Game(name="Sokoromi | /play para jugar ✨")
        await self.change_presence(activity=activity)

        commands = await self.tree.fetch_commands()
        logger.info(f'Comandos slash sincronizados: {[cmd.name for cmd in commands]}')
        
        # ← AGREGAR: Log específico para User Apps
        user_app_commands = [cmd.name for cmd in commands if hasattr(cmd, 'allowed_installs')]
        if user_app_commands:
            logger.info(f'Comandos User App disponibles: {user_app_commands}')

        self.loop.create_task(self.game_cleanup_timer())

    async def on_guild_join(self, guild):
        logger.info(f"Sokoromi agregado al servidor: {guild.name} (ID: {guild.id}) - {guild.member_count} miembros")

    async def on_guild_remove(self, guild):
        logger.info(f"Sokoromi removido del servidor: {guild.name} (ID: {guild.id})")
        if guild.id in self.prefixes:
            del self.prefixes[guild.id]
        # ← MEJORAR: Mejor manejo de errores en cleanup
        try:
            await self.db.remove_guild_data(guild.id)
        except Exception as e:
            logger.error(f"Error limpiando datos del servidor {guild.id}: {e}")

    async def game_cleanup_timer(self):
        """Timer para limpiar juegos inactivos cada minuto"""
        while not self.is_closed():
            try:
                # ← MEJORAR: Más logging del cleanup
                cleaned = await self.game_utils.cleanup_inactive_games()
                if cleaned > 0:
                    logger.info(f"Limpieza automática: {cleaned} juegos inactivos removidos")
                await asyncio.sleep(60)  # Esperar 1 minuto
            except Exception as e:
                logger.error(f"Error en cleanup timer: {e}")
                await asyncio.sleep(60)  # Continuar a pesar del error

    def debug_log(self, message):
        """Log de debug cuando está habilitado"""
        if self.debug:
            logger.info(f"[DEBUG] {message}")

async def main():
    bot = SokoromiBot()  # ← CAMBIAR: Nombre actualizado
    token = os.getenv('DISCORD_TOKEN')
    
    if not token:
        logger.error("No se encontró DISCORD_TOKEN en el archivo .env")
        return
        
    try:
        logger.info("Iniciando Sokoromi...")  # ← AGREGAR: Log de inicio
        await bot.start(token)
    except KeyboardInterrupt:
        logger.info("Sokoromi detenido por el usuario")
    except Exception as e:
        logger.error(f"Error ejecutando Sokoromi: {e}")
    finally:
        if not bot.is_closed():
            logger.info("Cerrando conexiones...")
            await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
