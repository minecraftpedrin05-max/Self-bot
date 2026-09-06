import discord
from discord.ext import commands

class StatusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jogar")
    async def jogar(self, ctx, *, texto):
        await self.bot.change_presence(activity=discord.Game(name=texto))
        await ctx.message.add_reaction("✅")

    @commands.command(name="ouvindo")
    async def ouvindo(self, ctx, *, texto):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=texto))
        await ctx.message.add_reaction("✅")

    @commands.command(name="assistindo")
    async def assistindo(self, ctx, *, texto):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=texto))
        await ctx.message.add_reaction("✅")

    @commands.command(name="parar_status")
    async def parar_status(self, ctx):
        await self.bot.change_presence(activity=None)
        await ctx.message.add_reaction("✅")

async def setup(bot):
    await bot.add_cog(StatusCog(bot))
  
