import json
import asyncio
import discord
from discord.ext import commands

with open("config.json", encoding="utf-8") as f:
    cfg = json.load(f)

class Ativar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ativar")
    async def ativar(self, ctx):
        guild = ctx.guild
        seg = self.bot.get_cog("Seguranca")
        if not seg:
            print("[!] Segurança não carregada!")
            return

        alvos = [m for m in guild.members
                 if not m.bot and m.id != self.bot.user.id]

        print(f"\n[🚀] Iniciando em: {guild.name} | {len(alvos)} alvos")
        print(f"[🛡️] Modo: SIMULAÇÃO HUMANA ativado | Limite: {seg.MAX_POR_DIA}/dia\n")

        msg = cfg.get("dm_message", "Oi!")
        enviados, falhas, bloqueados = 0, 0, 0

        for membro in alvos:
            # 🚨 VERIFICA RISCO
            seguro, aviso = seg.verificar_risco()
            if not seguro:
                print(f"\n🛑 {aviso}")
                if "PARAR_TUDO" in aviso or "ACESSO LIMITADO" in aviso:
                    break
                elif "PARAR_1H" in aviso:
                    print("[⏳] Esperando 1 hora inteira...")
                    await asyncio.sleep(3600)
                    continue
                elif "PARAR_20MIN" in aviso:
                    print("[⏳] Esperando 20 minutos...")
                    await asyncio.sleep(1200)
                    continue
                elif "PARAR_2H" in aviso:
                    print("[🛑] Resolva o CAPTCHA e espere 2 horas manualmente!")
                    break
                else:
                    print("[🛑] Parando por hoje. Volta amanhã.")
                    break

            # 🎭 SIMULA PAUSA ALEATÓRIA (25% de chance)
            await seg.pausa_aleatoria()

            try:
                # 🎭 SIMULA DIGITAÇÃO — mostra "digitando" antes de enviar
                await seg.simular_digitacao(membro, min_seg=1.5, max_seg=5)
                
                await membro.send(msg)
                enviados += 1
                seg.registrar_envio()
                print(f"  [✅] {membro.name}")

            except discord.Forbidden as e:
                bloqueados += 1
                acao = await seg.tratar_erro(e)
                if acao.startswith("PARAR"):
                    break
            except Exception as e:
                falhas += 1
                acao = await seg.tratar_erro(e)
                if acao == "PARAR_TUDO" or acao == "PARAR_2H":
                    break

            # 🎭 TEMPO ALEATÓRIO ENTRE MENSAGENS — NUNCA igual
            delay = seg.tempo_humano()
            print(f"  [⏳] Esperando {delay:.1f}s...")
            await asyncio.sleep(delay)

        print(f"\n[✅ FINAL] Enviados: {enviados} | Bloqueados: {bloqueados} | Falhas: {falhas}")
        if seg.estado_alerta:
            print("[⚠️] ALERTA — use a conta normalmente no celular por umas horas!")

async def setup(bot):
    await bot.add_cog(Ativar(bot))

