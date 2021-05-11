import discord
import random
import os

from keep_alive import keep_alive

client = discord.Client()

narration = ""

def check_max(roll, skill, diff):
  if roll<=skill:
    return "SUCCESS"
  elif roll >= diff:
    return "PASS"
  else:
    return "FAIL"

def check_min(roll, skill, diff):
  if roll<=skill:
    return "A GAIN"
  elif roll >= diff:
    return "NO COST"
  else:
    return "A LOSS"

def findBest(rolls, skill):
  if rolls[1] <= skill:
      bestResult = rolls[1]
  else:
      bestResult = rolls[0]
  return bestResult

def eval(rolls, skill, diff, effort):
  rolls.sort(reverse = True)
  
  if rolls[1] == 0:
    narration = "and NARRATION!"
  else:
    narration = ""

  if effort == True:
    return "Skill = {sk}, Diff = {df}. Rolls: {maxr},{minr} --> {maxresult} with exhaustion {narr}".format(
              sk = skill,
              df = diff,
              maxr = rolls[0],
              minr = rolls[1],
              maxresult = check_max(findBest(rolls, skill), skill, diff),
              narr = narration
              )
  else:          
    return "Skill = {sk}, Diff = {df}. Rolls: {maxr},{minr} --> {maxresult} with {minresult} {narr}".format(
              sk = skill,
              df = diff,
              maxr = rolls[0],
              minr = rolls[1],
              maxresult = check_max(rolls[0], skill, diff),
              minresult = check_min(rolls[1], skill, diff),
              narr = narration
              )

def twod10():
  return [random.randint(0, 9), random.randint(0, 9)]


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('!hello'):
        await message.channel.send('Hello!')

    if msg.startswith("!roll"):
        params = msg.split("!roll ",1)[1].strip()

        effort = False

        if "vs" in params:
          variables = params.split("vs",1)
        elif "v" in params:
          variables = params.split("v",1)
        elif "e" in params:
          variables = params.split("e",1)
          effort = True
        else: 
          variables = params

        variables = [int(i) for i in variables]

        skill = variables[0]

        if len(variables) > 1:
          diff = int(variables[1])
        else:
          diff = 6

        rolls = twod10()
        await message.channel.send(eval(rolls, skill, diff, effort))

    if msg.startswith("!eval"):
        params = msg.split("!eval ",1)[1]
        
        #!eval 3,2 1vs7
        variables = params.split(",")

        skill = variables[2]
        rolls = variables[:2]
        rolls = [int(i) for i in rolls]

        rolls.sort(reverse = True)
        
        await message.channel.send("Rolls: {maxr},{minr} --> {maxresult} with {minresult}".format(
                    maxr = rolls[0],
                    minr = rolls[1],
                    maxresult = check_max(rolls[0]),
                    minresult = check_min(rolls[1])
                    )) 

keep_alive()
client.run(os.getenv('TOKEN'))