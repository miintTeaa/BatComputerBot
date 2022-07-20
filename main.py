import os
import discord
from command import command_list
import advice.advice
assert advice # silences pyflakes unused warning

client = discord.Client()

prefix = "b;"

@client.event
async def on_ready():
  print("We have liftoff!")
  print("user: {}".format(client.user.name))
  print("id: {}".format(client.user.id))

@client.event
async def on_message(message):
  if (message.author == client.user):
    return;
  if (message.content.startswith(prefix)):
    await process_command(message)

async def process_command(message):
  args = message.content.split()
  command = command_list[args[0].replace(prefix, "")]
  amax = command.arg_max
  amin = command.arg_min
  if await validate_arg_size(message.channel, len(args) - 1, amin, amax):
    await command.function(message, args[1:])
    name = message.author.name+"#"+message.author.discriminator
    print("> {} executed command {}".format(name, args[0]))
    print("| {}".format(message.content))

async def validate_arg_size(channel, arg_len, amin, amax):
  if amin == -1 and amax == -1:
    return True
  if amin == -1 and arg_len > amax:
    await channel.send("Expected {} arguments or less.".format(amax))
    return False
  if amax == -1 and arg_len < amin:
    await channel.send("Expected {} arguments or more.".format(amin))
    return False
  if arg_len < amin and arg_len > amax:
    await channel.send("Expected {}-{} arguments.".format(amin, amax))
    return False
  return True

token = os.environ['TOKEN']
try:
  client.run(token)
except:
  os.system("kill 1")