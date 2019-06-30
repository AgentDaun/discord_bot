# -*- coding: utf-8 -*-
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import asyncio
description = '''not used yet'''

# ``` - Эти палочки нужны для стиля текста
# \n - Перенос строки

# Текст команды settings
SETTINGS_TEXT = '```65 слота | На сервере могут играть одновременно 64 человека\nЛут x1.8 | Вероятность найти предметы, увеличена в 4 раза.\nУрон x2 | Повышенный урон от не игровых персонажей.\n100 марионеток | Экстремальное количество марионеток в мире.\n65 Автомобиля | Максимально возможное количество на сегодняшний день\n20 животных | Животных хватит всем\nГруз x2 | Два аирдропа одновременно ждут Вас на карте\n7 дней | Время хранения созданных игроками ровна 1 недели\n1 день = 4 часа | Старт после перезагрузки 5:00 День продлится 4 часа```'

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
        info = scrapping()
        await onlineChannel.edit(name="{}{}".format(TEXT_ON_ONLINE_CHANNEL, info['count']))
        await worldRankChannel.edit(name="{}{}".format(TEXT_ON_WORLD_RANK_CHANNEL, info['rank']))
        await asyncio.sleep(2)


@bot.command()
async def online(ctx):
    info = scrapping()
    await ctx.send("```IP адресс: {}\nИгроков: {}\nМировой ранг: {}\nСтатус: {}\nПерезагрузки: 00/04/08/12/16/20:00 UTC+3:00```".format(info['address'], info['count'], info['rank'], info['status']))


@bot.command()
async def settings(ctx):
    await ctx.send(SETTINGS_TEXT)


@bot.command()
async def help(ctx):
    await ctx.send(HELP_TEXT)


if __name__ == '__main__':
    bot.run(BOT_TOKEN)
