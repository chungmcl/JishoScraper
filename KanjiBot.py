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
    messageContents = message.content.strip()
    if '!kanji' in messageContents[0:6]:
        flags = messageContents
        toSearch = messageContents[messageContents.find('!kanji'):len(messageContents)]
        results = KanjiScraper.get_kanji(toSearch)

        for kanji, kanjiData in results.items():
            toSend = list()
            toSend.append('-------------------------------------------------------------------- \n')
            toSend.append(f'**DATA ON {kanji}**' + '\n')

            AppendYomis(toSend, kanjiData)
            AppendTranslations(toSend, kanjiData)
            AppendReadingCompounds(toSend, kanjiData)

            toSend = ''.join(toSend)
            await message.channel.send(toSend)

            await SendStrokeOrderDiagram(message, kanjiData, kanji)

def AppendYomis(toSend, kanjiData):
    toSend.append('**KUNYOMI**' + '\n')
    for kun in kanjiData.kunyomi:
        toSend.append('> ' + kun + '\n')
    toSend.append('**ONYOMI**' + '\n')
    for on in kanjiData.onyomi:
        toSend.append('> ' + on + '\n')

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

async def SendStrokeOrderDiagram(message, kanjiData, kanji):
    with io.BytesIO() as png:
        # Convert strokeOrderDiagram SVG to PNG
        svg2png(bytestring=kanjiData.strokeOrderDiagram, write_to=png)
        png.seek(0)

        await message.channel.send(file=discord.File(png, f'{kanji}.png'))


client.run(token)