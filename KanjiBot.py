import os
import io
import time
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
    delimiterEnglishSpace = messageContents.find(' ')
    delimiterJapaneseSpace = messageContents.find('　')
    delimiter = ''
    if delimiterEnglishSpace >= 0 and delimiterJapaneseSpace >= 0: 
        delimiter = min(delimiterEnglishSpace, delimiterJapaneseSpace)
    elif delimiterEnglishSpace < 0 and delimiterJapaneseSpace >= 0:
        delimiter = delimiterJapaneseSpace
    elif delimiterEnglishSpace >= 0 and delimiterJapaneseSpace < 0:
        delimiter = delimiterEnglishSpace
    
    if '!kanji' in messageContents[0:6] and delimiter >= 0:
        flags = messageContents[6:delimiter]
        flagList = flags.split('#')
        toSearch = messageContents[delimiter:len(messageContents)]
        results = KanjiScraper.get_kanji(toSearch)

        for kanji, kanjiData in results.items():
            toSend = ''
            toSend += '-------------------------------------------------------------------- \n'
            toSend += f'**DATA ON {kanji}**' + '\n'

            toSend = [JoinYomis(toSend, kanjiData)]
            if 'translations' in flagList:
                AppendTranslations(toSend, kanjiData)
            if 'readings' in flagList:
                AppendReadingCompounds(toSend, kanjiData)

            for section in toSend:
                await message.channel.send(section)

            await SendStrokeOrderDiagram(message, kanjiData, kanji)
            time.sleep(0.20)

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

async def SendStrokeOrderDiagram(message, kanjiData, kanji):
    with io.BytesIO() as png:
        # Convert strokeOrderDiagram SVG to PNG
        svg2png(bytestring=kanjiData.strokeOrderDiagram, write_to=png)
        png.seek(0)

        await message.channel.send(file=discord.File(png, f'{kanji}.png'))


client.run(token)