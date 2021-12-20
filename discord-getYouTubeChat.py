import pytchat,discord,asyncio,csv,os,queue
from modules import settings
from logging import basicConfig, getLogger
from pytchat import LiveChatAsync
from os.path import join, dirname

basicConfig(level=settings.LOG_LEVEL)
LOG = getLogger(__name__)

bot = discord.Client(intents=discord.Intents.default())
queues = queue.Queue()

async def main():
    livechat = LiveChatAsync(settings.VIDEO_ID, callback = func)
    while livechat.is_alive():
        await asyncio.sleep(0.01)
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
    if len(bot.guilds) == 1:
        guild = bot.guilds[0] # BOTに紐づくギルドが1つのみという前提でギルドを取得
    else:
        LOG.error(f'BOTに紐づくギルドは1件である必要があります。お手数ですが登録/削除をお願いします。あなたのBOTに紐づくギルドの数：{bot.guilds}')
        LOG.info('処理を終了します。')
        return
    if settings.DISCORD_CHANNEL_ID:
        channel = guild.get_channel(settings.DISCORD_CHANNEL_ID)

    for c in chatdata.items:
        amount = f'({c.amountString})' if c.amountString != '' else ''
        youtube_chat_text = f"`{c.datetime}` -> [{c.author.name}] {c.message}{amount}"
        put_queue_task = asyncio.create_task(put_queue(youtube_chat_text)) if youtube_chat_text is not None else put_queue_task
        gather_queue_task = asyncio.create_task(gather_queue(queues))
        file_write_task = asyncio.create_task(file_write(c))
        gathered_data = await gather_queue_task
        await file_write_task,put_queue_task

        if gathered_data is not None and gathered_data != '':
            log_write_task = asyncio.create_task(log_write(gathered_data))
            channel_send_task = asyncio.create_task(channel.send(gathered_data))
            await channel_send_task, log_write_task

async def put_queue(text):
    queues.put(text)

async def log_write(text):
    LOG.info(text)

async def file_write(c):
    if settings.CSV_OUTPUT_FLAG:
        FILE_PATH = join(dirname(__file__), 'modules' + os.sep + 'files' + os.sep + 'csv' + os.sep + settings.VIDEO_ID + '.csv')
        with open(FILE_PATH, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([c.datetime, c.type, c.id, c.message, c.elapsedTime, c.amountString, c.currency, c.amountValue, c.author.name])

async def gather_queue(queue_data):
    if queue_data.empty():
        return
    gathered_data = ''
    # for data in queue_data.get():
    #     gathered_data += f'{dat
    while not queue_data.empty():
        gathered_data += f'{queue_data.get()}'
    return gathered_data

@bot.event
async def on_ready():
    LOG.info('bot ready.')
    await main()

if __name__=='__main__':
    try:
        bot.run(settings.DISCORD_TOKEN)
    except asyncio.exceptions.CancelledError:
        pass