import os
import KanjiScraper
import discord
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    messageContents = message.content
    if '!kanjiBot' in messageContents:
        toSearch = messageContents[messageContents.find('!kanjiBot'):len(messageContents)]
        results = KanjiScraper.get_kanji(toSearch)
        for kanjiData in results.values():
            print(type(kanjiData))
            await message.channel.send(kanjiData.kunyomi)
            await message.channel.send(kanjiData.onyomi)
            await message.channel.send(kanjiData.translations)
            await message.channel.send(kanjiData.kunReadingCompounds)
            await message.channel.send(kanjiData.onReadingCompounds)
            await message.channel.send(kanjiData.strokeOrderDiagram)
            with kanjiData.strokeOrderDiagram as fp:
                await message.channel.send(file=discord.File(fp, 'strokeOrder.svg'))


client.run(token)