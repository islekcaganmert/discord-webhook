import os
import discord
import json
import requests

TOKEN = open('./.env', 'rb').read().decode('UTF-8').splitlines()[0].split('=')[1]
client = discord.Client()
db = json.load(open('./db.json', 'rb'))


def save():
  with open('./db.json', 'wb') as f:
    f.write(json.dumps(db).encode('UTF-8'))


@client.event
async def on_ready():
  print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
  if message.content.startswith('hey webhook! '):
    cmds = message.content[len('hey webhook! '):].splitlines()
    for cmd in cmds:
      if cmd == 'init server':
        db.update({message.guild.id: ['announcements', 'https://example.com/webhook']})
        save()
        await message.channel.send('server initialized, you must set channel and hook now.')
      
      elif cmd.startswith('set channel to '):
        db[message.guild.id][0] = cmd[len('set channel to '):]
        save()
        await message.channel.send('source set to #' + cmd[len('set channel to '):])
      
      elif cmd.startswith('what is '):
        await message.channel.send(db[str(message.guild.id)][{
          'channel': 0,
          'hook': 1
        }[cmd[len('what is '):]]])
      
      elif cmd.startswith('set hook to '):
        db[message.guild.id][1] = cmd[len('set hook to '):]
        save()
        await message.channel.send('hook set to ' + cmd[len('set channel to '):])
      
      elif cmd == 'which server is it?':
        await message.channel.send(message.guild.id)
      
  else:
    if message.author != client.user:
      if message.channel.name == db[str(message.guild.id)][0]:
        payload = {
          'content': message.content,
          'username': message.guild.name,
          'avatar_url': str(message.guild.icon_url)
        }
        r = await requests.post(db[str(message.guild.id)][1], json=payload)
        await message.channel.send(r.status_code)
      else:
        print(message.channel.name + '\n' + db[str(message.guild.id)][0])

client.run(TOKEN)
