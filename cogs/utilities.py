import disnake as discord
import disnake
from disnake.ext import commands
import random
import requests
import json
import asyncio
from datetime import datetime
from dateutil.relativedelta import relativedelta
import bs4
import wikipedia
import html
import aiohttp
bot_embed_color = 0x4548a8

with open('config.json') as f:
    config = json.load(f)

extreme_ip_api_key = config.get('extreme-ip-api-key')
timezone_api_key = config.get('timezone_api_key')
edamam_api_recipe_app_id = config.get('edamam_api_recipe_app_id')
edamam_api_recipe_app_key = config.get('edamam_api_recipe_app_key')

class Utilities(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=['ethereum'])
  async def eth(self, ctx):
      r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,EUR')
      r = r.json()
      usd = r['USD']
      eur = r['EUR']
      em = discord.Embed(description=f'USD: `{str(usd)}$`\nEUR: `{str(eur)}€`')
      em.set_author(name='Ethereum', icon_url='https://cdn.disnakeapp.com/attachments/271256875205525504/374282740218200064/2000px-Ethereum_logo.png')
      await ctx.reply(embed=em)



  @commands.command(aliases=['bitcoin'])
  async def eth(self, ctx):
      r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR')
      r = r.json()
      usd = r['USD']
      eur = r['EUR']
      em = discord.Embed(description=f'USD: `{str(usd)}$`\nEUR: `{str(eur)}€`')
      em.set_author(name='Bitcoin', icon_url='https://cdn.pixabay.com/photo/2013/12/08/12/12/bitcoin-225079_960_720.png')
      await ctx.reply(embed=em)


  @commands.command()
  async def pingweb(self, ctx, website):
      if website is None: 
          embed=discord.Embed(title="Error!", description="You didn't enter a website to ping for ;-;", color=0x243e7b)
          await ctx.send(embed=embed)
      else:
          try:
              r = requests.get(website).status_code
          except Exception as e:
              await ctx.send(f'''Error raised :- ```{e}```''')
          if r == 404:
              await ctx.send(f'Site is down, responded with a status code of {r}')
          else:
              await ctx.send(f'Site is up, responded with a status code of {r}')


  @commands.command(aliases=['pfp', 'avatar'])
  async def av(self, ctx, *, user: discord.Member): 
      av = user.display_avatar.url
      embed = discord.Embed(title="{}'s pfp".format(user.name), description="Here it is!", color=bot_embed_color)
      embed.set_image(url=av)
      await ctx.send(embed=embed)


  @commands.command(aliases=['server', 'serverinfo'])
  async def sinfo(self, ctx):
      embed = discord.Embed(title=f"{ctx.guild.name}", description="Here is the server info :-", color=bot_embed_color)
      embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
      embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
      embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
      embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
      embed.set_thumbnail(url=f"{ctx.guild.icon}")
      await ctx.reply(embed=embed)

  @commands.command(aliases = ["timezone", "timing"])
  async def time(self, ctx, * , location):
    details = location.replace(" ", "+")
    r = requests.get(f"https://timezone.abstractapi.com/v1/current_time/?api_key={timezone_api_key}&location={details}")
    res = r.json()
    timezone_location = str(res['timezone_location'])
    raw_time = str(res['datetime'])
    datetime_time = datetime.strptime(raw_time, "%Y-%m-%d %H:%M:%S")
    time = str(datetime_time.strftime("%I:%M %p"))
    date = str(datetime_time.strftime("%d %B %Y"))
    embedVar = disnake.Embed(title=f"Time in {location} is {time}", description=f'''{date}\nTimezone - {timezone_location}''', color=bot_embed_color)
    embedVar.set_thumbnail(url="https://i.pinimg.com/originals/26/be/b0/26beb09153b8df233d82e66bef3edfbb.jpg")
    await ctx.reply(embed=embedVar)

  @commands.command()
  async def recipe(self, ctx, *, food_name):
    food = food_name.replace(" ", "+")
    api_url = f"https://api.edamam.com/api/recipes/v2?type=public&q={food}&app_id={edamam_api_recipe_app_id}&app_key={edamam_api_recipe_app_key}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as resp:
            res = await resp.json()
    ing = res['hits'][0]['recipe']['ingredients']
    naam = res["hits"][0]["recipe"]["label"]
    url = res["hits"][0]["recipe"]["url"]
    image = res["hits"][0]["recipe"]["image"]
    inge = ""
    for ingredient in ing:
        inge += f"{ingredient['text']}\n-------\n"
    embed = disnake.Embed(title=naam, url=url, description=inge, color=bot_embed_color)
    embed.set_thumbnail(url=image)
    await ctx.reply(embed=embed)


  @commands.command(aliases=['geolocate', 'iptogeo', 'iptolocation', 'ip2geo', 'ip'])
  async def geoip(self, ctx, *, ipaddr: str = '1.3.3.7'): 
      r = requests.get(f'http://extreme-ip-lookup.com/json/{ipaddr}?key={extreme_ip_api_key}')
      geo = r.json()
      em = discord.Embed()
      fields = [
          {'name': 'IP', 'value': geo['query']},
          {'name': 'ipType', 'value': geo['ipType']},
          {'name': 'Country', 'value': geo['country']},
          {'name': 'City', 'value': geo['city']},
          {'name': 'Continent', 'value': geo['continent']},
          {'name': 'Country', 'value': geo['country']},
          {'name': 'IPName', 'value': geo['ipName']},
          {'name': 'ISP', 'value': geo['isp']},
          {'name': 'Latitute', 'value': geo['lat']},
          {'name': 'Longitude', 'value': geo['lon']},
          {'name': 'Org', 'value': geo['org']},
          {'name': 'Region', 'value': geo['region']},
          {'name': 'Status', 'value': geo['status']},
      ]
      for field in fields:
          if field['value']:
              em.add_field(name=field['name'], value=field['value'], inline=True)
      return await ctx.send(embed=em)

  @commands.command(aliases=['wikiped', 'wikipedia'])
  async def wiki(self, ctx, *, query: str):
      global wikipedia_language
      wikipedia_language = "en"
      try:
          page=wikipedia.page(wikipedia.search(query)[0])
      except wikipedia.exceptions.DisambiguationError as e:
          counter=0
          while page is None:
              try:
                  page=wikipedia.page(e.options[counter])
              except:
                  counter+=1
      except IndexError as e:
          await ctx.send(languages[guild_language.setdefault(str(ctx.guild.id), "en")]["wikipedia_page_error"])
          print(e)
          return
      summary=page.summary.split("\n")[0]
      if len(summary)>2048:
          summary=summary[:2045]+"..."
      embed=discord.Embed(colour=0xfefefe,
                          title=page.title,
                          description=summary,
                          url=page.url,)
      embed.set_author(name="Wikipedia",
                      icon_url="https://cdn.discordapp.com/attachments/601676952134221845/799319569025335406/wikipedia.png",
                      url="https://www.wikipedia.org/")
      if page.images:
          embed.set_thumbnail(url=page.images[0])
      await ctx.send(embed=embed)

  @commands.command()
  async def truth(self, ctx, rating = None):
    if rating is None:
      r = requests.get(f"https://api.truthordarebot.xyz/api/truth")
      res = r.json()
      Tile = f"Here is a truth for you"
      Desc = res['question']
      embed=discord.Embed(title=Tile, description=Desc, color=bot_embed_color)
      await ctx.reply(embed=embed)
    else:
      try: 
        r = requests.get(f"https://api.truthordarebot.xyz/api/truth/?rating={rating}")
        res = r.json()
        Tile = f"Here is a {rating} rated question for you"
        Desc = res['question']
        embed=discord.Embed(title=Tile, description=Desc, color=bot_embed_color)
        await ctx.reply(embed=embed)
      except:
        await ctx.reply("Please send a valid rating!! Valid parameters are `pg`,`pg13`,`r`")


  @commands.command()
  async def question(self, ctx):
    r = requests.get('https://opentdb.com/api.php?amount=1')
    res = json.loads(r.text)
    question1 = res['results'][0]['question']
    question = html.unescape(question1)
    correct_answer = res['results'][0]['correct_answer']
    category = res['results'][0]['category']
    difficulty = res['results'][0]['difficulty']
    em = disnake.Embed(title=category, description=question,colour=bot_embed_color)
    em.add_field(name="Correct Answer :-", value=f"||{correct_answer}||")
    em.set_footer(text=f"Difficulty : {difficulty}")
    await ctx.reply(embed=em)


  @commands.command()
  async def dare(self, ctx, rating = None):
    if rating is None:
      r = requests.get(f"https://api.truthordarebot.xyz/api/dare")
      res = r.json()
      Tile = f"Here is a dare for you"
      Desc = res['question']
      embed=discord.Embed(title=Tile, description=Desc, color=bot_embed_color)
      await ctx.reply(embed=embed)
    else:
      try: 
        r = requests.get(f"https://api.truthordarebot.xyz/api/dare/?rating={rating}")
        res = r.json()
        Tile = f"Here is a {rating} rated question for you"
        Desc = res['question']
        embed=discord.Embed(title=Tile, description=Desc, color=bot_embed_color)
        await ctx.reply(embed=embed)
      except:
        await ctx.reply("Please send a valid rating!! Valid parameters are `pg`,`pg13`,`r`")

  @commands.command()
  async def pypi(self, ctx, package):
    r = requests.get(f"https://pypi.org/pypi/{package}/json")
    try:
        res = r.json()
        author = res['info']['author']
        embed = disnake.Embed(title=res['info']['name'], url = f"https://pypi.org/project/{package}/", description=f"{res['info']['summary']}\n\n\n", color=bot_embed_color)
        embed.set_author(name="PyPI", url="https://pypi.org/", icon_url="https://thumbs.dreamstime.com/b/python-icon-filled-python-icon-website-design-mobile-app-development-python-icon-filled-development-collection-155362649.jpg")
        embed.add_field(name="More Details :- \n\n", value=res['info']['home_page'], inline=False)
        embed.set_thumbnail(url=f"https://pypi.org/static/images/twitter.6fecba6f.jpg")
        await ctx.reply(embed=embed)
    except:
        embed = disnake.Embed(title="Package Not Found!", description="Please check the spelling of the package name and try again!", color=bot_embed_color)
        await ctx.reply(embed=embed)

  @commands.command()
  async def remind(self, ctx, time = None, *, reminder = None):
    if time.isdigit():
      time = int(time)
      if time > 0:
        embedVar = disnake.Embed(title=f"Reminding in {time} seconds!", description=f"Reason: {reminder}", color=bot_embed_color)
        await ctx.reply(embed=embedVar)
        await asyncio.sleep(time)
        embed = disnake.Embed(title=f"Reminder!", description=f"Reason: {reminder}", color=bot_embed_color)
        await ctx.reply(f"{ctx.author.mention}", embed=embed)
      else:
        embed = disnake.Embed(title="Invalid Time!", description="Please enter a valid time!", color=bot_embed_color)
        await ctx.reply(embed=embed)
    else:
      embed = disnake.Embed(title="Invalid Time!", description="Please enter a valid time!", color=bot_embed_color)
      await ctx.reply(embed=embed)


def setup(bot):
  bot.add_cog(Utilities(bot))
