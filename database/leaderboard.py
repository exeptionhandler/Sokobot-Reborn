import discord
from typing import List, Dict, Optional, Tuple

class Leaderboard:
    def __init__(self, database, bot=None):
        self.db = database
        self.bot = bot

    async def initialize(self):
        await self.db.execute('''
            CREATE TABLE IF NOT EXISTS player_stats (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                best_level INTEGER DEFAULT 1,
                total_games INTEGER DEFAULT 0,
                total_moves INTEGER DEFAULT 0,
                total_time REAL DEFAULT 0.0,
                total_score INTEGER DEFAULT 0,
                average_score REAL DEFAULT 0.0,
                last_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await self.db.execute('''
            CREATE TABLE IF NOT EXISTS game_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                moves INTEGER NOT NULL,
                time_taken REAL NOT NULL,
                score INTEGER NOT NULL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES player_stats (user_id)
            )
        ''')
        await self.db.execute('CREATE INDEX IF NOT EXISTS idx_player_stats_level ON player_stats(best_level DESC)')
        await self.db.execute('CREATE INDEX IF NOT EXISTS idx_player_stats_score ON player_stats(total_score DESC)')
        await self.db.execute('CREATE INDEX IF NOT EXISTS idx_game_sessions_user ON game_sessions(user_id)')

    async def update_player_stats(self, user_id: int, level: int, moves: int, time_taken: float, score: int, username: str = None):
        existing = await self.db.fetch_one('SELECT * FROM player_stats WHERE user_id = ?', (user_id,))
        if existing:
            new_best_level = max(existing['best_level'], level)
            new_total_games = existing['total_games'] + 1
            new_total_moves = existing['total_moves'] + moves
            new_total_time = existing['total_time'] + time_taken
            new_total_score = existing['total_score'] + score
            new_average_score = new_total_score / new_total_games
            await self.db.execute('''
                UPDATE player_stats 
                SET best_level = ?, total_games = ?, total_moves = ?, 
                    total_time = ?, total_score = ?, average_score = ?,
                    last_played = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (new_best_level, new_total_games, new_total_moves, new_total_time, new_total_score, new_average_score, user_id))
        else:
            username = username or f"Usuario_{user_id}"
            await self.db.execute('''
                INSERT INTO player_stats 
                (user_id, username, best_level, total_games, total_moves, 
                 total_time, total_score, average_score)
                VALUES (?, ?, ?, 1, ?, ?, ?, ?)
            ''', (user_id, username, level, moves, time_taken, score, score))
        await self.db.execute('''
            INSERT INTO game_sessions (user_id, level_reached, moves, time_taken, score)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, level, moves, time_taken, score))

    async def get_player_stats(self, user_id: int) -> Optional[Dict]:
        return await self.db.fetch_one('SELECT * FROM player_stats WHERE user_id = ?', (user_id,))

    async def get_leaderboard(self, limit: int = 10, sort_by: str = 'best_level') -> List[Dict]:
        valid_sorts = {
            'best_level': 'best_level DESC',
            'total_score': 'total_score DESC', 
            'average_score': 'average_score DESC',
            'total_games': 'total_games DESC'
        }
        order_by = valid_sorts.get(sort_by, 'best_level DESC')
        return await self.db.fetch_all(f'''
            SELECT user_id, username, best_level, total_games, 
                   total_score, average_score, last_played
            FROM player_stats 
            ORDER BY {order_by}
            LIMIT ?
        ''', (limit,))

    async def create_leaderboard_embed(self, sort_by: str = 'best_level', limit: int = 10) -> discord.Embed:
        leaderboard = await self.get_leaderboard(limit, sort_by)
        sort_names = {
            'best_level': 'Mejor Nivel',
            'total_score': 'Puntuación Total',
            'average_score': 'Puntuación Promedio',
            'total_games': 'Partidas Jugadas'
        }
        title = f"🏆 Leaderboard - {sort_names.get(sort_by, 'Mejor Nivel')}"
        embed = discord.Embed(
            title=title,
            color=0xffd700,
            timestamp=discord.utils.utcnow()
        )
        if not leaderboard:
            embed.description = "No hay datos de leaderboard aún."
            return embed
        
        medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
        leaderboard_text = ""
        
        for i, player in enumerate(leaderboard):
            medal = medals[i] if i < len(medals) else "📍"
            
            # Intentar obtener el usuario real desde Discord
            display_name = player['username']
            if self.bot:
                try:
                    user = self.bot.get_user(player['user_id'])
                    if user:
                        display_name = user.display_name
                    else:
                        # Intentar fetchear el usuario si no está en caché
                        user = await self.bot.fetch_user(player['user_id'])
                        display_name = user.display_name if user else player['username']
                except:
                    # Si falla, usar el nombre guardado en la base de datos
                    display_name = player['username']
            
            # Si el nombre sigue siendo Usuario_ID, mostrar algo más amigable
            if display_name.startswith("Usuario_"):
                display_name = "Usuario Desconocido"
            
            if sort_by == 'best_level':
                value = f"Nivel {player['best_level']}"
            elif sort_by == 'total_score':
                value = f"{player['total_score']:,} pts"
            elif sort_by == 'average_score':
                value = f"{player['average_score']:.1f} pts"
            elif sort_by == 'total_games':
                value = f"{player['total_games']} partidas"
            
            leaderboard_text += f"{medal} **{display_name}** - {value}\n"
        
        embed.description = leaderboard_text
        embed.set_footer(text="Usa /stats para ver tus estadísticas personales")
        return embed
