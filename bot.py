import discord
import os
import datetime
from datetime import date
import asyncio

from dotenv import load_dotenv
from discord.ext import commands
from operator import itemgetter
from discord.ext.tasks import loop

load_dotenv('.env')


intents = discord.Intents.default()
intents.members = False
intents.presences = False
intents.messages = True

bot = commands.Bot(command_prefix="$", intents=intents)
# client = discord.Client(intents=intents)

XMAS_DATE = date(year=(date.today().year if date.today().month <= 12 and date.today().day <= 24 else date.today().year + 1), month=12, day=24)
countdown = XMAS_DATE - date.today()
days_left_msg = f"Days left until Xmas: {countdown.days}"

@bot.event
async def on_message(message):
  await bot.process_commands(message)

@bot.event
async def on_ready():
  print("Logged in as")
  print(bot.user.name + " #" + bot.user.discriminator)
  print(days_left_msg)
  print("------")
  await wait_for_xmas_cancel()
  await asyncio.sleep(0.01)
  await wait_for_xmas_start()
  await asyncio.sleep(1)
  await daily_xmas_check_cancel()
  await asyncio.sleep(0.01)
  await daily_xmas_check_start()

@bot.command()
async def days_left_until_xmas(ctx):
  print("days_left_until_xmas")
  await ctx.send(days_left_msg)


@loop(hours=1)
async def wait_for_xmas():
  if countdown.days == 0:
    for guild in bot.guilds:
      for channel in guild.channels:
        if "chat" in channel.name or "general" in channel.name:
          await channel.send("It's Xmas @everyone https://tenor.com/view/gabdro-gabriel-dropout-vignette-raphiel-merry-christmas-gif-19695324")

async def wait_for_xmas_cancel():
  wait_for_xmas.cancel()

async def wait_for_xmas_start():
  wait_for_xmas.start()

@bot.command()
async def dont_wait_for_xmas_time():
  await wait_for_xmas_cancel()


@loop(hours=24)
async def daily_xmas_check():
  for guild in bot.guilds:
    for channel in guild.channels:
      if "spam" in channel.name:
        await channel.send(days_left_msg)
  print("test")

async def daily_xmas_check_cancel():
  daily_xmas_check.cancel()

async def daily_xmas_check_start():
  daily_xmas_check.start()

@bot.command()
async def dont_do_daily_xmas_check():
  await daily_xmas_check_cancel()


bot.run(os.getenv('TOKEN'))

# client.run(os.getenv('TOKEN'))

# Update this bot to work with slash commands
# https://discordpy.readthedocs.io/en/latest/ext/commands/slash.html

# @bot.slash_command()
# async def days_left_until_xmas(ctx):
#     await ctx.send(days_left_msg)

# @bot.slash_command()
# async def dont_wait_for_xmas_time(ctx):
#   await wait_for_xmas_cancel()

# @bot.slash_command()
# async def dont_do_daily_xmas_check(ctx):
#   await daily_xmas_check_cancel()

# bot.run(os.getenv('TOKEN'))
