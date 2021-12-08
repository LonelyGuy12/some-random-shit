import disnake as discord
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

def setup(bot):
  bot.add_cog(NSFW(bot))