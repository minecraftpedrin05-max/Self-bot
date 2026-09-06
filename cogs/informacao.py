import discord
from datetime import datetime
from discord.ext import commands

class InformacaoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="eu")
    async def eu(self, ctx):
        user = self.bot.user
        embed = discord.Embed(color=0x2ecc71)
        embed.set_thumbnail(url=user.avatar.url if user.avatar else None)
        embed.add_field(name="Nome", value=str(user), inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Conta criada", value=user.created_at.strftime("%d/%m/%Y"), inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="servidor")
    async def servidor(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title=guild.name, color=0x3498db)
        if guild.icon: embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="Membros", value=str(guild.member_count), inline=True)
        embed.add_field(name="Criado em", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="Canais", value=str(len(guild.channels)), inline=True)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(InformacaoCog(bot))
  
