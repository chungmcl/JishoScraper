import os
import io
import KanjiScraper
import discord
from dotenv import load_dotenv
from cairosvg import svg2png
from PIL import Image

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print('CONNECTED TO DISCORD.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    messageContents = message.content
    if '!kanjiBot' in messageContents:
        toSearch = messageContents[messageContents.find('!kanjiBot'):len(messageContents)]
        results = KanjiScraper.get_kanji(toSearch)
        for kanji, kanjiData in results.items():
            toSend = list()
            toSend.append('-------------------------------------------------------------------- \n')
            toSend.append(f'**DATA ON {kanji}**' + '\n')
            toSend.append('**KUNYOMI**' + '\n')
            for kun in kanjiData.kunyomi:
                toSend.append('> ' + kun + '\n')
            toSend.append('**ONYOMI**' + '\n')
            for on in kanjiData.onyomi:
                toSend.append('> ' + on + '\n')
            toSend.append('**TRANSLATIONS**' + '\n')
            for translation in kanjiData.translations:
                toSend.append('> ' + translation + '\n')
            toSend.append('**KUNYOMI READING COMPOUNDS**' + '\n')
            for i, readingCompound in enumerate(kanjiData.kunReadingCompounds):
                toSend.append(readingCompound.replace('\n', '> ', 1).replace('\n', ' ') + '\n')
            toSend.append('**ONYOMI READING COMPOUNDS**' + '\n')
            for i, readingCompound in enumerate(kanjiData.onReadingCompounds):
                toSend.append(readingCompound.replace('\n', '> ', 1).replace('\n', ' ') + '\n')
            toSend = ''.join(toSend)
            await message.channel.send(toSend)

            with io.BytesIO() as png:
                ReformatStrokeOrderDiagram(kanjiData.strokeOrderDiagram, png)
                await message.channel.send(file=discord.File(png, f'{kanji}.png'))

def ReformatStrokeOrderDiagram(strokeOrderDiagram, png):
    strokeOrderDiagram = strokeOrderDiagram.replace('<svg xmlns="http://www.w3.org/2000/svg" width="109" height="109" viewBox="0 0 109 109">', 
    '<svg xmlns="http://www.w3.org/2000/svg" width="909" height="909" viewBox="0 0 109 109">\n<rect width="100%" height="100%" fill="white" /> ')
    svg2png(bytestring=strokeOrderDiagram, write_to=png)
    png.seek(0)

client.run(token)