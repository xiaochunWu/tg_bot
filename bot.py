import requests
import schedule
import time
from telegram.ext import Updater, CommandHandler
from telegram import Bot
import telegram.vendor.ptb_urllib3.urllib3 as urllib3
from openai import OpenAI

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7851775832:AAEtuGXRVLa4VJmKcd6W3BAP7KQGlPv2TEU"
# 源群组ID
SOURCE_GROUP_ID = -4755939234  # 替换为实际的群组ID
# 目标频道ID
TARGET_CHANNEL_ID = "@your_channel_name"  # 替换为实际的频道名称或ID
# proxy
proxy_url = 'https://127.0.0.1:9090'
proxy = urllib3.ProxyManager(proxy_url)
# LLM API
API_KEY=os.version.get("DEEPSEEK_API_KEY")
request_url="https://ark.cn-beijing.volces.com/api/v3"
client = OpenAI(
        api_key=API_KEY,
        base_url=request_url
)

# 存储上一次总结的时间
last_summary_time = time.time()

# 初始化Telegram Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)
updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# 获取群组聊天记录
def get_group_chat_history():
    global last_summary_time
    messages = []
    # 模拟获取群组消息，实际中可能需要分页获取等操作
    for message in bot.get_updates():
        if message.date.timestamp() > last_summary_time:
            if message.text:
                messages.append(message.text)
    last_summary_time = time.time()
    return " ".join(messages)

# 调用DeepSeek API进行总结
def summarize_text(text):
    completion = client.chat.comletions.create(
        model="<model endpoint ID>",
        messages=[
            {"role": "system", "content": "请帮我对下列聊天记录进行总结"},
            {"role": "user", "content": text}
        ]
    )

    return completion.choice[0].message.content

# 定时任务：每小时总结并转发
def hourly_summary_and_forward():
    chat_history = get_group_chat_history()
    if chat_history:
        summary = summarize_text(chat_history)
        if summary:
            bot.send_message(chat_id=TARGET_CHANNEL_ID, text=f"过去一小时群组聊天总结：{summary}")

# 调度定时任务
schedule.every(1).hours.do(hourly_summary_and_forward)

# 启动Bot
updater.start_polling()

# 运行定时任务循环
while True:
    schedule.run_pending()
    time.sleep(1)

'''
chat_history = get_group_chat_history()
print(chat_history)
'''