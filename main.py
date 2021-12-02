import os
import disnake
import disnake as discord
from typing import *
from urllib import parse, request
from disnake.ext.commands import Context, ctx_menus_core
import re
import json
import GetLyrics_ATRS_SelfBot
from disnake.ext.commands.params import Param
from disnake.ext import commands
import typehint
from disnake_together import DisnakeTogether
import requests
from dotenv import load_dotenv
import time
import io
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta
import aiohttp
import bs4
from simpcalc import simpcalc 
from bs4 import BeautifulSoup as bs4
import asyncio
asyncio.get_event_loop().set_debug(True)
load_dotenv()

with open('config.json') as f:
    config = json.load(f)

with open('help.json') as l:
    helpl = json.load(l)

waifuim= {'User-Agent':f'aiohttp/{aiohttp.__version__}; YourAppName'}
bot_embed_color = 0x4548a8
prefix = config.get('prefix')
cuttly_key = config.get('cuttly_key')
NASA_API_KEY = config.get('NASA_API_KEY')
token = os.getenv("token")
cat_key = config.get('cat_key')
weather_key = config.get('weather_key')
intents = disnake.Intents().all()
bitly_key = config.get('bitly_key')
bot = commands.Bot(command_prefix=commands.when_mentioned_or('Luv', 'Eru', 'eru', 'luv', 'love', 'Love'), strip_after_prefix = True, intents = intents, sync_commands_debug=True, case_insensitive=True)
together_control = DisnakeTogether(bot)
bot.remove_command('help')

@bot.event
async def on_ready():
  print("Bot is ready")

@bot.event
async def on_guild_join(guild):
    general = guild.text_channels[0]
    if general and general.permissions_for(guild.me).send_messages:
        embed=discord.Embed(title="**======== *Thanks For Adding Me!* ========**", description=f"""
        Thanks for adding me to {guild.name}!
        You can use the `luv help` command to get started!
	I hope we can have a great time together
        """, color=bot_embed_color)
        await general.send(embed=embed)

@bot.event
async def on_command_error(ctx,error):
  if isinstance(error,commands.CommandOnCooldown):
    msg='***Still on Cooldown**, please try again in {:.2f}s'.format(error.retry_after)
    await ctx.send(msg)
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f"Missing arguemnts!! Please try again with proper arguments. Error - {error}")
  else:
    raise(error)

@bot.command()
async def kick(ctx, target: disnake.Member = None, *,reason: str = None):
    if ctx.author.guild_permissions.kick_members:
        if target is None:
            embed = disnake.Embed(description="Cannot kick cause member is not mentioned. ", color=bot_embed_color)
            await ctx.reply(embed=embed)
            return
        if target == ctx.author:
            embed = disnake.Embed(description="You cannot kick yourself. ", color=bot_embed_color)
            await ctx.reply(embed=embed)
            return
        if target == ctx.guild.owner:
            embed = disnake.Embed(description="You cannot kick the guild owner.", color=bot_embed_color)
            await ctx.reply(embed=embed)
            return
        if target.bot:
            embed = disnake.Embed(description="You cannot kick any bot.", color=bot_embed_color)
            await ctx.reply(embed=embed)
            return

        # Kicking member part
        await target.kick(reason=str(reason))

        if reason is None:
            embed = disnake.Embed(description=f"{target.mention} has been kicked successfully by {ctx.author.mention} "
                                              f"without any given reason. ", color=bot_embed_color)
        else:
            embed = disnake.Embed(description=f"{target.mention} has been kicked successfully by {ctx.author.mention}. "
                                              f"\nReason given: {reason}", color=bot_embed_color)
        await ctx.reply(embed=embed)
    else:
        embed = disnake.Embed(description=f"Cannot kick {target.mention} cause {ctx.author.mention} "
                                          f"do not have the permissions to kick members. ", color=bot_embed_color)
        await ctx.reply(embed=embed)

@bot.command()
async def ban(ctx, target: disnake.Member = None, *, reason: str = None):
    if ctx.author.guild_permissions.ban_members:
        if target is None:
            embed = disnake.Embed(description="Cannot ban cause member is not mentioned.", color=bot_embed_color)
            await ctx.reply(embed=embed)
            return
        if target == ctx.author:
            embed = disnake.Embed(description="You cannot ban yourself. ", color=bot_embed_color)
            await ctx.reply(embed=embed)
            return
        if target == ctx.guild.owner:
            embed = disnake.Embed(description="You cannot ban the server owner. ", color=bot_embed_color)
            await ctx.reply(embed=embed)
            return
        if target.bot:
            embed = disnake.Embed(description="You cannot ban any bot.", color=bot_embed_color)
            await ctx.reply(embed=embed)
            return

        # banning member part
        await target.ban(reason=str(reason))

        if reason is None:
            embed = disnake.Embed(description=f"{target.mention} has been banned successfully by {ctx.author.mention} "
                                              f"without any given reason. ", color=bot_embed_color)
        else:
            embed = disnake.Embed(description=f"{target.mention} has been banned successfully by {ctx.author.mention}. "
                                              f"\nReason given: `{reason}`", color=bot_embed_color)
        await ctx.reply(embed=embed)
    else:
        embed = disnake.Embed(description=f"Cannot ban {target.mention} cause {ctx.author.mention} "
                                          f"do not have the permissions to ban members. ", color=bot_embed_color)
        await ctx.reply(embed=embed)

@bot.command()
async def unban(ctx, user: str = None):
    member = user
    if ctx.author.guild_permissions.ban_members:
        if member is None:
            embed = disnake.Embed(description=f"Cannot unban cause member is not provided. \nFormat: ` "
                                              "member_with_discriminator#9999` ", color=bot_embed_color)
            await ctx.reply(embed=embed)
            return
        banned_users = await ctx.guild.bans()

        try:
            member_name, member_discriminator = member.split('#')
        except:
            embed = disnake.Embed(description=f"Cannot unban cause member format is not correct. \nFormat: `"
                                              "member_with_discriminator#9999` ", color=bot_embed_color)
            await ctx.reply(embed=embed)
            return

        unbanned_users = 0
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                # unbanning member part
                embed = disnake.Embed(description=f"`{member}` has been successfully unbanned by {ctx.author.mention}.",
                                      color=bot_embed_color)
                await ctx.reply(embed=embed)
                unbanned_users += 1
                break

        if unbanned_users == 0:
            embed = disnake.Embed(description=f"No one is unbanned as `{member}` is not found in server ban list. ",
                                  color=bot_embed_color)
            await ctx.reply(embed=embed)

    else:
        embed = disnake.Embed(description=f"Cannot unban {member} cause {ctx.author.mention} "
                                          f"do not have the permissions to ban/unban members. ", color=bot_embed_color)
        await ctx.reply(embed=embed)

@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: disnake.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = disnake.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = disnake.Embed(title="muted", description=f"{member.mention} was muted ", colour=disnake.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" you have been muted from: {guild.name} reason: {reason}")

@bot.command()
async def kiss(ctx, mentioned_member: disnake.Member = None):
    r = requests.get("https://api.waifu.pics/sfw/kiss")
    res = r.json()
    em = disnake.Embed(description=f"**{str(ctx.author.mention)} _kisses_ {str(mentioned_member.mention)}**")    
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@bot.slash_command(
    name="kiss",
    description="Kisses the given member😘"
    )
async def kiss(
    inter: disnake.ApplicationCommandInteraction,
    member: disnake.Member = Param(
        description="The member to kiss")
    ):
    r = requests.get("https://api.waifu.pics/sfw/kiss")
    res = r.json()
    em = disnake.Embed(description=f"**{str(inter.user.mention)} _kisses_ {str(member.mention)}**") 
    em.set_image(url=res['url'])
    await inter.response.send_message(embed=em)

