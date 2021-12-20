from cogs.modules import setting
from discord.ext import commands
from logging import basicConfig, getLogger
from datetime import timedelta, timezone
from cogs.modules import setting
import discord, os, datetime
import keep_alive

# 時間
JST = timezone(timedelta(hours=9), 'JST')
now = datetime.datetime.now(JST)

basicConfig(level=setting.LOG_LEVEL)
LOG = getLogger('discord-getYouTubeChat')

# 読み込むCogの名前を格納しておく。
INITIAL_EXTENSIONS = [
    'cogs.getYouTubeChatCog'
]

class DiscordGetYoutubeChatBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        # スーパークラスのコンストラクタに値を渡して実行。
        super().__init__(command_prefix, case_insensitive=True, intents=intents, help_command=None)
        LOG.info('cogを読むぞ！')

        # INITIAL_COGSに格納されている名前から、コグを読み込む。
        for cog in INITIAL_EXTENSIONS:
            self.load_extension(cog)

    async def on_ready(self):
        LOG.info('We have logged in as {0.user}'.format(self))
        LOG.info(f"### guilds length ### {len(self.guilds)}")
        LOG.debug(f"### guilds ### \n{self.guilds}")

if __name__ == '__main__':
    intents = discord.Intents.all()
    intents.typing = False
    intents.members = False
    intents.presences = False

    bot = DiscordGetYoutubeChatBot(command_prefix='/', intents=intents)

    # start a server
    keep_alive.keep_alive()
    bot.run(setting.DISCORD_TOKEN)