from discord.ext import commands
import pytchat,asyncio,csv,os,queue
from .modules import setting
from logging import basicConfig, getLogger
from pytchat import LiveChatAsync
from os.path import join, dirname

basicConfig(level=setting.LOG_LEVEL)
LOG = getLogger(__name__)

# コグとして用いるクラスを定義。
class GetYouTubeChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = queue.Queue()
        self.livechat = None
        self.channel = None

    def prepare(self):
        if len(self.bot.guilds) == 1:
            guild = self.bot.guilds[0] # BOTに紐づくギルドが1つのみという前提でギルドを取得
        else:
            LOG.error(f'BOTに紐づくギルドは1件である必要があります。お手数ですが登録/削除をお願いします。あなたのBOTに紐づくギルドの数：{self.bot.guilds}')
            LOG.info('処理を終了します。')
            return
        if setting.DISCORD_CHANNEL_ID:
            self.channel = guild.get_channel(setting.DISCORD_CHANNEL_ID)

    # 読み込まれた時の処理
    @commands.Cog.listener()
    async def on_ready(self):
        LOG.debug(self.bot.guilds)
        self.prepare()
        await self.main()

    async def main(self):
        self.livechat = LiveChatAsync(setting.VIDEO_ID, callback = self.func)
        while self.livechat.is_alive():
            await asyncio.sleep(0.01)
            #other background operation.

        # If you want to check the reason for the termination, 
        # you can use `raise_for_status()` function.
        try:
            self.livechat.raise_for_status()
        except pytchat.ChatDataFinished:
            print("Chat data finished.")
        except Exception as e:
            print(type(e), str(e))

    #callback function is automatically called periodically.
    async def func(self, chatdata):

        for c in chatdata.items:
            amount = f'({c.amountString})' if c.amountString != '' else ''
            youtube_chat_text = f"`{c.datetime}` -> [{c.author.name}] {c.message}{amount}"
            put_queue_task = asyncio.create_task(self.put_queue(youtube_chat_text)) if youtube_chat_text is not None else put_queue_task
            gather_queue_task = asyncio.create_task(self.gather_queue(self.queues))
            file_write_task = asyncio.create_task(self.file_write(c))
            gathered_data = await gather_queue_task
            await file_write_task,put_queue_task

            if gathered_data is not None and gathered_data != '':
                log_write_task = asyncio.create_task(self.log_write(gathered_data))
                channel_send_task = asyncio.create_task(self.channel.send(gathered_data))
                await channel_send_task, log_write_task

    async def put_queue(self, text):
        self.queues.put(text)

    async def log_write(self, text):
        LOG.info(text)

    async def file_write(self, c):
        if setting.CSV_OUTPUT_FLAG:
            FILE_PATH = join(dirname(__file__), 'modules' + os.sep + 'files' + os.sep + 'csv' + os.sep + setting.VIDEO_ID + '.csv')
            with open(FILE_PATH, 'a') as f:
                writer = csv.writer(f)
                writer.writerow([c.datetime, c.type, c.id, c.message, c.elapsedTime, c.amountString, c.currency, c.amountValue, c.author.name])

    async def gather_queue(self, queue_data):
        if queue_data.empty():
            return
        gathered_data = ''
        while not queue_data.empty():
            gathered_data += f'{queue_data.get()}'
        return gathered_data

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    LOG.info('GetYouTubeChatCogを読み込む！')
    bot.add_cog(GetYouTubeChatCog(bot))  # GetYouTubeChatCogにBotを渡してインスタンス化し、Botにコグとして登録する。