@bot.command()
async def hug(ctx, mentioned_member: disnake.Member = None):
  try:
    r = requests.get("https://api.waifu.pics/sfw/hug")
    res = r.json()
    em = disnake.Embed(description=f"**{str(ctx.author.mention)} _hugs_ {str(mentioned_member.mention)}**") 
    em.set_image(url=res['url'])
    await ctx.send(embed=em)
  except:
    r = requests.get("https://api.waifu.pics/sfw/hug")
    res = r.json()
    em = disnake.Embed(description=f"**Hina hugs {str(ctx.author.mention)} cuz you didn't mention anyone to hug!  ;-;**") 
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@bot.slash_command(
    name="hug",
    description="Hugs the given member"
    )
async def hug(
    inter: disnake.ApplicationCommandInteraction,
    member: disnake.Member = Param(
        description="The member to hug")
    ):
    r = requests.get("https://api.waifu.pics/sfw/hug")
    res = r.json()
    em = disnake.Embed(description=f"**{str(inter.user.mention)} _hugs_ {str(member.mention)}**") 
    em.set_image(url=res['url'])
    await inter.response.send_message(embed=em)

@bot.command()
async def recipe(ctx, *, food_name):
    food = food_name.replace(" ", "+")
    api_url = "https://api.edamam.com/api/recipes/v2?type=public&q=" + food + "&app_id=6c255cd9&app_key=%205962a391f3b2c29e43c8c6af5e9fa2c9%09"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as resp:
            res = await resp.json()
    ing = res['hits'][0]['recipe']['ingredients']
    naam = res["hits"][0]["recipe"]["label"]
    url = res["hits"][0]["recipe"]["url"]
    inge = ""
    for ingredient in ing:
        inge += f"{ingredient['text']}\n-------\n"
    embed = disnake.Embed(title=naam, url=url, description=inge, color=bot_embed_color)
    await ctx.reply(embed=embed)

@bot.command()
async def cuddle(ctx, mentioned_member: disnake.Member = None):
  try:
    r = requests.get("https://api.waifu.pics/sfw/cuddle")
    res = r.json()
    em = disnake.Embed(description=f"**{str(ctx.author.mention)} _cuddles with_ {str(mentioned_member.mention)}**") 
    em.set_image(url=res['url'])
    await ctx.send(embed=em)
  except:
    r = requests.get("https://api.waifu.pics/sfw/cuddle")
    res = r.json()
    em = disnake.Embed(description=f"**Hina _cuddles with_ {str(ctx.author.mention)} cuz you didn't mention anyone to cuddle with!  :)**") 
    em.set_image(url=res['url'])
    await ctx.send(embed=em)


@bot.slash_command(
    name="cuddle",
    description="Cuddles with the given member"
    )
async def cuddle(
    inter: disnake.ApplicationCommandInteraction,
    member: disnake.Member = Param(
        description="The member to bully")
    ):
    r = requests.get("https://api.waifu.pics/sfw/cuddle")
    res = r.json()
    em = disnake.Embed(description=f"**{str(inter.user.mention)} _cuddles with_ {str(member.mention)}**") 
    em.set_image(url=res['url'])
    await inter.response.send_message(embed=em)

@bot.command()
async def pat(ctx, mentioned_member: disnake.Member = None):
    r = requests.get("https://api.waifu.pics/sfw/pat")
    res = r.json()
    em = disnake.Embed(description=f"**{str(ctx.author.mention)} _pats_ {str(mentioned_member.mention)}**") 
    em.set_image(url=res['url'])
    await ctx.send(embed=em)


@bot.command()
async def cry(ctx):
    r = requests.get("https://api.waifu.pics/sfw/cry")
    res = r.json()
    em = disnake.Embed(description=f"**{str(ctx.author.mention)} _cries_**") 
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@bot.command()
async def highfive(ctx, mentioned_member: disnake.Member = None):
    r = requests.get("https://api.waifu.pics/sfw/highfive")
    res = r.json()
    em = disnake.Embed(description=f"**{str(ctx.author.mention)} _gives a highfive to_ {str(mentioned_member.mention)}**") 
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@bot.slash_command(
    name="highfive",
    description="Gives a highfive to the given member"
    )
async def highfive(
    inter: disnake.ApplicationCommandInteraction,
    member: disnake.Member = Param(
        description="The member to highfive")
    ):
    r = requests.get("https://api.waifu.pics/sfw/highfive")
    res = r.json()
    em = disnake.Embed(description=f"**{str(inter.user.mention)} _gives a highfive to_ {str(member.mention)}**") 
    em.set_image(url=res['url'])
    await inter.response.send_message(embed=em)

@bot.command()
async def kickem(ctx, mentioned_member: disnake.Member = None):
    r = requests.get("https://api.waifu.pics/sfw/kick")
    res = r.json()
    em = disnake.Embed(description=f"**{str(ctx.author.mention)} _kicks_ {str(mentioned_member.mention)}**") 
    em.set_image(url=res['url'])
    await ctx.send(embed=em)


@bot.command()
async def kill(ctx, mentioned_member: disnake.Member = None):
    r = requests.get("https://api.waifu.pics/sfw/kill")
    res = r.json()
    em = disnake.Embed(description=f"**{str(ctx.author.mention)} _kills_ {str(mentioned_member.mention)}**") 
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@bot.slash_command(
    name="kill",
    description="Kills the given member:knife:"
    )
async def kill(
    inter: disnake.ApplicationCommandInteraction,
    member: disnake.Member = Param(
        description="The member to kill")
    ):
    r = requests.get("https://api.waifu.pics/sfw/kill")
    res = r.json()
    em = disnake.Embed(description=f"**{str(inter.user.mention)} _kills_ {str(member.mention)}**") 
    em.set_image(url=res['url'])
    await inter.response.send_message(embed=em)

@bot.command()
async def bully(ctx, mentioned_member: disnake.Member):
    r = requests.get("https://api.waifu.pics/sfw/bully")
    res = r.json()
    em = disnake.Embed(description=f"**{str(ctx.author.mention)} _bullies_ {str(mentioned_member.mention)}**") 
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@bot.slash_command(
    name="bully",
    description="Bullies the given member"
    )
async def bully(
    inter: disnake.ApplicationCommandInteraction,
    member: disnake.Member = Param(
        description="The member to bully")
    ):
    r = requests.get("https://api.waifu.pics/sfw/bully")
    res = r.json()
    em = disnake.Embed(description=f"**{str(inter.user.mention)} _bullies_ {str(member.mention)}**") 
    em.set_image(url=res['url'])
    await inter.response.send_message(embed=em)

@bot.command()
async def bite(ctx, mentioned_member: disnake.Member):
    r = requests.get("https://api.waifu.pics/sfw/bite")
    res = r.json()
    em = disnake.Embed(description=f"**{str(ctx.author.mention)} _bites_ {str(mentioned_member.mention)}**") 
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@bot.slash_command(
    name="bite",
    description="Bites the given member"
    )
async def bite(
    inter: disnake.ApplicationCommandInteraction,
    member: disnake.Member = Param(
        description="The member to bite")
    ):
    r = requests.get("https://api.waifu.pics/sfw/bite")
    res = r.json()
    em = disnake.Embed(description=f"**{str(inter.user.mention)} _bites_ {str(member.mention)}**") 
    em.set_image(url=res['url'])
    await inter.response.send_message(embed=em)

@bot.command()
async def bitly(ctx, *, link):
            r=requests.get(f"https://api-ssl.bitly.com/v3/shorten?longUrl={link}&domain=bit.ly&format=json&access_token={bitly_key}")
            r = r.json()
            new = r['data']['url']
            em = disnake.Embed()
            em.add_field(name='Shortened link', value=new, inline=False)
            await ctx.reply(embed=em)

@bot.command()
async def cuttly(ctx, *, link):
  req = requests.get(f'https://cutt.ly/api/api.php?key={cuttly_key}&short={link}')
  r = req.json()
  new = r['url']['shortLink']
  em = disnake.Embed()
  em.add_field(name='Shortened link', value=new, inline=False)
  await ctx.reply(embed=em)

