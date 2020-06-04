import os
import io
import time
import KanjiScraper
import discord
from discord.ext import commands
from dotenv import load_dotenv
from cairosvg import svg2png
from PIL import Image

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot('!')

@bot.event
async def on_ready():
    print('CONNECTED TO DISCORD.')

@bot.command()
async def kanji(ctx, *args):
    flags = {i for i in args if i.startswith('#')}
    kanjiPhrase = ' '.join([i for i in args if i not in flags])
    results = KanjiScraper.get_kanji(kanjiPhrase)

    for kanji, kanjiData in results.items():
        toSend = ''
        toSend += '-------------------------------------------------------------------- \n'
        toSend += f'**DATA ON {kanji}**' + '\n'

        toSend = [JoinYomis(toSend, kanjiData)]
        if '#translations' in flags:
            AppendTranslations(toSend, kanjiData)
        if '#readings' in flags:
            AppendReadingCompounds(toSend, kanjiData)

        for section in toSend:
            await ctx.send(section)

        await SendStrokeOrderDiagram(ctx, kanjiData, kanji)

@bot.command()
async def joinVoice(ctx, vc : discord.VoiceChannel):
    ctx.bot.voiceBoi = await vc.connect()

@bot.command()
async def leave(ctx):
    await ctx.bot.voiceBoi.disconnect()

def JoinYomis(toSend, kanjiData):
    toSend += '**KUNYOMI**' + '\n'
    for kun in kanjiData.kunyomi:
        toSend += '> ' + kun + '\n'
    toSend += '**ONYOMI**' + '\n'
    for on in kanjiData.onyomi:
        toSend += '> ' + on + '\n'
    return toSend

def AppendTranslations(toSend, kanjiData):
    toSend.append('**TRANSLATIONS**' + '\n')
    for translation in kanjiData.translations:
        toSend.append('> ' + translation + '\n')

def AppendReadingCompounds(toSend, kanjiData):
    toSend.append('**KUNYOMI READING COMPOUNDS**' + '\n')
    for i, readingCompound in enumerate(kanjiData.kunReadingCompounds):
        toSend.append(readingCompound.replace('\n', '> ', 1).replace('\n', ' ') + '\n')
    toSend.append('**ONYOMI READING COMPOUNDS**' + '\n')
    for i, readingCompound in enumerate(kanjiData.onReadingCompounds):
        toSend.append(readingCompound.replace('\n', '> ', 1).replace('\n', ' ') + '\n')

async def SendStrokeOrderDiagram(ctx, kanjiData, kanji):
    with io.BytesIO() as png:
        # Convert strokeOrderDiagram SVG to PNG
        svg2png(bytestring=kanjiData.strokeOrderDiagram, write_to=png)
        png.seek(0)

        await ctx.send(file=discord.File(png, f'{kanji}.png'))


bot.run(token)