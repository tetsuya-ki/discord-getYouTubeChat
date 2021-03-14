import pytchat,discord,asyncio
from modules import settings
from logging import basicConfig, getLogger

basicConfig(level=settings.LOG_LEVEL)
LOG = getLogger(__name__)

bot = discord.Client(intents=discord.Intents.default())
chat = pytchat.create(video_id=settings.VIDEO_ID)

async def get_youtube_chat():
    while chat.is_alive():
        for c in chat.get().sync_items():
            youtube_chat_text = f"`{c.datetime}` -> [{c.author.name}] {c.message}"

            if len(bot.guilds) == 1:
                guild = bot.guilds[0] # BOTに紐づくギルドが1つのみという前提でギルドを取得
            else:
                LOG.error(f'BOTに紐づくギルドは1件である必要があります。お手数ですが登録/削除をお願いします。あなたのBOTに紐づくギルドの数：{bot.guilds}')
                LOG.info('処理を終了します。')
                return
            channel = guild.get_channel(settings.DISCORD_CHANNEL_ID)
            await channel.send(youtube_chat_text)


@bot.event
async def on_ready():
    LOG.info('bot ready.')
    await get_youtube_chat()

bot.run(settings.DISCORD_TOKEN)