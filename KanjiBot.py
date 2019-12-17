import os
import io
import KanjiScraper
import discord
from dotenv import load_dotenv
from cairosvg import svg2png

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

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
                svg2png(bytestring=kanjiData.strokeOrderDiagram, write_to=png)
                png.seek(0)
                await message.channel.send(file=discord.File(fp, f'{kanji}.png'))
            #with kanjiData.strokeOrderDiagram as fp:
             #   await message.channel.send(file=discord.File(fp, 'strokeOrder.svg'))

client.run(token)