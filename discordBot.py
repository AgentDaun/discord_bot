# -*- coding: utf-8 -*-
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import asyncio
description = '''not used yet'''

# ``` - Эти палочки нужны для стиля текста
# \n - Перенос строки

# Текст команды settings
SETTINGS_TEXT = '```Слотов - 50 слота\nРейт лута - x2\nУрон - x2\nМарионеток - 100 шт\nАвтомобилей - 64 шт\nЖивотных - 20 шт\nЭирдропы - x2\nХранение - 10 дней\nВремя - 3 часа / 2 суток```'

# Текст команды help
HELP_TEXT = '```$online - Информация о сервереnn\n$settings - Настройки сервера```'

# Знак перед каждой командой
COMMAND_PREFIX = "$"

# Токен для бота, можешь поменять его/получить на https://discordapp.com/developers/applications/590070691634741258/bots
BOT_TOKEN = "NTkwMDcwNjkxNjM0NzQxMjU4.XRkZDw.DSB0RidI-Za2zcgoSAXSqba0w04"

# Название канала, показывающий онлайн на сервере. В конце подставляется сам онлайн.
TEXT_ON_ONLINE_CHANNEL = "Сейчас в игре: "

# Название канала, показывающий мировой ранг сервера. В конце подставляется сам онлайн.
TEXT_ON_WORLD_RANK_CHANNEL = "Мировой ранг: "

bot = commands.Bot(command_prefix=COMMAND_PREFIX, description=description)
bot.remove_command('help')


def scrapping():
    query_page = "https://www.battlemetrics.com/servers/scum/3717791"
    page = requests.get(query_page).text

    soup = BeautifulSoup(page, 'html.parser')
    horizonalInfo = soup.find('dl', attrs={'class': 'dl-horizontal'})
    items = horizonalInfo.find_all('dd')
    info = {
        'rank': items[0].text,
        'count': items[1].text,
        'address': items[2].text,
        'status': items[3].text,
    }
    return info


@bot.event
async def on_ready():
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    onlineChannel = bot.get_channel(594983928679628814)
    worldRankChannel = bot.get_channel(594984209907449908)
    while True:
        try:
            info = scrapping()
            await onlineChannel.edit(name="{}{}".format(TEXT_ON_ONLINE_CHANNEL, info['count']))
            await worldRankChannel.edit(name="{}{}".format(TEXT_ON_WORLD_RANK_CHANNEL, info['rank']))
            await asyncio.sleep(5)
        except Exception as e:
            print(e)
            print('FOREVER LOOP FOR CHANNEL')
            await asyncio.sleep(5)
            continue


@bot.command()
async def online(ctx):
    try:
        info = scrapping()
    except Exception as e:
        await ctx.send('```Информация временно отсуствует, пожалуйста, попробуйте позже```')
        await asyncio.sleep(5)
        print(e)
        print('$ONLINE COMMAND')
        return
    await ctx.send("```IP адресс: {}\nИгроков: {}\nМировой ранг: {}\nСтатус: {}\nПерезагрузки: 00/04/08/12/16/20:00 UTC+3:00```".format(info['address'], info['count'], info['rank'], info['status']))


@bot.command()
async def settings(ctx):
    await ctx.send(SETTINGS_TEXT)


@bot.command()
async def help(ctx):
    await ctx.send(HELP_TEXT)


if __name__ == '__main__':
    bot.run(BOT_TOKEN)
