from email import message
from multiprocessing.connection import wait
from os import curdir
import discord
import sqlite3, json, string
from discord.ext import commands
import config
from math_calc import *



intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# запуск бота и подключение к базе данных
@bot.event
async def on_ready():
    print('Этому серверу нужен новый шериф!')

    global base, cur
    base = sqlite3.connect('Sheriff.db')
    cur = base.cursor()
    if base:
        print('Database connected...OK')

# реакция бота на присоединение нового участника к серверу
@bot.event
async def on_member_join(member):
    await member.send('Привет. Я шериф слежу за порядком в чате, а также подрабатываю калькулятором. Третье предупреждение за мат - БАН. Список !инфо')
    
    for ch in bot.get_guild(member.guild.id).channels:
        if ch.name == 'основной':
            await bot.get_channel(ch.id).send(f'{member.mention}, круто, что ты с нами, отправил тебе в лс список команд')

# реакция бота на удаление участника с сервера
@bot.event
async def on_member_remove(member):
    for ch in bot.get_guild(member.guild.id).channels:
        if ch.name == 'основной':
            await bot.get_channel(ch.id).send(f'{member.mention}, нам будет тебя не хватать')

# выводит список команд для пользователя
@bot.command()
async def инфо(ctx, arg=None):
    author = ctx.message.author
    if arg == None:
        await ctx.send(f'{author.mention} Введите:\n!инфо общая\n!инфо команды')
    elif arg == 'общая':
        await ctx.send(f'{author.mention} Привет. Я шериф слежу за порядком в чате, а также подрабатываю калькулятором. Третье предупреждение за мат - БАН')
    elif arg == 'команды':
        await ctx.send(f'{author.mention} !статус - мои предупреждения\n!инфо калькулятор - обычный калькулятор')
    elif arg == 'калькулятор':
        await ctx.send(f'{author.mention} Доступны следующие действия после знака "!": \n!сложение\n!вычитание\n!деление\n!умножение\n!корень\nНапиши !сложение 2 2')
    else:
        await ctx.send(f'{author.mention} Такой команды нет')

# отправляет запрос в базу данных на наличение записи о количестве предупреждений
@bot.command()
async def статус(ctx):
    base.execute('CREATE TABLE IF NOT EXISTS {}(userid INT, count INT)'.format(ctx.message.guild.name))
    base.commit()
    warning = cur.execute('SELECT * FROM {} WHERE userid == ?'.format(ctx.message.guild.name),(ctx.message.author.id,)).fetchone()
    if warning is None:
        await ctx.send(f'{ctx.message.author.mention}, у Вас нет предупреждений')
    else:
        await ctx.send(f'{ctx.message.author.mention}, у Вас {warning[1]} предупреждений')

# производит анализ отправленных сообщений в чат
@bot.event
async def on_message(message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation))for i in message.content.split(' ')}\
    .intersection(set(json.load(open('cenz.json')))) != set(): # метод преобразует сообщение в множество и проверяет с помощью пересечения с множеством запрещенных слов из json файла
        await message.channel.send(f'{message.author.mention} ууу... кого по губам отшлепать??')
        await message.delete()
        # создаем базу данных с нарушителями
        name = message.guild.name

        base.execute('CREATE TABLE IF NOT EXISTS {}(userid INT, count INT)'.format(name))
        base.commit()

        warning = cur.execute('SELECT * FROM {} WHERE userid == ?'.format(name),(message.author.id,)).fetchone()

        if warning is None:
            cur.execute('INSERT INTO {} VALUES(?, ?)'.format(name),(message.author.id,1))
            base.commit()
            await message.channel.send(f'{message.author.mention}, первое предупреждение, на третье - БАН!')
        elif warning[1] == 1:
            cur.execute('UPDATE {} SET count == ? WHERE userid == ?'.format(name),(2,message.author.id))
            base.commit()
            await message.channel.send(f'{message.author.mention}, второе предупреждение, на третье - БАН!')
        elif warning[1] == 2:
            cur.execute('UPDATE {} SET count == ? WHERE userid == ?'.format(name),(3,message.author.id))
            base.commit()
            await message.channel.send(f'{message.author.mention}, забанен за мат в чате!')
            await message.author.ban(reason='Нецензурные выражения')

    await bot.process_commands(message) # после того как прошла проверка сообщения на запрещенные слова, бот проверяет данное сообщение на наличие команд

# команды калькулятора

@bot.command()
async def сложение(ctx, x: float, y: float):
    await ctx.send(f'Ответ: {sum(x, y)}')

@bot.command()
async def вычитание(ctx, x: float, y: float):
    await ctx.send(f'Ответ: {sub(x, y)}')

@bot.command()
async def деление(ctx, x: float, y: float):
    await ctx.send(f'Ответ: {div(x, y)}')

@bot.command()
async def корень(ctx, x: float):
    await ctx.send(f'Ответ: {sqrt(x)}')

@bot.command()
async def умножение(ctx, x: float, y: float):
    await ctx.send(f'Ответ: {mylt(x, y)}')

bot.run(config.settings['discord_token'])