@bot.command(pass_context=True)
async def userinfo(ctx, user: disnake.Member = None):
  if user == None:
    user = ctx.author
  else:
    pass
  embed = disnake.Embed(title="{}'s Info".format(user.name), description="Here's What I could Find in Discord's Database!", color=0x0072ff)
  embed.add_field(name="Name", value=user.name)
  embed.add_field(name="ID", value=user.id, inline=True)
  embed.add_field(name="Status", value=user.status, inline=True)
  embed.add_field(name="Role", value=user.top_role, inline=True)
  embed.add_field(name="Joined At", value=user.joined_at, inline=True)
  embed.set_thumbnail(url=user.display_avatar.url)
  embed.set_footer(text="By Lonely for bot")
  await ctx.reply(embed=embed)


@bot.command()
async def tickle(ctx, mentioned_member: disnake.Member = None):
    r = requests.get("https://nekos.life/api/v2/img/tickle")
    res = r.json()
    em = disnake.Embed(description=f"**{str(ctx.author.mention)} _tickles_ {str(mentioned_member.mention)}**") 
    em.set_image(url=res['url'])
    await ctx.send(embed=em)


@bot.command()
async def slap(ctx, mentioned_member: disnake.Member = None):
    r = requests.get("https://api.waifu.pics/sfw/slap")
    res = r.json()
    em = disnake.Embed(description=f"**{str(ctx.author.mention)} _slaps_ {str(mentioned_member.mention)}**") 
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@bot.slash_command(
    name="slap",
    description="Slaps the given member"
    )
async def slap(
    inter: disnake.ApplicationCommandInteraction,
    member: disnake.Member = Param(
        description="The member to slap")
    ):
    r = requests.get("https://api.waifu.pics/sfw/slap")
    res = r.json()
    em = disnake.Embed(description=f"**{str(inter.user.mention)} _slaps_ {str(member.mention)}**") 
    em.set_image(url=res['url'])
    await inter.response.send_message(embed=em)

@bot.command(aliases=['wouldyourather', 'would-you-rather', 'wyrq'])
async def wyr(ctx): # b'\xfc'
    r = requests.get('https://www.conversationstarters.com/wyrqlist.php').text
    soup = bs4(r, 'html.parser')
    qa = soup.find(id='qa').text
    qor = soup.find(id='qor').text
    qb = soup.find(id='qb').text
    em = disnake.Embed(description=f'{qa}\n{qor}\n{qb}')
    await ctx.send(embed=em)

@bot.slash_command(
    name="wyr",
    description="Gives a would you rather question"
    )
async def wyr(
    inter: disnake.ApplicationCommandInteraction
    ):
    r = requests.get('https://www.conversationstarters.com/wyrqlist.php').text
    soup = bs4(r, 'html.parser')
    qa = soup.find(id='qa').text
    qor = soup.find(id='qor').text
    qb = soup.find(id='qb').text
    em = disnake.Embed(description=f'{qa}\n{qor}\n{qb}')
    await inter.response.send_message(embed=em)

@bot.command() 
async def cat(ctx):
        try:
            req = requests.get(f"https://api.thecatapi.com/v1/images/search?format=json&x-api-key={cat_key}")
            r = req.json()
            em = disnake.Embed()
            em.set_image(url=str(r[0]["url"]))
            try:
                await ctx.send(embed=em)
            except:
                await ctx.send(str(r[0]["url"]))
        except:
            await ctx.send("Error occured while processing please try again later")


@bot.command(aliases=['ri', 'role'])
async def roleinfo(ctx, *, role: disnake.Role): 
    guild = ctx.guild
    since_created = (ctx.message.created_at - role.created_at).days
    role_created = role.created_at.strftime("%d %b %Y %H:%M")
    created_on = "{} ({} days ago)".format(role_created, since_created)
    users = len([x for x in guild.members if role in x.roles])
    if str(role.colour) == "#000000":
        colour = "default"
        color = ("#%06x" % random.randint(0, 0xFFFFFF))
        color = int(colour[1:], 16)
    else:
        colour = str(role.colour).upper()
        color = role.colour
    em = disnake.Embed(colour=color)
    em.set_author(name=f"Name: {role.name}"
    f"\nRole ID: {role.id}")
    em.add_field(name="Users", value = role.members)
    em.add_field(name="Mentionable", value=role.mentionable)
    em.add_field(name="Hoist", value=role.hoist)
    em.add_field(name="Position", value=role.position)
    em.add_field(name="Managed", value=role.managed)
    em.add_field(name="Colour", value=colour)
    em.add_field(name='Creation Date', value=created_on)
    await ctx.send(embed=em)
'''
@bot.command()
async def maid(ctx, mentioned_member: disnake.Member = None):
    async with aiohttp.ClientSession() as cs:
	    async with cs.get("https://api.waifu.im/sfw/maid/?exclude=3867126be8e260b5.jpeg,ca52928d43b30d6a&gif=true",headers=waifuim) as rep:
		    api= await rep.json()
		    url=api.get('tags')[0].get('images')[0].get('url')
            em = disnake.Embed()
            em.set_image(url=res['url'])
            await ctx.send(embed=em)


@bot.command()
async def waifu(ctx, mentioned_member: disnake.Member = None):
    async with aiohttp.ClientSession() as cs:
	    async with cs.get("https://api.waifu.im/sfw/waifu/?exclude=3867126be8e260b5.jpeg,ca52928d43b30d6a&gif=true",headers=waifuim) as rep:
		    api= await rep.json()
		    url=api.get('tags')[0].get('images')[0].get('url')
            em = disnake.Embed()
            em.set_image(url=res['url'])
            await ctx.send(embed=em)
'''

@bot.command()
async def nsfwwaifu(ctx):
 if ctx.channel.is_nsfw():
   r = requests.get("https://api.waifu.pics/nsfw/waifu")
   res = r.json()
   em = disnake.Embed()
   em.set_image(url=res['url'])
   await ctx.send(embed=em)
 else:
   titld = "Not a NSFW Channel!!"
   main = "The command you tried to use can be used only in a NSFW channel. Really sorry for the inconvenience. Please use this command in a NSFW channel"
   embedVar = disnake.Embed(title=titld, description=main, color=0x00ff00)
   await ctx.send(embed=embedVar)

@bot.command()
async def time(ctx, * , location):
    details = location.replace(" ", "+")
    r = requests.get(f"https://timezone.abstractapi.com/v1/current_time/?api_key=c083fc7d4cb14170ba7f6edf88a4d257&location={details}")
    res = r.json()
    timezone_location = str(res['timezone_location'])
    raw_time = str(res['datetime'])
    datetime_time = datetime.strptime(raw_time, "%Y-%m-%d %H:%M:%S")
    time = str(datetime_time.strftime("%I:%M %p"))
    date = str(datetime_time.strftime("%d %B %Y"))
    embedVar = disnake.Embed(title=f"Time in {location} is {time}", description=f'''{date}
     Timezone - {timezone_location}''', color=bot_embed_color)
    embedVar.set_thumbnail(url="https://i.pinimg.com/originals/26/be/b0/26beb09153b8df233d82e66bef3edfbb.jpg")
    await ctx.send(embed=embedVar)

