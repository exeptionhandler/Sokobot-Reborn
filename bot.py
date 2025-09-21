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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class SokobotPython(Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guild_messages = True
        intents.guild_reactions = True

        super().__init__(
            command_prefix=self.get_prefix,
            intents=intents,
            description="Sokobot en Python - El clásico juego de rompecabezas de empujar cajas"
        )

        self.db = Database()
        self.leaderboard = Leaderboard(self.db)
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

    async def setup_hook(self):
        logger.info("Configurando bot...")
        print("Comandos actuales en árbol antes de cargar cogs:", [cmd.name for cmd in self.tree.get_commands()])

        await self.db.initialize()
        await self.leaderboard.initialize()

        await self.load_cogs()
        
        print("Comandos actuales en árbol después de cargar cogs:", [cmd.name for cmd in self.tree.get_commands()])

        if self.testing_mode and self.test_guilds:
            for guild_id in self.test_guilds:
                guild = discord.Object(id=guild_id)
                try:
                    synced = await self.tree.sync(guild=guild)
                    logger.info(f"Sincronizados {len(synced)} comandos slash en servidor de prueba {guild_id}")
                except Exception as e:
                    logger.error(f"Error sincronizando comandos en servidor de prueba {guild_id}: {e}")
        else:
            try:
                synced = await self.tree.sync()
                logger.info(f"Sincronizados {len(synced)} comandos slash globalmente")
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
        activity = discord.Game(name="Sokoban | /play para jugar")
        await self.change_presence(activity=activity)

        commands = await self.tree.fetch_commands()
        logger.info(f'Comandos slash sincronizados: {[cmd.name for cmd in commands]}')

        self.loop.create_task(self.game_cleanup_timer())

    async def on_guild_join(self, guild):
        logger.info(f"Bot agregado al servidor: {guild.name} (ID: {guild.id})")

    async def on_guild_remove(self, guild):
        logger.info(f"Bot removido del servidor: {guild.name} (ID: {guild.id})")
        if guild.id in self.prefixes:
            del self.prefixes[guild.id]
        await self.db.remove_guild_data(guild.id)

    async def game_cleanup_timer(self):
        while not self.is_closed():
            try:
                await self.game_utils.cleanup_inactive_games()
                await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"Error en cleanup timer: {e}")
                await asyncio.sleep(60)

    def debug_log(self, message):
        if self.debug:
            logger.info(f"[DEBUG] {message}")

async def main():
    bot = SokobotPython()
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logger.error("No se encontró DISCORD_TOKEN en el archivo .env")
        return
    try:
        await bot.start(token)
    except KeyboardInterrupt:
        logger.info("Bot detenido por el usuario")
    except Exception as e:
        logger.error(f"Error ejecutando el bot: {e}")
    finally:
        if not bot.is_closed():
            await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
