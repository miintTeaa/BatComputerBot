import requests
import json
from replit import db

advice_api = "https://api.adviceslip.com/advice"

# b;advice
async def send_advice(message):
  channel = message.channel
  response = requests.get(advice_api)
  slip = json.loads(response.text)["slip"]

  if id == "" and is_blocked(slip["id"]):
    await send_advice(channel)
  else:
    await channel.send("{}: {}".format(slip["id"], slip["advice"]))

async def send_advice_id(message, id):
  channel = message.channel
  
  if is_blocked(id):
    await channel.send("This advice was blacklisted.")
    return

  if not id.isnumeric():
    await channel.send("Expected an integer argument.")
    return
  
  try:
    response = requests.get(advice_api+"/"+id)
    slip = json.loads(response.text)["slip"]
    await channel.send("{}: {}".format(slip["id"], slip["advice"]))
  except KeyError:
    await channel.send("Could not find advice #{}.".format(id))
  except json.JSONDecodeError:
    await channel.send("Unknown error.")

# b;badvice
async def send_badvice_list(channel):
  str = "List of blacklisted advice: \n"
  for key in db.keys():
    if key.startswith("block_adv"):
      str += "- {}: \"{}\"\n".format(key.replace("block_adv", ""), db[key])
  await channel.send(str)

# Utility
def block_key(advice_id):
  return "block_adv{}".format(advice_id)

def is_blocked(advice_id):
  key = block_key(advice_id)
  return key in db.keys()

def extract_message(str):
  index = str.find(" ", str.find(" ") + 1) + 1
  return str[index:]