@bot.command()
async def weather(ctx, *, city):
    if weather_key == '':
        print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}Weather API key has not been set in the config.json file"+Fore.RESET)
    else:
        try:
            req = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_key}')
            r = req.json()
            temperature = round(float(r["main"]["temp"]) - 273.15, 1)
            lowest = round(float(r["main"]["temp_min"]) - 273.15, 1)
            highest = round(float(r["main"]["temp_max"]) - 273.15, 1)
            weather = r["weather"][0]["main"]
            humidity = round(float(r["main"]["humidity"]), 1)
            wind_speed = round(float(r["wind"]["speed"]), 1)
            em = disnake.Embed(description=f'''
            Temperature: `{temperature}`
            Lowest: `{lowest}`
            Highest: `{highest}`
            Weather: `{weather}`
            Humidity: `{humidity}`
            Wind Speed: `{wind_speed}`
            ''')
            em.add_field(name='City', value=city.capitalize())
            em.set_thumbnail(url='https://ak0.picdn.net/shutterstock/videos/1019313310/thumb/1.jpg')
            try:
                await ctx.send(embed=em)
            except:
                await ctx.send(f'''
                Temperature: {temperature}
                Lowest: {lowest}
                Highest: {highest}
                Weather: {weather}
                Humidity: {humidity}
                Wind Speed: {wind_speed}
                City: {city.capitalize()}
                ''')    
        except KeyError:
            embed=disnake.Embed(title="Error!!", description="Looks like an error occured! I am trying my best to solve the issue. Please stay with us. If you entered the wrong city name. Please try again and enter the city name properly without spelling mistakes!! Thank You!", color = bot_embed_color)
            embed.set_footer(text="Possible Error - Rate Limiting or Invalid city")
            await ctx.send(embed=embed)
        else:
            print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{req.text}"+Fore.RESET)

@bot.command(pass_context=True)
async def meaning(ctx, *args):
    if not args:
        await ctx.send(
            ":question: Meaning of what? Correct format: `~meaning [Word]`",
            delete_after=10)
        return
    else:
        wait = await ctx.send(f":mag: Please hold on, searching ")
        try:
            word = args[0]
            meaning = GetMeaning_ATRS_SelfBot.GetMeaning()
            meaning.meaning(word)
            defination = meaning.defination
            part = meaning.part_of_speech
            word = meaning.word
            usage = meaning.use
            embed = disnake.Embed(title=word + f" [{part}]", description="**" + defination + "**", color=0xffae00)
            embed.set_footer(text=usage)
            await wait.edit(content="", embed=embed)
        except: 
            await wait.edit(content=":x: Something went wrong, cannot get get meaning of this ")

@bot.command()
async def nsfwneko(ctx):
 if ctx.channel.is_nsfw():
   r = requests.get("https://api.waifu.pics/nsfw/neko")
   res = r.json()
   em = disnake.Embed()
   em.set_image(url=res['url'])
   await ctx.send(embed=em)
 else:
   titld = "Not a NSFW Channel!!"
   main = "The command you tried to use can be used only in a NSFW channel. Really sorry for the inconvenience. Please use this command in a NSFW channel"
   embedVar = disnake.Embed(title=titld, description=main, color=bot_embed_color)
   await ctx.send(embed=embedVar)

@bot.command()
async def nsfwtrap(ctx):
 if ctx.channel.is_nsfw():
   r = requests.get("https://api.waifu.pics/nsfw/trap")
   res = r.json()
   em = disnake.Embed()
   em.set_image(url=res['url'])
   await ctx.send(embed=em)
 else:
   titld = "Not a NSFW Channel!!"
   main = "The command you tried to use can be used only in a NSFW channel. Really sorry for the inconvenience. Please use this command in a NSFW channel"
   embedVar = disnake.Embed(title=titld, description=main, color=bot_embed_color)
   await ctx.send(embed=embedVar)

@bot.command()
async def blowjob(ctx):
 if ctx.channel.is_nsfw():
   r = requests.get("https://api.waifu.pics/nsfw/blowjob")
   res = r.json()
   em = disnake.Embed()
   em.set_image(url=res['url'])
   await ctx.send(embed=em)
 else:
   titld = "Not a NSFW Channel!!"
   main = "The command you tried to use can be used only in a NSFW channel. Really sorry for the inconvenience. Please use this command in a NSFW channel"
   embedVar = disnake.Embed(title=titld, description=main, color=bot_embed_color)
   await ctx.send(embed=embedVar)


@bot.command()
async def game(ctx, *, message):
  if ctx.author.id in [738609666505834517,840411506646319124,827123687055949824]:
     await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.playing, name=message))
     await ctx.reply("Successfully changed")
  else:
     titld = "You don't have permissions?"
     main = "The command you tried to use can be used only be used by the developer and people whom he gave access to. You are not allowed to use it"
     embedVar = disnake.Embed(title=titld, description=main, color=bot_embed_color)
     await ctx.send(embed=embedVar)

@bot.command()
async def listening(ctx, *, message):
  if ctx.author.id in [738609666505834517,840411506646319124,827123687055949824]:
     await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.listening, name=message))
  else:
     titld = "You don't have permissions?"
     main = "The command you tried to use can be used only be used by the developer and people whom he gave access to. You are not allowed to use it"
     embedVar = disnake.Embed(title=titld, description=main, color=bot_embed_color)
     await ctx.send(embed=embedVar)

@bot.command()
async def setdelay(ctx, seconds: int):
  if ctx.author.guild_permissions.manage_guild:
      if seconds > -1 :
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")
      else:
        await ctx.channel.edit("Can't set negative slowmode! Trying to full me?? Huh?")
  else:
    await ctx.send("You are not allowed to use this command")



@bot.command()
async def startYT(ctx, channel:disnake.VoiceChannel = None):
    if not channel:
        try:
            vc = ctx.author.voice.channel.id
            link = await together_control.create_link(vc, 'youtube')
            await ctx.send(f"Click the link 👇\n{link}")
        except:
            await ctx.send("Please join a VC or tag a channel and try again:slight_smile:")
    else:
        vc = channel.id
        link = await together_control.create_link(vc, 'youtube')
        await ctx.send(f"Click the link 👇\n{link}")

@bot.slash_command(
    name="youtube",
    description="Creates link for Youtube Together VC activity!!📺"
    )
async def youtube(
    inter: disnake.ApplicationCommandInteraction,
    channel:disnake.VoiceChannel = Param(
        description="The channel to play in", default=None)
    ):
    if not channel:
        try:
            vc = inter.author.voice.channel.id
            link = await together_control.create_link(vc, 'youtube')
            await inter.response.send_message(f"Click the link 👇\n{link}")
        except:
            await inter.response.send_message("Please join a VC or tag a channel and try again:slight_smile:")
    else:
        vc = channel.id
        link = await together_control.create_link(vc, 'youtube')
        await inter.response.send_message(f"Click the link 👇\n{link}")

@bot.command()
async def chess(ctx, channel:disnake.VoiceChannel = None):
    if not channel:
        try:
            vc = ctx.author.voice.channel.id
            link = await together_control.create_link(vc, 'chess')
            await ctx.send(f"Click the link 👇\n{link}")
        except:
            await ctx.send("Please join a VC or tag a channel and try again:slight_smile:")
    else:
        vc = channel.id
        link = await together_control.create_link(vc, 'chess')
        await ctx.send(f"Click the link 👇\n{link}")

@bot.slash_command(
    name="chess",
    description="Sends link for Chess in the Park VC activity"
    )
async def chess(
    inter: disnake.ApplicationCommandInteraction,
    channel:disnake.VoiceChannel = Param(
        description="The channel to play in", default=None)
    ):
    if not channel:
        try:
            vc = inter.author.voice.channel.id
            link = await together_control.create_link(vc, 'chess')
            await inter.response.send_message(f"Click the link 👇\n{link}")
        except:
            await inter.response.send_message("Please join a VC or tag a channel and try again:slight_smile:")
    else:
        vc = channel.id
        link = await together_control.create_link(vc, 'chess')
        await inter.response.send_message(f"Click the link 👇\n{link}")

@bot.command()
async def poker(ctx, channel:disnake.VoiceChannel = None):
    if not channel:
        try:
            vc = ctx.author.voice.channel.id
            link = await together_control.create_link(vc, 'poker')
            await ctx.send(f"Click the link 👇\n{link}")
        except:
            await ctx.send("Please join a VC or tag a channel and try again:slight_smile:")
    else:
        vc = channel.id
        link = await together_control.create_link(vc, 'poker')
        await ctx.send(f"Click the link 👇\n{link}")

@bot.slash_command(
    name="poker",
    description="Sends link for Poker Night VC activity!"
    )
