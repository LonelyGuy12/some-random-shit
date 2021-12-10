import disnake as discord
import disnake
from disnake.ext import commands
import random
import praw
import requests
import aiohttp

bot_embed_color = 0x4548a8

class Roleplay(commands.Cog):

  def __init__(self, bot):
    self.bot = bot


  @commands.command(aliases=['patting'])
  async def pat(self, ctx, mentioned_member: disnake.Member):
    r = requests.get("https://api.waifu.pics/sfw/pat")
    res = r.json()
    em = disnake.Embed(description=f"**{str(ctx.author.mention)} _pats_ {str(mentioned_member.mention)}**", color=bot_embed_color) 
    em.set_image(url=res['url'])
    await ctx.reply(embed=em)

  @commands.command(aliases=['kissing', "kisss"])
  async def kiss(self, ctx, mentioned_member: disnake.Member):
    r = requests.get("https://api.waifu.pics/sfw/kiss")
    res = r.json()
    em = disnake.Embed(description=f"**{str(ctx.author.mention)} _kisses_ {str(mentioned_member.mention)}**", color = bot_embed_color) 
    em.set_image(url=res['url'])
    await ctx.reply(embed=em)

  @commands.command(aliases=['hfive', "hfv"])
  async def highfive(self, ctx, mentioned_member: disnake.Member):
    r = requests.get("https://api.waifu.pics/sfw/kiss")
    res = r.json()
    em = disnake.Embed(description=f"**{str(ctx.author.mention)} _gives a highfive to_ {str(mentioned_member.mention)}**") 
    em.set_image(url=res['url'])
    await ctx.reply(embed=em)


def setup(bot):
  bot.add_cog(Roleplay(bot))
