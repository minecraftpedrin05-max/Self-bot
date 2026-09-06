from discord.ext import commands

class LimpezaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="limpar")
    async def limpar(self, ctx, quantidade: int = 10):
        contador = 0
        async for msg in ctx.channel.history(limit=100):
            if msg.author == self.bot.user and contador < quantidade:
                await msg.delete()
                contador += 1
        await ctx.send(f"✅ Apaguei {contador} mensagens minhas", delete_after=3)

async def setup(bot):
    await bot.add_cog(LimpezaCog(bot))
  
