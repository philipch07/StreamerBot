import discord
import json
import os

try:
    # for local
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    token = config['bottoken']
    general_channel = config['general_channel']
    bot_commands_channel = config['bot_commands_channel']
    tarkov_settings = config['tarkov_settings']
    nvidia_settings = config['nvidia_settings']
    key_help = config['key_help']
    twitch_page = config['twitch_page']
    streamer = "User"
    # for heroku
except FileNotFoundError:
    token = os.environ['bottoken']

with open('count.txt', 'r') as c:
    count = int(c.read())
c.close()

def incr_count():
    with open('count.txt', 'r') as c:
        count = int(c.read())
    c.close()
    
    count = count + 1
    print(f"Count: {count}")
    
    with open('count.txt', 'w') as c:
        c.write(f'{count}')
    c.close()

class MyClient(discord.Client):
    async def on_ready(self):
        if count == 0:
            await client.change_presence(activity=discord.Game('Awaiting drones to guide.'))
        else:
            await client.change_presence(activity=discord.Game(f'Guiding drones. {count} drones guided.'))
        print('Logged in.')

    async def on_message(self, message):
        if message.author == client.user:
            return

        # responding to stuff in bot-commands channel that's better than what nightbot has to say
        if message.channel.id == general_channel:
            if message.content == '!settings':
                await message.reply(f'{streamer}\'s tarkov settings: <#{tarkov_settings}> \n{streamer}\'s nvidia settings: <#{nvidia_settings}>')
                incr_count()
                with open('count.txt', 'r') as c:
                    count = int(c.read())
                c.close()
                await client.change_presence(activity=discord.Game(f'Guiding drones. {count} drones guided.'))
            elif message.content == '!keys':
                await message.reply(f'You can ask for help with keys in <#{key_help}>. If you\'re looking for what keys they use with certain maps, use `![map name]`.')
                with open('count.txt', 'r') as c:
                    count = int(c.read())
                c.close()
                await client.change_presence(activity=discord.Game(f'Guiding drones. {count} drones guided.'))
                incr_count()
            elif message.content == '!pc':
                await message.reply(f'You can check their specs on their twitch page. Go to {twitch_page} and look at the "Gear" section. This isn\'t always updated, so feel free to ask them when they\'re live on stream!')
                with open('count.txt', 'r') as c:
                    count = int(c.read())
                c.close()
                await client.change_presence(activity=discord.Game(f'Guiding drones. {count} drones guided.'))
                incr_count()
            return

        if message.content.startswith('!'):
            if len(set(message.content)) > 2:
                await message.reply(f'Please use bot commands in <#{bot_commands_channel}>')
                incr_count()
                with open('count.txt', 'r') as c:
                    count = int(c.read())
                c.close()
                await client.change_presence(activity=discord.Game(f'Guiding drones. {count} drones guided.'))
                return

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)