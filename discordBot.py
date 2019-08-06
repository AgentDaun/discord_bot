# -*- coding: utf-8 -*-
from discord.ext import commands
from apiBattle import get_server_info
import asyncio
description = '''not used yet'''

# ``` - Эти палочки нужны для стиля текста
# \n - Перенос строки

# Текст команды settings
SETTINGS_TEXT = '```Слотов - 50 слота\nРейт лута - x1\nУрон - x2\nМарионеток - 100 шт\nАвтомобилей - 64 шт\nЖивотных - 20 шт\nЭирдропы - x2\nХранение - 10 дней\nВремя - 3 часа / 2 суток```'

# Текст команды help
HELP_TEXT = '```$online - Информация о сервереnn\n$settings - Настройки сервера```'

# Знак перед каждой командой
COMMAND_PREFIX = "$"

# Токен для бота, можешь поменять его/получить на https://discordapp.com/developers/applications/590070691634741258/bots
BOT_TOKEN = "NTk1ODczMTk4NzM5MDMwMDI2.XUnxpQ.Icb2Jl-yFKeg531fJU7tqSxXpRc"

# Название канала, показывающий онлайн на сервере. В конце подставляется сам онлайн.
TEXT_ON_ONLINE_CHANNEL = "Сейчас в игре: "

# Название канала, показывающий мировой ранг сервера. В конце подставляется сам онлайн.
TEXT_ON_WORLD_RANK_CHANNEL = "Мировой ранг: "

bot = commands.Bot(command_prefix=COMMAND_PREFIX, description=description)
bot.remove_command('help')


@bot.event
async def on_ready():
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    onlineChannel = bot.get_channel(595878933652701204)
    worldRankChannel = bot.get_channel(595878994969231363)
    while True:
        info = get_server_info()['attributes']
        online = info['players']
        rank = info['rank']
        await onlineChannel.edit(name="{}{}".format(TEXT_ON_ONLINE_CHANNEL, online))
        await worldRankChannel.edit(name="{}{}".format(TEXT_ON_WORLD_RANK_CHANNEL, rank))


@bot.command()
async def online(ctx):
    try:
        message = await ctx.send("Обрабатываю вызов..")
        info = get_server_info()['attributes']
    except Exception as e:
        print(e)
        await ctx.send('```Что-то пошло не так. Попробуй через 5 секунд.```')
        await asyncio.sleep(5)
        return
    ip = info['ip']
    online = info['players']
    max_online = info['maxPlayers']
    rank = info['rank']
    status = info['status']
    await message.edit(content="```IP адресс: {}\nИгроков: {}/{}\nМировой ранг: {}\nСтатус: {}\nПерезагрузки: 00/04/08/12/16/20:00 UTC+3:00```".format(ip, online, max_online, rank, status))


@bot.command()
async def settings(ctx):
    await ctx.send(SETTINGS_TEXT)


@bot.command()
async def help(ctx):
    await ctx.send(HELP_TEXT)


if __name__ == '__main__':
    bot.run(BOT_TOKEN)
