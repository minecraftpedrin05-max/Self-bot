import random
from discord.ext import commands

piadas = [
    "Por que o programador foi ao médico?\nPorque ele tinha muitos bugs! 🐛",
    "O que o Python disse pro Java?\nVocê tem classe, mas eu tenho estilo! 😎",
    "Por que o Discord baniram o selfbot?\nPorque ele era muito autêntico demais! 💀",
    "O que é um bot sem internet?\nUm robô inútil! 🤖📉",
    "Por que eu uso selfbot?\nPorque fazer manual é coisa de quem tem tempo! 💀🔥"
]

perguntas_8ball = [
    "Com certeza ✅",
    "Sem dúvida nenhuma 🎯",
    "Pode contar com isso 💪",
    "Não tenho certeza 🤔",
    "Pergunte mais tarde ⏳",
    "Não conte com isso ❌",
    "Definitivamente não 🚫",
    "Muito duvidoso 🤨"
]

class DiversaoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="piada")
    async def piada(self, ctx):
        await ctx.send(random.choice(piadas))

    @commands.command(name="dado")
    async def dado(self, ctx):
        d1 = random.randint(1,6)
        d2 = random.randint(1,6)
        await ctx.send(f"🎲 Dado 1: **{d1}**\n🎲 Dado 2: **{d2}**\nTotal: **{d1+d2}**")

    @commands.command(name="8ball")
    async def bola8(self, ctx, *, pergunta):
        await ctx.send(f"🎱 **Pergunta:** {pergunta}\n🔮 **Resposta:** {random.choice(perguntas_8ball)}")

async def setup(bot):
    await bot.add_cog(DiversaoCog(bot))
       
