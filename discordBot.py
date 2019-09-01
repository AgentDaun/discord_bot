# -*- coding: utf-8 -*-
from discord.ext import commands
import discord
from datetime import datetime

import asyncio

from apiBattle import get_server_info
from messages_templates import *
from chatparser.messages_parser import chat_message_parse, kill_message_parse
from chatparser.scumlogs import read_logs

description = '''not used yet'''

# ``` - Эти палочки нужны для стиля текста
# \n - Перенос строки

import logging
import sys

# root = logging.getLogger()
# root.setLevel(logging.DEBUG)

# handler = logging.StreamHandler(sys.stdout)
# handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# root.addHandler(handler)


# Текст команды settings
SETTINGS_TEXT = '```Слотов - 50 слота\nРейт лута - x1\nУрон - x2\nМарионеток - 100 шт\nАвтомобилей - 64 шт\nЖивотных - 20 шт\nЭирдропы - x2\nХранение - 10 дней\nВремя - 3 часа / 2 суток```'

# Текст команды help
HELP_TEXT = '```$online - Информация о сервереnn\n$settings - Настройки сервера```'

# Знак перед каждой командой
COMMAND_PREFIX = "$"

# Токен для бота, можешь поменять его/получить на https://discordapp.com/developers/applications/590070691634741258/bots
BOT_TOKEN = "NTk1ODczMTk4NzM5MDMwMDI2.XWwlEQ.o2tHG88vIQ06OZUtSCbitH3Mhq8"
# BOT_TOKEN = "NTk1ODk2NjMxODk1Nzg1NTI1.XWkoWA.PT-XdCvq8D5SnrE1lsTSHdLohYc"

# Название канала, показывающий онлайн на сервере. В конце подставляется сам онлайн.
TEXT_ON_ONLINE_CHANNEL = "Сейчас в игре: "

# Название канала, показывающий мировой ранг сервера. В конце подставляется сам онлайн.
TEXT_ON_WORLD_RANK_CHANNEL = "Мировой ранг: "

bot = commands.Bot(command_prefix=COMMAND_PREFIX, description=description)
bot.remove_command('help')

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
                        text= message['text']
                        author = message['author']
                        date = message['date']
                        ready_message = create_chat_message_template(text=text, author=author, date=date)
                        await chat_messages_channel.send(embed=ready_message)
            if kill_msgs:
                # print(kill_msgs)
                for message_raw in kill_msgs:
                    message = kill_message_parse(message_raw)
                    print(message)
                    if message: 
                        date = message['date']
                        killer = message['killer']
                        killer_loc = message['killer_loc']
                        killed = message['killed']
                        killed_loc = message['killed_loc']
                        ready_message = create_kill_message_template(killer=killer,
                                                                    killer_loc=killer_loc,
                                                                    killed=killed,
                                                                    killed_loc=killed_loc,
                                                                    date=date)
                        await kill_messages_channel.send(embed=ready_message)
        return True
    except Exception as e:
        print(sys._getframe().f_code.co_name + " @ Caught exception").center(50) + '\n' + (str(e).decode('utf8') + '. line: ' + str(sys.exc_info()[2].tb_lineno)).center(50)
        print(f"2. {e}")
        return False
        await asyncio.sleep(15)

@bot.event
async def on_ready():
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    onlineChannel = bot.get_channel(595878933652701204)
    worldRankChannel = bot.get_channel(595878994969231363)
    # onlineChannel = bot.get_channel(595899795550371840)595878933652701204
    # worldRankChannel = bot.get_channel(595899869898473472)
    while True:
        try:
            info = get_server_info()
            online = info['players']
            max_online = info['maxPlayers']
            rank = info['rank']
            await onlineChannel.edit(name="{}{}/{}".format(TEXT_ON_ONLINE_CHANNEL, online, max_online))
            await worldRankChannel.edit(name="{}#{}".format(TEXT_ON_WORLD_RANK_CHANNEL, rank))
        except Exception as e:
            print(e)
            await asyncio.sleep(60)
        try:
            await check_new_messages()
        except:
            await asyncio.sleep(30)
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
