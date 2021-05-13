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

        #extract skill and diff
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

        #set diff if passed (default 6)
        if len(variables) > 1:
          diff = int(variables[1])
        else:
          diff = 6

        rolls = twod10()
        await message.channel.send(eval(rolls, skill, diff, effort))

    if msg.startswith("!eval"):
        #!eval 3,2 1vs7
        full_params = msg.split("!eval ",1)[1]
                
        variables = full_params.split(" ")

        #get the rolls, variables[0] = 3,8
        rolls = variables[0].split(",")
        rolls = [int(i) for i in rolls] #convert to int
        rolls.sort(reverse = True)
        #get the skill and diff
        #variables[1]: 2v7
        params = variables[1]
        effort = False

        #extract skill and diff
        if "vs" in params:
          variables = params.split("vs",1)
        elif "v" in params:
          variables = params.split("v",1)
        elif "e" in params:
          variables = params.split("e",1)
          effort = True
        else: 
          variables = params

        variables = [int(i) for i in variables]  #convert to int
        skill = variables[0]

        #set diff if passed (default 6)
        if len(variables) > 1:
          diff = int(variables[1])
        else:
          diff = 6
                
        await message.channel.send(eval(rolls, skill, diff, effort))

keep_alive()
client.run(os.getenv('TOKEN'))