async def poker(
    inter: disnake.ApplicationCommandInteraction,
    channel:disnake.VoiceChannel = Param(
        description="The channel to play in", default=None)
    ):
    if not channel:
        try:
            vc = inter.author.voice.channel.id
            link = await together_control.create_link(vc, 'poker')
            await inter.response.send_message(f"Click the link 👇\n{link}")
        except:
            await inter.response.send_message("Please join a VC or tag a channel and try again:slight_smile:")
    else:
        vc = channel.id
        link = await together_control.create_link(vc, 'poker')
        await inter.response.send_message(f"Click the link 👇\n{link}")

@bot.command()
async def betrayal(ctx, channel:disnake.VoiceChannel = None):
    if not channel:
        try:
            vc = ctx.author.voice.channel.id
            link = await together_control.create_link(vc, 'betrayal')
            await ctx.send(f"Click the link 👇\n{link}")
        except:
            await ctx.send("Please join a VC or tag a channel and try again:slight_smile:")
    else:
        vc = channel.id
        link = await together_control.create_link(vc, 'betrayal')
        await ctx.send(f"Click the link 👇\n{link}")

@bot.slash_command(
    name="betrayal",
    description="Sends link for Betrayal.io VC activity!"
    )
async def betrayal(
    inter: disnake.ApplicationCommandInteraction,
    channel:disnake.VoiceChannel = Param(
        description="The channel to play in", default=None)
    ):
    if not channel:
        try:
            vc = inter.author.voice.channel.id
            link = await together_control.create_link(vc, 'betrayal')
            await inter.response.send_message(f"Click the link 👇\n{link}")
        except:
            await inter.response.send_message("Please join a VC or tag a channel and try again:slight_smile:")
    else:
        vc = channel.id
        link = await together_control.create_link(vc, 'betrayal')
        await inter.response.send_message(f"Click the link 👇\n{link}")

@bot.command()
async def fishing(ctx, channel:disnake.VoiceChannel = None):
    if not channel:
        try:
            vc = ctx.author.voice.channel.id
            link = await together_control.create_link(vc, 'fishing')
            await ctx.send(f"Click the link 👇\n{link}")
        except:
            await ctx.send("Please join a VC or tag a channel and try again:slight_smile:")
    else:
        vc = channel.id
        link = await together_control.create_link(vc, 'fishing')
        await ctx.send(f"Click the link 👇\n{link}")

@bot.slash_command(
    name="fishing",
    description="Sends link for Fishington.io VC activity!"
    )
async def fishing(
    inter: disnake.ApplicationCommandInteraction,
    channel:disnake.VoiceChannel = Param(
        description="The channel to play in", default=None)
    ):
    if not channel:
        try:
            vc = inter.author.voice.channel.id
            link = await together_control.create_link(vc, 'fishing')
            await inter.response.send_message(f"Click the link 👇\n{link}")
        except:
            await inter.response.send_message("Please join a VC or tag a channel and try again:slight_smile:")
    else:
        vc = channel.id
        link = await together_control.create_link(vc, 'fishing')
        await inter.response.send_message(f"Click the link 👇\n{link}")

@bot.command()
async def lettertile(ctx, channel:disnake.VoiceChannel = None):
    if not channel:
        try:
            vc = ctx.author.voice.channel.id
            link = await together_control.create_link(vc, '879863686565621790')
            await ctx.reply(f"Click the link 👇\n{link}")
        except:
            await ctx.reply("Please join a VC or tag a channel and try again:slight_smile:")
    else:
        vc = channel.id
        link = await together_control.create_link(vc, '879863686565621790')
        await ctx.reply(f"Click the link 👇\n{link}")

@bot.command()
async def wordsnack(ctx, channel:disnake.VoiceChannel = None):
    if not channel:
        try:
            vc = ctx.author.voice.channel.id
            link = await together_control.create_link(vc, '879863976006127627')
            await ctx.reply(f"Click the link 👇\n{link}")
        except:
            await ctx.reply("Please join a VC or tag a channel and try again:slight_smile:")
    else:
        vc = channel.id
        link = await together_control.create_link(vc, '879863976006127627')
        await ctx.reply(f"Click the link 👇\n{link}")

@bot.command()
async def doodlecrew(ctx, channel:disnake.VoiceChannel = None):
    if not channel:
        try:
            vc = ctx.author.voice.channel.id
            link = await together_control.create_link(vc, '878067389634314250')
            await ctx.reply(f"Click the link 👇\n{link}")
        except:
            await ctx.reply("Please join a VC or tag a channel and try again:slight_smile:")
    else:
        vc = channel.id
        link = await together_control.create_link(vc, '878067389634314250')
        await ctx.reply(f"Click the link 👇\n{link}")

@bot.command()
async def spellcast(ctx, channel:disnake.VoiceChannel = None):
    if not channel:
        try:
            vc = ctx.author.voice.channel.id
            link = await together_control.create_link(vc, '852509694341283871')
            await ctx.send(f"Click the link 👇\n{link}")
        except:
            await ctx.send("Please join a VC or tag a channel and try again:slight_smile:")
    else:
        vc = channel.id
        link = await together_control.create_link(vc, '852509694341283871')
        await ctx.send(f"Click the link 👇\n{link}")

@bot.slash_command(
    name="spellcast",
    description="Sends link for Spell Cast 🔮 VC activity!"
    )
async def spellcast(
    inter: disnake.ApplicationCommandInteraction,
    channel:disnake.VoiceChannel = Param(
        description="The channel to play in", default=None)
    ):
    if not channel:
        try:
            vc = inter.author.voice.channel.id
            link = await together_control.create_link(vc, '852509694341283871')
            await inter.response.send_message(f"Click the link 👇\n{link}")
        except:
            await inter.response.send_message("Please join a VC or tag a channel and try again:slight_smile:")
    else:
        vc = channel.id
        link = await together_control.create_link(vc, '852509694341283871')
        await inter.response.send_message(f"Click the link 👇\n{link}")

@bot.command(aliases=['screenshot', 'ss', 'screen'])
async def sshot(ctx,url):
   await ctx.send("Fetching screenshot from the given URL. Please wait........")
   r = requests.get(f"https://shot.screenshotapi.net/screenshot?token=V5VWA2H-TJPMV0C-GR13FY9-Y9F2F8Q&url={url}")
   res = r.json()
   screenshot=res['screenshot']
   em = disnake.Embed(description="**Here is your screenshot :-**",color = bot_embed_color)
   em.set_image(url=screenshot)
   await ctx.send(embed=em)


@bot.command(pass_context=True)
async def lyrics(ctx, *args):
    track = " ".join(args)
    user = ctx.author
    for activity in user.activities:
        if isinstance(activity, Spotify):
            track = activity.title + " by " + str(activity.artist).split(";")[0]
    if track == "" or track == " " or track.isspace():
        await ctx.reply(":question: What track to search? Correct format: `~lyrics [Query]`", delete_after=10)
        return
    else:
        wait = await ctx.reply(f":mag: Please hold on, searching for `{track}`")
        try:
            search_lyrics = GetLyrics_ATRS_SelfBot.GetLyrics()
            try:
                search_lyrics.musixmatch_lyrics(query=track)
            except TimeoutError:
                search_lyrics.google_lyrics(query=track)
            except:
                search_lyrics.genius_lyrics(query=track,
                                            api_key="API Key")
            embed = disnake.Embed(title=search_lyrics.title, description="**" + search_lyrics.artist + "**",
                                  colour=0xffae00)
            lyric = str(str(search_lyrics.lyrics).strip()).split("\n\n")
            for i in lyric:
                embed.add_field(name="​", value=i, inline=False)
            embed.set_footer(text="Source: " + search_lyrics.source)
            try:
                await wait.edit(embed=embed, content="")
            except:
                embed = disnake.Embed(title=":x: Something went wrong, can't show lyrics. Click here. ",
                                      url=search_lyrics.url, colour=0xffae00)
                await wait.edit(embed=embed, content="")
        except:
            await wait.edit(content=":x: Something went wrong, can't show lyrics ")

