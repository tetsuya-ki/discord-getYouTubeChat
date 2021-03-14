import pytchat,discord,asyncio
from modules import settings
from logging import basicConfig, getLogger
from pytchat import LiveChatAsync

basicConfig(level=settings.LOG_LEVEL)
LOG = getLogger(__name__)

bot = discord.Client(intents=discord.Intents.default())

async def main():
    livechat = LiveChatAsync(settings.VIDEO_ID, callback = func)
    while livechat.is_alive():
        await asyncio.sleep(1)
        #other background operation.

    # If you want to check the reason for the termination, 
    # you can use `raise_for_status()` function.
    try:
        livechat.raise_for_status()
    except pytchat.ChatDataFinished:
        print("Chat data finished.")
    except Exception as e:
        print(type(e), str(e))

#callback function is automatically called periodically.
async def func(chatdata):
    for c in chatdata.items:
        youtube_chat_text = f"`{c.datetime}` -> [{c.author.name}] {c.message}"
        LOG.info(youtube_chat_text)
        await chatdata.tick_async()
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
    await main()

if __name__=='__main__':
    try:
        bot.run(settings.DISCORD_TOKEN)
    except asyncio.exceptions.CancelledError:
        pass
