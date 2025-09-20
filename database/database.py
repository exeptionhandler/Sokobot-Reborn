import aiosqlite
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path: str = "sokobot.db"):
        self.db_path = db_path
        self.connection = None

    async def initialize(self):
        try:
            self.connection = await aiosqlite.connect(self.db_path)
            self.connection.row_factory = aiosqlite.Row
            await self.execute('''
                CREATE TABLE IF NOT EXISTS guild_prefixes (
                    guild_id INTEGER PRIMARY KEY,
                    prefix TEXT NOT NULL DEFAULT '!'
                )
            ''')
            logger.info("Base de datos inicializada correctamente")
        except Exception as e:
            logger.error(f"Error inicializando base de datos: {e}")
            raise

    async def execute(self, query: str, parameters: tuple = ()) -> None:
        if not self.connection:
            await self.initialize()
        try:
            async with self.connection.execute(query, parameters) as cursor:
                await self.connection.commit()
        except Exception as e:
            logger.error(f"Error ejecutando query: {query} - {e}")
            raise

    async def fetch_one(self, query: str, parameters: tuple = ()):
        if not self.connection:
            await self.initialize()
        try:
            async with self.connection.execute(query, parameters) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error en fetch_one: {query} - {e}")
            return None

    async def fetch_all(self, query: str, parameters: tuple = ()):
        if not self.connection:
            await self.initialize()
        try:
            async with self.connection.execute(query, parameters) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows] if rows else []
        except Exception as e:
            logger.error(f"Error en fetch_all: {query} - {e}")
            return []

    async def get_guild_prefix(self, guild_id: int) -> str:
        result = await self.fetch_one('SELECT prefix FROM guild_prefixes WHERE guild_id = ?', (guild_id,))
        return result['prefix'] if result else '!'

    async def set_guild_prefix(self, guild_id: int, prefix: str):
        await self.execute('INSERT OR REPLACE INTO guild_prefixes (guild_id, prefix) VALUES (?, ?)', (guild_id, prefix))

    async def remove_guild_prefix(self, guild_id: int):
        await self.execute('DELETE FROM guild_prefixes WHERE guild_id = ?', (guild_id,))

    async def remove_guild_data(self, guild_id: int):
        await self.remove_guild_prefix(guild_id)

    async def close(self):
        if self.connection:
            await self.connection.close()
            self.connection = None
