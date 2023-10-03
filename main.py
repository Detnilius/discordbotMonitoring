from config import botToken, messageID, channelID

import cs2dServer

import datetime
import asyncio
import discord
from discord.ext import commands, tasks

servers = [
    cs2dServer.Server('18.229.40.57', 36963),
    cs2dServer.Server('18.229.40.57', 36964),
    cs2dServer.Server('18.229.40.57', 36965),
    cs2dServer.Server('18.229.40.57', 36966),
    cs2dServer.Server('18.229.40.57', 36967),
]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Бот {bot.user.name} подключен')
    send_data.start()

@tasks.loop(minutes=1)
async def send_data():
    await asyncio.gather(*[srv.update() for srv in servers])
    
    channel = bot.get_channel(channelID)

    if channel:
        
        embeds = []

        for srv in servers:
            
            title = f'> **Offline**'
            text = ''

            if srv.status == 'Online':
                title = f'> **{srv.name}**'

                text += f'```Map:      {srv.map}\n'
                text += f'Players:  {srv.players}\n'
                text += f'Gamemode: {srv.gamemode}```\n'
            
            text += f'```{srv.address}```\n'

            color = 0x00ff00 if srv.status == 'Online' else 0xff0000
            timestamp = datetime.datetime.now() if srv == servers[-1] else None

            emd = discord.Embed(title=title, description=text, color=color, timestamp=timestamp)
            embeds.append(emd)
        
        global messageID

        try:
            message = await channel.fetch_message(messageID)
            await  message.edit(embeds=embeds)
        except discord.errors.NotFound:
            new_message = await channel.send(embeds=embeds)
            messageID = new_message.id
    else:
        print('Channel not found!')


bot.run(botToken)
