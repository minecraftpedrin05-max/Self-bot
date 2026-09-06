import asyncio
import discord
from discord.ext import commands

class Extra(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clear")
    async def clear(self, ctx, quantidade: int = 10):
        """Apaga mensagens suas no chat atual."""
        apagadas = 0
        async for m in ctx.channel.history(limit=100):
            if m.author.id == self.bot.user.id and apagadas < quantidade:
                await m.delete()
                apagadas += 1
                await asyncio.sleep(0.5)
        print(f"[+] {apagadas} mensagens apagadas")

    @commands.command(name="snip")
    async def snip(self, ctx, quantidade: int = 1):
        """Apaga as últimas N mensagens do chat (todas, não só suas)."""
        apagadas = 0
        async for m in ctx.channel.history(limit=quantidade):
            await m.delete()
            apagadas += 1
            await asyncio.sleep(0.4)
        print(f"[+] {apagadas} mensagens removidas")

    @commands.command(name="react")
    async def react(self, ctx, emoji: str, quantidade: int = 1):
        """Reage nas últimas N mensagens do canal."""
        contador = 0
        async for m in ctx.channel.history(limit=quantidade):
            try:
                await m.add_reaction(emoji)
                contador += 1
            except Exception as e:
                print(f"[!] {e}")
            await asyncio.sleep(0.3)
        print(f"[+] Reagiu em {contador} mensagens")

async def setup(bot):
    await bot.add_cog(Extra(bot))