@bot.command()
async def company(ctx, domain):
    r = requests.get(f"https://companyenrichment.abstractapi.com/v1/?api_key=de0b735ecaa547cc9a012c73240fb364&domain={domain}")
    res = r.json()
    company_name = str(res['name'])
    if company_name == "None":
      await ctx.reply("Company not found!")
    else:
      em = discord.Embed(description=f'''
      Company Name: `{str(res['name'])}`
      Domain: `{str(res['domain'])}`
      Founded on: `{str(res['year_founded'])}`
      Total no. of employees: `{str(res['employees_count'])}`
      Locality: `{str(res['locality'])}`
      Country: `{str(res['country'])}`
      Linkedin: `{str(res['linkedin_url'])}`
      ''', color=bot_embed_color)
      await ctx.reply(embed=em)


class InteractiveView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.expr = ""
        self.calc = simpcalc.Calculate() # if you are using the above function, no need to declare this!

    @disnake.ui.button(style=disnake.ButtonStyle.blurple, label="1", row=0)
    async def one(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        self.expr += "1"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @disnake.ui.button(style=disnake.ButtonStyle.blurple, label="2", row=0)
    async def two(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        self.expr += "2"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @disnake.ui.button(style=disnake.ButtonStyle.blurple, label="3", row=0)
    async def three(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        self.expr += "3"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @disnake.ui.button(style=disnake.ButtonStyle.green, label="+", row=0)
    async def plus(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        self.expr += "+"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @disnake.ui.button(style=disnake.ButtonStyle.blurple, label="4", row=1)
    async def last(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        self.expr += "4"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @disnake.ui.button(style=disnake.ButtonStyle.blurple, label="5", row=1)
    async def five(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        self.expr += "5"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @disnake.ui.button(style=disnake.ButtonStyle.blurple, label="6", row=1)
    async def six(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        self.expr += "6"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @disnake.ui.button(style=disnake.ButtonStyle.green, label="/", row=1)
    async def divide(self, button: disnake.ui.Button, interaction: disnake.Interaction):
            self.expr += "/"
            await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @disnake.ui.button(style=disnake.ButtonStyle.blurple, label="7", row=2)
    async def seven(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        self.expr += "7"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @disnake.ui.button(style=disnake.ButtonStyle.blurple, label="8", row=2)
    async def eight(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        self.expr += "8"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @disnake.ui.button(style=disnake.ButtonStyle.blurple, label="9", row=2)
    async def nine(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        self.expr += "9"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @disnake.ui.button(style=disnake.ButtonStyle.green, label="*", row=2)
    async def multiply(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        self.expr += "*"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @disnake.ui.button(style=disnake.ButtonStyle.blurple, label=".", row=3)
    async def dot(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        self.expr += "."
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @disnake.ui.button(style=disnake.ButtonStyle.blurple, label="0", row=3)
    async def zero(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        self.expr += "0"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @disnake.ui.button(style=disnake.ButtonStyle.green, label="=", row=3)
    async def equal(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        try:
            self.expr = await self.calc.calculate(self.expr)
        except errors.BadArgument: # if you are function only, change this to BadArgument
            return await interaction.response.send_message("Um, looks like you provided a wrong expression....")
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @disnake.ui.button(style=disnake.ButtonStyle.green, label="-", row=3)
    async def minus(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        self.expr += "-"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @disnake.ui.button(style=disnake.ButtonStyle.green, label="(", row=4)
    async def left_bracket(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        self.expr += "("
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @disnake.ui.button(style=disnake.ButtonStyle.green, label=")", row=4)
    async def right_bracket(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        self.expr += ")"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @disnake.ui.button(style=disnake.ButtonStyle.red, label="C", row=4)
    async def clear(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        self.expr = ""
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @disnake.ui.button(style=disnake.ButtonStyle.red, label="<==", row=4)
    async def back(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        self.expr = self.expr[:-1]
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

@bot.command(name="calculate")
async def interactive_calc(ctx):
      view = InteractiveView()
      await ctx.reply("```\n```",view=view)

@bot.message_command(name="Reverse") # optional
async def reverse(inter: disnake.MessageCommandInteraction):
    await inter.response.send_message(inter.target.content[::-1])

@bot.command()
async def help(ctx, *, cmd = None): 
    if cmd == "commands":
        Tile = "Here are all the commands for you :-"
        Desc = "I hope you Enjoy!!!"
        embed=discord.Embed(title=Tile, description=Desc, color=bot_embed_color)
        Field1 = "Fun :-"
        hi = f"`kiss`,`hug`,`cuddle`,`pat`,`highfive`,`kickem`,`kill`,`bully`,`bite`,`tickle`,`cat`,`8ball`,`wyr`,`slap`,`cry`,`truth`,`dare`, `tic`"
        embed.add_field(name=Field1, value=hi, inline=False)
        Field2 = "Moderation :-"
        hi2 = "`kick`,`ban`,`unban`,`purge`,`setdelay`"
        embed.add_field(name=Field2, value=hi2, inline=False)
        Field3 = "VC Activities :-  _(Note - These activities are Beta features. They are availabe only on a few desktop platforms)_"
        hi3 = "`startYT`,`chess`,`poker`,`betrayal`,`fishing`, `lettertile`, `wordsnack`, `doodlecrew`"
        embed.add_field(name=Field3, value=hi3, inline=False)
        Field4 = "NSFW :-"
        hi4 = "||`nsfwwaifu`,`nsfwneko`,`blowjob`, `nsfwtrap`||"
        embed.add_field(name=Field4, value=hi4, inline=False)
        Field5 = "Utilities :-"
        hi5 = "`recipe`, `time`, `company`,`pingweb`,`bitly`,`cuttly`,`eth`,`btc` ,`userinfo` ,`geoip` ,`roleinfo`,`av` ,`lyrics` ,`calculate`, `mac`"
        embed.add_field(name=Field5, value=hi5, inline=False)
        Field6 = "Music :-  (**The music bot is still under testing some things might fail to work or cause errors.**)"
        hi6 = "`join`,`loop`,`now`,`play`,`queue`,`remove`,`shuffle`,`skip`,`volume`"
        embed.add_field(name=Field6, value=hi6, inline=False)
        embed.set_footer(text="Note:- VC Activities will work only if the bot has permissions to create invite link")
        await ctx.reply(embed=embed)
    elif cmd == None:
      titld = "Need Help??"
      main = "Hina is a bot made for fun and moderation. It is totally dedicated to the girl I love bot. To view the command list please use `luv help commands`"
      embedVar = disnake.Embed(title=titld, url="https://discord.gg/Tgb5s784ga", description=main, color=0x2a45bf)
      await ctx.send(embed=embedVar)
    else:
        try:
                desc = helpl.get(cmd)
                if desc == None:
                        embedVar = disnake.Embed(title="Command not found", description="Please check the command name", color=0x2a45bf)
                        await ctx.reply(embed=embedVar)
                else:
                        embedVar = disnake.Embed(title=cmd, description=desc, color=bot_embed_color)
                        await ctx.reply(embed=embedVar)
	except:
		pass

@bot.user_command(name="Avatar") # optional
async def avatar(inter: disnake.UserCommandInteraction):
    # inter.target is the user you clicked on
    emb = disnake.Embed(title=f"{inter.target}'s avatar")
    emb.set_image(url=inter.target.display_avatar.url)
    await inter.response.send_message(embed=emb)

@bot.command()
async def test(ctx, location):
    details = "+".join(location)
    r = requests.get(f"https://timezone.abstractapi.com/v1/current_time/?api_key=c083fc7d4cb14170ba7f6edf88a4d257&location={details}")
    print(r.content)
    print(r.json())
    res = r.json()
    print(res)
    await ctx.send(res)

@bot.command()
async def searchyoutube(ctx, *, search):
    query_string = parse.urlencode({'search_query': search})
    html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall( r"watch\?v=(\S{11})", html_content.read().decode())
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])

@bot.slash_command(
    name="truth",
    description="Sends a random truth"
    )
async def truth(
    inter: disnake.ApplicationCommandInteraction,
    rating: str = Param(
        description="The Rating of which you want the question to be", default = None)
    ):
    if rating == None:
      r = requests.get(f"https://api.truthordarebot.xyz/api/truth/?rating=")
      res = r.json()
      Tile = f"Here is a truth for you"
      Desc = res['question']
      embed=discord.Embed(title=Tile, description=Desc, color=bot_embed_color)
      await inter.response.send_message(embed=embed)
    else:
      try: 
        r = requests.get(f"https://api.truthordarebot.xyz/api/truth/?rating={rating}")
        res = r.json()
        Tile = f"Here is a {rating} rated question for you"
        Desc = res['question']
        embed=discord.Embed(title=Tile, description=Desc, color=bot_embed_color)
        await inter.response.send_message(embed=embed)
      except:
        await inter.response.send_message("Please send a valid rating!! Valid parameters are `pg`,`pg13`,`r`")

@bot.command()
async def invite(ctx):
  embed=discord.Embed(title="Invite me!!", url="https://discord.com/oauth2/authorize?client_id=902740840181542974&permissions=271641726&scope=bot%20applications.commands", description="Invite me to you server and we can have fun together!! I am totally free without any premium plans. I hope we can all be good friends in your server too!!!!!!!! Click on the title of this embed to invite me!", color = 0x242624)
  embed.set_footer(text="Bot made by Lonely for bot (My Love)")
  await ctx.reply(embed=embed)

@bot.slash_command(
    name="invite",
    description="Sends the invite link of the bot"
    )
async def invite(
    inter: disnake.ApplicationCommandInteraction
    ):
    embed=disnake.Embed(title="Invite me!!", url="https://discord.com/oauth2/authorize?client_id=902740840181542974&permissions=271641726&scope=bot%20applications.commands", description="Invite me to you server and we can have fun together!! I am totally free without any premium plans. I hope we can all be good friends in your server too!!!!!!!! Click on the title of this embed to invite me!", color = 0x242624)
    embed.set_footer(text="Bot made by Lonely for bot (My Love)")
    await inter.response.send_message(embed=embed)

@bot.slash_command(
    name="calculate",
    description="Calculate 🖩"
    )
async def calculate(
    inter: disnake.ApplicationCommandInteraction
    ):
    view = InteractiveView()
    await inter.response.send_message("```\n```",view=view)

@bot.command()
async def mac(ctx, mac):
    r = requests.get('http://api.macvendors.com/' + mac)
    em = discord.Embed(title='MAC Lookup Result', description=r.text, colour=0xDEADBF)
    await ctx.send(embed=em)

@bot.slash_command(
    name="love",
    description="Check how much you love the mentioned member"
    )
async def love(
    inter: disnake.ApplicationCommandInteraction,
    member: disnake.Member = Param(
        description="Your crush")
    ):
    r = requests.get(f"https://atrs-webapis.herokuapp.com/API/calculate_love/{str(inter.user.name)}/{str(member.name)}")
    em = disnake.Embed(description=f"You love {str(member.mention)} by {(r.text)}")
    await inter.response.send_message(embed=em)

@bot.command()
async def love(ctx, mentioned_member: disnake.Member = None):
  r = requests.get(f"https://atrs-webapis.herokuapp.com/API/calculate_love/{str(ctx.author.name)}/{str(mentioned_member.name)}")
  em = disnake.Embed(description=f"You love {str(mentioned_member.mention)} by {(r.text)}") 
  await ctx.send(embed=em)

@bot.command()
async def spotipy(ctx, user: disnake.Member = None):
  user = user or ctx.author  
  spot = (activity for activity in user.activities if isinstance(activity, discord.Spotify)), None
  if spot is None:
    await ctx.send(f"{user.name} is not listening to Spotify")
    return
  else:
    embed = discord.Embed(title=f"{user.name}'s Spotify", color=bot_embed_color)
    embed.add_field(name="Song", value=spot.title)
    embed.add_field(name="Artist", value=spot.artist)
    embed.add_field(name="Album", value=spot.album)
    embed.add_field(name="Track Link", value=f"[{spot.title}](https://open.spotify.com/track/{spot.track_id})")
    embed.set_thumbnail(url=spot.album_cover_url)
    await ctx.send(embed=embed)

@bot.command()
async def apod(ctx, choice = None):
    r = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}")
    res = r.json()
    explanation = res['explanation']
    try:
        url=res['hdurl']
        title = res['title']
        explanation = res['explanation']
        embed = disnake.Embed(title = title, description = explanation, colour = bot_embed_color)
        embed.set_image(url=url)
    except:
	    url = res['url']
	    title = res['title']
	    embed = disnake.Embed(title = title, url = url, description = explanation, colour = bot_embed_color)
    await ctx.reply(embed=embed)


@bot.command()
async def question(ctx):
  r = requests.get('https://opentdb.com/api.php?amount=1')
  res = json.loads(r.text)
  Quote = res[0]['question']
  em = discord.Embed(title=Quote, description="Bruh",colour=0xDEADBF)
  await ctx.send(embed=em)

@bot.command()
async def spotify(ctx: Context, member: disnake.Member = None):
    """See info about the member's spotify activity."""

    member = member or ctx.author

    if member.bot:
        await ctx.message.delete()
        return await ctx.send(
            "Cannot check for spotify activity for bots! Use on members only!",
            delete_after=10
        )

    for activity in member.activities:
        if isinstance(activity, disnake.Spotify):
            diff = relativedelta(
                datetime.datetime.utcnow(),
                activity.created_at.replace(tzinfo=None)
            )

            m = disnake.Embed(title=f"{member.name} activity:")
            m.add_field(name="Listening to:", value=activity.title, inline=False)
            m.add_field(name="By:", value=activity.artist, inline=False)
            m.add_field(name="On:", value=activity.album, inline=False)
            m1, s1 = divmod(int(activity.duration.seconds), 60)
            song_length = '{:02}:{:02}'.format(m1, s1)
            playing_for = '{:02}:{:02}'.format(diff.minutes, diff.seconds)
            m.add_field(name="Duration:", value=f"{playing_for} - {song_length}")
            m.add_field(name="Total Duration:", value=song_length, inline=False)
            m.set_thumbnail(url=activity.album_cover_url)
            m.color = disnake.Color.green()
            view = SpotifyView(song_url=f'https://open.spotify.com/track/{activity.track_id}?si=xrjyVAxhS1y5rNHLM_WRww')
            view.message = await ctx.send(embed=m, view=view)
            return

    await ctx.send("No spotify activity detected!")


@bot.slash_command(
    name="dare",
    description="Sends a random dare"
    )
async def dare(
    inter: disnake.ApplicationCommandInteraction,
    rating: str = Param(
        description="The Rating of which you want the question to be", default = None)
    ):
    if rating == None:
      r = requests.get(f"https://api.truthordarebot.xyz/api/dare/?rating=")
      res = r.json()
      Tile = f"Here is a dare for you"
      Desc = res['question']
      embed=discord.Embed(title=Tile, description=Desc, color=bot_embed_color)
      await inter.response.send_message(embed=embed)
    else:
      try: 
        r = requests.get(f"https://api.truthordarebot.xyz/api/dare/?rating={rating}")
        res = r.json()
        Tile = f"Here is a {rating} rated dare for you"
        Desc = res['question']
        embed=discord.Embed(title=Tile, description=Desc, color=bot_embed_color)
        await inter.response.send_message(embed=embed)
      except:
        await inter.response.send_message("Please send a valid rating!! Valid parameters are `pg`,`pg13`,`r`")

@bot.command()
async def nhie(ctx, rating = None):
  if rating == None:
    r = requests.get(f"https://api.truthordarebot.xyz/api/nhie")
    res = r.json()
    Tile = f"Here is a never have I ever question for you "
    Desc = res['question']
    embed=discord.Embed(title=Tile, description=Desc, color=bot_embed_color)
    await ctx.send(embed=embed)
  else:
    try: 
      r = requests.get(f"https://api.truthordarebot.xyz/api/nhie/?rating={rating}")
      res = r.json()
      Tile = f"Here is a {rating} rated never have I ever question for you"
      Desc = res['question']
      embed=disnake.Embed(title=Tile, description=Desc, color=bot_embed_color)
      await ctx.send(embed=embed)
    except:
      await ctx.send("Please send a valid rating!! Valid parameters are `pg`,`pg13`,`r`")

@bot.slash_command(
    name="nhie",
    description="Sends a random Never Have I Ever question"
    )
async def nhie(
    inter: disnake.ApplicationCommandInteraction,
    rating: str = Param(
        description="The Rating of which you want the question to be", default = None)
    ):
    if rating == None:
      r = requests.get(f"https://api.truthordarebot.xyz/api/nhie")
      res = r.json()
      Tile = f"Here is a Never Have I ever question for you"
      Desc = res['question']
      embed=disnake.Embed(title=Tile, description=Desc, color=bot_embed_color)
      await inter.response.send_message(embed=embed)
    else:
      try: 
        r = requests.get(f"https://api.truthordarebot.xyz/api/nhie/?rating={rating}")
        res = r.json()
        Tile = f"Here is a {rating} rated Never Have I Ever for you"
        Desc = res['question']
        embed=discord.Embed(title=Tile, description=Desc, color=bot_embed_color)
        await inter.response.send_message(embed=embed)
      except:
        await inter.response.send_message("Please send a valid rating!! Valid parameters are `pg`,`pg13`,`r`")

@bot.command()
async def inspire(ctx):
    r = requests.get(f"https://zenquotes.io/api/random")
    res = json.loads(r.text)
    Quote = res[0] ['q'] + " - " + res [0] ['a']
    Tile = "Here is a random generated quote for you  :-"
    embed=discord.Embed(title=Tile, description=Quote, color=bot_embed_color)
    await ctx.send(embed=embed)

@bot.slash_command(
    name="inspire",
    description="Sends you a quote 💖"
    )
async def inspire(
    inter: disnake.ApplicationCommandInteraction
    ):
    r = requests.get(f"https://zenquotes.io/api/random")
    res = json.loads(r.text)
    Quote = res[0] ['q'] + " - " + res [0] ['a']
    Tile = "Here is a random generated quote for you  :-"
    embed=discord.Embed(title=Tile, description=Quote, color=bot_embed_color)
    await inter.response.send_message(embed=embed)

@bot.command()
async def allserversinvite(ctx):
  if ctx.author.id in [738609666505834517,840411506646319124,827123687055949824,886120777630486538]:
      for guild in bot.guilds:
        try:
            channel = guild.system_channel    
            await ctx.send(await channel.create_invite())
        except:
          await ctx.send("Missing permissions")
  else:
    await ctx.send("This command has been restricted to owner and a few people!")


@bot.command(pass_context=True)
async def ping(ctx):
  ping = round(bot.latency * 1000)
  Tile = f"Pong! 🏓"
  Desc = f"Here is the bot latency for you - {ping}ms"
  embed=discord.Embed(title=Tile, description=Desc, color=bot_embed_color)
  embed.set_footer(text="Bot made by Lonely for bot!")
  await ctx.reply(embed=embed)

@bot.slash_command(
    name="ping",
    description="Gives you the latency 🏓"
    )
async def ping(
    inter: disnake.ApplicationCommandInteraction
    ):
    ping = round(bot.latency * 1000)
    Tile = f"Pong!"
    Desc = f"Here is the bot latency for you - {ping}ms"
    embed=discord.Embed(title=Tile, description=Desc, color=bot_embed_color)
    embed.set_footer(text="Bot made by Lonely for bot!")
    await inter.response.send_message(embed=embed)

@bot.command()
async def spamwifey(ctx, amount: int, *, message): 
  if ctx.author.id in [827123687055949824, 826823454081941545, 886120777630486538, 738609666505834517]:
    await ctx.message.delete() 
    user = bot.get_user(840411506646319124)   
    for _i in range(amount):
        await user.send(message)
  else:
    await ctx.send ("How TF do you know bout this command?? And you trying to spam my wifey?? Why TF?? This command can't be used by anyone. And don't dare spam my wifey")

@bot.command()
async def sendJJ(ctx,  message): # b'\xfc'
    await ctx.message.delete() 
    user = bot.get_user(870820425033211944)
    await user.send(message)

@bot.command()
async def devintroduce(ctx):
  if ctx.author.id in [827123687055949824, 826823454081941545, 886120777630486538, 738609666505834517]:
    await ctx.message.delete()
    embed=disnake.Embed(title="Hello There ", url="https://lonelyguy12.github.io/", description=f'''I hope you all are doing good
    I am {str(ctx.author.mention)} from Moscow, Russia
    I love my wifey, coding, music(EDM and Pop), cooking and cycling
    Imma Nyctophile and Selenophile BTW
    Dislikes - Rude People, Linux Haters
    I am ~~single~~ taken by Skyy xD
    Personality Type - ISFP - T :)
    Glad to see y'all have an amazing day''', color = bot_embed_color)
    embed.set_author(name=f"{ctx.author.name}", url="https://discord.gg/ANj8Mz6fy4", icon_url="https://cdn.discordapp.com/attachments/900226775458652270/910943017299497010/IMG_0078.png")
    embed.set_image(url="https://p4.wallpaperbetter.com/wallpaper/623/371/684/anime-hyouka-eru-chitanda-h%C5%8Dtar%C5%8D-oreki-hd-wallpaper-preview.jpg")
    embed.set_thumbnail(url="https://i.pinimg.com/originals/08/7d/61/087d61a0739e928e7a840a8a51bed05a.jpg")
    embed.set_footer(text="For more info :- https://lonelyguy12.github.io/")
    await ctx.send(embed=embed) 
  else:
    embed=disnake.Embed(title="Hello There ", url="https://lonelyguy12.github.io/", description=f'''I hope you all are doing good
    I am Lonely Guy from Moscow, Russia
    I love my wifey, coding, music(EDM and Pop), cooking and cycling
    Imma Nyctophile and Selenophile BTW
    Dislikes - Rude People, Linux Haters
    I am ~~single~~ taken by Skyy xD
    Personality Type - ISFP - T :)
    Glad to see y'all have an amazing day''', color = bot_embed_color)
    embed.set_author(name=f"Lonely Guy", url="https://discord.gg/ANj8Mz6fy4", icon_url="https://cdn.discordapp.com/attachments/900226775458652270/910943017299497010/IMG_0078.png")
    embed.set_image(url="https://p4.wallpaperbetter.com/wallpaper/623/371/684/anime-hyouka-eru-chitanda-h%C5%8Dtar%C5%8D-oreki-hd-wallpaper-preview.jpg")
    embed.set_thumbnail(url="https://i.pinimg.com/originals/08/7d/61/087d61a0739e928e7a840a8a51bed05a.jpg")
    embed.set_footer(text="For more info :- https://lonelyguy12.github.io/")
    await ctx.send(embed=embed)

@bot.command()
async def unloadall(ctx):
    if ctx.author.id in [827123687055949824, 826823454081941545, 886120777630486538, 738609666505834517]:
        for filename in os.listdir("./cogs"):
            if filename.endswith('.py'):
                bot.unload_extension(f"cogs.{filename[:-3]}")
                await ctx.send(f"Unloaded `{filename[:-3]}` successfully!")    

@bot.command()
async def loadall(ctx):
    if ctx.author.id in [827123687055949824, 826823454081941545, 886120777630486538, 738609666505834517]:
        for filename in os.listdir("./cogs"):
            if filename.endswith('.py'):
                bot.load_extension(f"cogs.{filename[:-3]}")
                await ctx.send(f"Loaded `{filename[:-3]}` successfully!")

bot.load_extension("cogs.utilities")
bot.load_extension("cogs.fun")
#bot.load_extension("cogs.music")
bot.load_extension("cogs.EvalCommand")
bot.run(token)
