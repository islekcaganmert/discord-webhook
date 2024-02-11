import os
import discord
import json
import requests

intents = discord.Intents.default()
intents.message_content = True
TOKEN = open('./.env', 'rb').read().decode('UTF-8').splitlines()[0].split('=')[1]
client = discord.Client(intents=intents)
db = json.load(open('./db.json', 'rb'))


def save():
    with open('./db.json', 'wb') as f:
        f.write(json.dumps(db).encode('UTF-8'))


async def send_payload(url, payload):
    requests.post(url, json=payload)



@client.event
async def on_ready():
  print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.content.startswith('hey webhook! '):
        cmds = message.content[len('hey webhook! '):].splitlines()
        for cmd in cmds:
            if cmd == 'init server':
                db.update({str(message.guild.id): ['announcements', 'https://example.com/webhook', 'https://discord.com/assets/847541504914fd33810e70a0ea73177e.ico']})
                save()
                await message.channel.send('server initialized, you must set channel and hook now.')

            elif cmd.startswith('set channel to '):
                db[str(message.guild.id)][0] = cmd[len('set channel to '):]
                save()
                await message.channel.send('source set to #' + cmd[len('set channel to '):])

            elif cmd.startswith('what is '):
                await message.channel.send(db[str(message.guild.id)][{
                    'channel': 0,
                    'hook': 1,
                    'avatar': 2
                }[cmd[len('what is '):]]])

            elif cmd.startswith('set hook to '):
                db[str(message.guild.id)][1] = cmd[len('set hook to '):]
                save()
                await message.channel.send('hook set to ' + cmd[len('set hook to '):])

            elif cmd.startswith('set avatar to '):
                db[str(message.guild.id)][1] = cmd[len('set avatar to '):]
                save()
                await message.channel.send('avatar set to ' + cmd[len('set avatar to '):])

            elif cmd == 'which server is it?':
                await message.channel.send(message.guild.id)

    else:
        if message.author != client.user:
            try:
                if message.channel.name == db[str(message.guild.id)][0]:
                    payload = {
                        'content': message.content,
                        'username': message.guild.name,
                        'avatar_url': db[str(message.guild.id)][2]
                    }
                    _ = await send_payload(db[str(message.guild.id)][1], payload)
            except KeyError:
                pass

client.run(TOKEN)
