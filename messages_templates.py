from datetime import datetime
import discord


def create_chat_message_template(text, author, date):
    date_result = datetime.strptime(date, '%Y.%m.%d-%H.%M.%S')
    embed = discord.Embed(title="Пишет в общем чате:",
                          colour=discord.Colour(0x2b50ff),
                          description=text, timestamp=date_result)

    embed.set_author(name=author,
                     url="http://s1.iconbird.com/ico/2013/6/271/w513h5131371296185messages.png",
                     icon_url="https://scumfree.ru/wp-content/uploads/2019/09/favicon-400x400.png")
    embed.set_footer(text="SCUMFREE.RU",
                     icon_url="http://s1.iconbird.com/ico/2013/6/271/w513h5131371296185messages.png")

    return embed


def create_kill_message_template(killer, killed, date, kill_sector=None, kill_distance=None):
    date_result = datetime.strptime(date, '%Y.%m.%d-%H.%M.%S')
    embed = discord.Embed(title="Совершил убийство",
                          colour=discord.Colour(0xdd0016),
                          description=f"Имя жертвы **{killed}**",
                          timestamp=date_result)

    embed.set_author(name=killer,
                     url="https://scumfree.ru/",
                     icon_url="https://scumfree.ru/wp-content/uploads/2019/09/favicon-400x400.png")
    embed.set_footer(text="SCUMFREE.RU", icon_url="http://s1.iconbird.com/ico/2013/9/440/w128h1281380212083target.png")

    if kill_sector:
        embed.add_field(name="Дистанция",
                        value=f"{kill_distance} м.",
                        inline=True)
        embed.add_field(name="Сектор",
                        value=kill_sector['sector_letter'] + kill_sector['sector_number'],
                        inline=True)
    else:
        embed.add_field(name="Дистанция",
                        value=f"не более 10 метров",
                        inline=True)
        embed.add_field(name="Сектор",
                        value=f"Закрытая информация",
                        inline=True)

    return embed
