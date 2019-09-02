# -*- coding: utf-8 -*-
import traceback

from discord.ext import commands

import asyncio

from apiBattle import get_server_info
from messages_templates import create_chat_message_template, create_kill_message_template
from chatparser.messages_parser import chat_message_parse, kill_message_parse
from chatparser.scumlogs import read_logs

description = '''not used yet'''

# root = logging.getLogger()
# root.setLevel(logging.DEBUG)

# handler = logging.StreamHandler(sys.stdout)
# handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# root.addHandler(handler)

# ``` - Эти палочки нужны для стиля текста
# \n - Перенос строки


# Текст команды settings
SETTINGS_TEXT = '```Слотов - 50 слота\nРейт лута - x1\nУрон - x2\nМарионеток - 100 шт\nАвтомобилей - 64 шт\nЖивотных - 20 шт\nЭирдропы - x2\nХранение - 10 дней\nВремя - 3 часа / 2 суток```'

# Текст команды help
HELP_TEXT = '```$online - Информация о сервереnn\n$settings - Настройки сервера```'

# Знак перед каждой командой
COMMAND_PREFIX = "$"

# Токен для бота, можешь поменять его/получить на https://discordapp.com/developers/applications/590070691634741258/bots
# BOT_TOKEN = "NTk1ODczMTk4NzM5MDMwMDI2.XWwlEQ.o2tHG88vIQ06OZUtSCbitH3Mhq8"
BOT_TOKEN = "NTk1ODk2NjMxODk1Nzg1NTI1.XW1m8w.atM-59720fgOjzYRlNp8CHWWzfc"

# Название канала, показывающий онлайн на сервере. В конце подставляется сам онлайн.
TEXT_ON_ONLINE_CHANNEL = "Сейчас в игре: "

# Название канала, показывающий мировой ранг сервера. В конце подставляется сам онлайн.
TEXT_ON_WORLD_RANK_CHANNEL = "Мировой ранг: "

bot = commands.Bot(command_prefix=COMMAND_PREFIX, description=description)
bot.remove_command('help')

# chat_messages_channel = bot.get_channel(595899795550371840)
# kill_messages_channel = bot.get_channel(595899869898473472)


async def check_new_messages():
    chat_messages_channel = bot.get_channel(617040424846229504)
    kill_messages_channel = bot.get_channel(617040494593179840)
    try:
        messages, result = await read_logs()
        if result:
            chat_msgs = messages[0]
            kill_msgs = messages[1]
            if chat_msgs:
                for message_raw in chat_msgs:
                    message = chat_message_parse(message_raw)
                    if message:
                        text = message['text']
                        author = message['author']
                        date = message['date']
                        ready_message = create_chat_message_template(text=text,
                                                                     author=author,
                                                                     date=date)
                        await chat_messages_channel.send(embed=ready_message)
            if kill_msgs:
                # print(kill_msgs)
                for message_raw in kill_msgs:
                    message = kill_message_parse(message_raw)
                    if message:
                        if not message['kill_sector'] and message['chat_type'] != "Local":

                            killed = message['killed']
                            killer = message['killer']
                            date = message['date']

                            ready_message = create_kill_message_template(date=date,
                                                                         killer=killer,
                                                                         killed=killed)
                        if not message["is_event_kill"]:
                            date = message['date']
                            killer = message['killer']
                            killed = message['killed']
                            kill_sector = message['kill_sector']
                            kill_distance = message['kill_distance']

                            ready_message = create_kill_message_template(date=date,
                                                                         killer=killer,
                                                                         killed=killed,
                                                                         kill_sector=kill_sector,
                                                                         kill_distance=kill_distance)
                            await kill_messages_channel.send(embed=ready_message)
        return True
    except Exception:
        print(traceback.format_exc())
        await asyncio.sleep(15)
        return False


@bot.event
async def on_ready():
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    onlineChannel = bot.get_channel(595878933652701204)
    worldRankChannel = bot.get_channel(595878994969231363)
    # onlineChannel = bot.get_channel(595899795550371840)
    # worldRankChannel = bot.get_channel(595899869898473472)
    while True:
        info = get_server_info()['attributes']
        online = info['players']
        max_online = info['maxPlayers']
        rank = info['rank']
        await onlineChannel.edit(name="{}{}/{}".format(TEXT_ON_ONLINE_CHANNEL, online, max_online))
        await worldRankChannel.edit(name="{}#{}".format(TEXT_ON_WORLD_RANK_CHANNEL, rank))

        new_messages_confirm = await check_new_messages()
        if new_messages_confirm:
            print("Confirmed New")
        else:
            print("Last messaged dropped into void?")
        await asyncio.sleep(10)


# @bot.command()
# async def online(ctx):
#     try:
#         message = await ctx.send("Обрабатываю вызов..")
#         info = get_server_info()['attributes']
#     except Exception as e:
#         print(e)
#         await ctx.send('```Что-то пошло не так. Попробуй через 5 секунд.```')
#         await asyncio.sleep(5)
#         return
#     ip = info['ip']
#     online = info['players']
#     max_online = info['maxPlayers']
#     rank = info['rank']
#     status = info['status']
#     await message.edit(content="```IP адресс: {}\nИгроков: {}/{}\nМировой ранг: {}\nСтатус: {}\nПерезагрузки: 00/04/08/12/16/20:00 UTC+3:00```".format(ip, online, max_online, rank, status))


# @bot.command()
# async def settings(ctx):
#     onlineChannel = bot.get_channel(595899795550371840)
#     await onlineChannel.send([])


# @bot.command()
# async def help(ctx):
#     await ctx.send(HELP_TEXT)


if __name__ == '__main__':
    bot.run(BOT_TOKEN)
