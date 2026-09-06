from discord.ext import commands

class SegurancaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Sinalizador global pra parar processos
        self.bot.em_execucao = False

    @commands.command(name="parar")
    async def parar(self, ctx):
        """🛑 Para TODOS os processos imediatamente"""
        self.bot.em_execucao = False
        await ctx.send("🛑 **PARANDO TUDO AGORA!** Todos os processos foram encerrados.", delete_after=5)

    @commands.command(name="modo_seguro")
    async def modo_seguro(self, ctx):
        """🛡️ Ativa proteção máxima: delay 10s"""
        if hasattr(self.bot, "config") and "delay_segundos" in self.bot.config:
            self.bot.config["delay_segundos"] = 10
        await ctx.send("🛡️ **MODO SEGURO ATIVADO!** Delay = 10s, máximo de proteção.", delete_after=5)

async def setup(bot):
    await bot.add_cog(SegurancaCog(bot))
    
