from command import Command
from advice.advice_extra import send_advice
from advice.advice_extra import send_advice_id
from advice.advice_extra import send_badvice_list
from advice.advice_extra import block_key
from advice.advice_extra import extract_message

from replit import db

# Command functions

#b;advice
async def show_advice(message, args):
  if len(args) == 0:
    await send_advice(message)
  else:
    await send_advice_id(message, args[0])

#b;badvice
async def block_advice(message, args):
  advice_id = args[0]
  channel = message.channel

  if advice_id == "list":
    await send_badvice_list(message.channel)
    return
  if not advice_id.isnumeric():
    await channel.send("Expected an integer argument.")
    return
  
  key = block_key(advice_id)
  
  if key in db.keys():
    await channel.send("Advice already blocked.")
  else:
    await channel.send("Blocked advice #{}.".format(advice_id))
    if len(args) > 1:
      db[key] = extract_message(message.content)
    else:
      db[key] = "No reason given."

#b;ubadvice
async def unblock_advice(message, args):
  advice_id = args[0]
  channel = message.channel
  
  if not advice_id.isnumeric():
    await channel.send("Expected an integer argument.")
    return
  
  key = block_key(advice_id)
  
  if key in db.keys():
    await channel.send("Unblocked advice #{}.".format(advice_id))
    del db[key]
  else:
    await channel.send("Advice not blocked.")

# Creating commands

show_advice = Command("advice", show_advice, 0, 1)
blacklist_advice = Command("badvice", block_advice, 1, -1)
unblacklist_advice = Command("ubadvice", unblock_advice, 1, 1)
