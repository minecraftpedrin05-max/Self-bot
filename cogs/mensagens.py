from discord.ext import commands

class MensagensCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dizer")
    async def dizer(self, ctx, *, texto):
        await ctx.message.delete()
        await ctx.send(texto)

    @commands.command(name="maiusculo")
    async def maiusculo(self, ctx, *, texto):
        await ctx.message.delete()
        await ctx.send(texto.upper())

    @commands.command(name="minusculo")
    async def minusculo(self, ctx, *, texto):
        await ctx.message.delete()
        await ctx.send(texto.lower())

    @commands.command(name="inverter")
    async def inverter(self, ctx, *, texto):
        await ctx.message.delete()
        await ctx.send(texto[::-1])

async def setup(bot):
    await bot.add_cog(MensagensCog(bot))
  
