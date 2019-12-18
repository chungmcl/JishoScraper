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
    strokeOrderDiagram = strokeOrderDiagram.replace('width="109" height="109"', 'width="909" height="909"')
    svg2png(bytestring=strokeOrderDiagram, write_to=png)
    png.seek(0)

    img = Image.open(png)
    png.seek(0)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[3] == 0:
            newData.append((255, 255, 255, 255))
        else:
            newData.append(item)

    img.putdata(newData)
    #img.save('/Users/chungmcl/Downloads/test.png')
    # This doesn't work for some reason - Discord can't process it for some reason
    img.save(png, 'PNG')
    png.seek(0)

client.run(token)