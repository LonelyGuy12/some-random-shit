import disnake
from disnake.ext import commands
import random
import requests
import aiohttp


class NSFW(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases = ["nwaifu", "nsfwaifu"])
  @commands.is_nsfw()
  async def nsfwwaifu(self, ctx):
    r = requests.get("https://api.waifu.pics/nsfw/waifu")
    res = r.json()
    em = disnake.Embed()
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

  @commands.command(aliases = ["nneko", "nsfneko"])
  @commands.is_nsfw()
  async def nsfwneko(self, ctx):
    r = requests.get("https://api.waifu.pics/nsfw/neko")
    res = r.json()
    em = disnake.Embed()
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

  @commands.command(aliases = ["ntrap", "trap"])
  @commands.is_nsfw()
  async def nsfwtrap(self, ctx):
    r = requests.get("https://api.waifu.pics/nsfw/trap")
    res = r.json()
    em = disnake.Embed()
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

  @commands.command(aliases = ["bjob", "blow"])
  @commands.is_nsfw()
  async def blowjob(self, ctx):
    r = requests.get("https://api.waifu.pics/nsfw/blowjob")
    res = r.json()
    em = disnake.Embed()
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

  @commands.command(aliases = ["nass", "pussy"])
  @commands.is_nsfw()
  async def ass(self, ctx):
    r = requests.get("https://api.waifu.im/nsfw/ass")
    res = r.json()
    em = disnake.Embed()
    gif = res['images'][0]['url']
    em.set_image(url=gif)
    await ctx.send(embed=em)

  @commands.command(aliases = ["boob", "boobs"])
  @commands.is_nsfw()
  async def oppai(self, ctx):
    r = requests.get("https://api.waifu.im/nsfw/oppai")
    res = r.json()
    em = disnake.Embed()
    gif = res['images'][0]['url']
    em.set_image(url=gif)
    await ctx.send(embed=em)

  @commands.command(aliases = ["henta", "hent"])
  @commands.is_nsfw()
  async def hentai(self, ctx):
    r = requests.get("https://api.waifu.im/nsfw/hentai")
    res = r.json()
    em = disnake.Embed()
    gif = res['images'][0]['url']
    em.set_image(url=gif)
    await ctx.send(embed=em)

  @commands.command(aliases = ["nmaid", "nsfmaid"])
  @commands.is_nsfw()
  async def nsfwmaid(self, ctx):
    r = requests.get("https://api.waifu.im/nsfw/maid")
    res = r.json()
    em = disnake.Embed()
    gif = res['images'][0]['url']
    em.set_image(url=gif)
    await ctx.send(embed=em)

  @commands.command(aliases = ["selfie", "nsfwselfies"])
  @commands.is_nsfw()
  async def selfies(self, ctx):
    r = requests.get("https://api.waifu.im/nsfw/selfies")
    res = r.json()
    em = disnake.Embed()
    gif = res['images'][0]['url']
    em.set_image(url=gif)
    await ctx.send(embed=em)

  @commands.command(aliases = ["nsfworal", "noral"])
  @commands.is_nsfw()
  async def oral(self, ctx):
    r = requests.get("https://api.waifu.im/nsfw/oral")
    res = r.json()
    em = disnake.Embed()
    gif = res['images'][0]['url']
    em.set_image(url=gif)
    await ctx.send(embed=em)

def setup(bot):
  bot.add_cog(NSFW(bot))
