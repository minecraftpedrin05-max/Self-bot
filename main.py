import json
import sys
import platform
import discord
from discord.ext import commands

# ═══════════════════════════════════════════════
# 🎨 TELA DE INÍCIO
# ═══════════════════════════════════════════════

LOGO = """
██╗   ██╗███████╗ ██████╗██╗  ██╗
██║   ██║██╔════╝██╔════╝██║ ██╔╝
██║   ██║█████╗  ██║     █████╔╝ 
╚██╗ ██╔╝██╔══╝  ██║     ██╔═██╗ 
 ╚████╔╝ ███████╗╚██████╗██║  ██╗
  ╚═══╝  ╚══════╝ ╚═════╝╚═╝  ╚═╝
"""

VERDE = "\033[92m"
AZUL = "\033[94m"
AMARELO = "\033[93m"
VERMELHO = "\033[91m"
RESET = "\033[0m"

def inicializar_tela():
    print(f"{AZUL}{LOGO}{RESET}")
    print(f"{AZUL}> Meu Selfbot — Versão 1.0{RESET}")
    print(f"{AZUL}> Use por sua conta e risco — self-bots violam os ToS do Discord{RESET}")
    print(f"{AZUL}> Desenvolvido por pedrin_yt {RESET}")
    print(f"{AZUL}> Suporte: https://discord.gg/nmDUsAeRxP{RESET}")
    print()

def info_sistema():
    print(f"{AMARELO}[INFO]{RESET} Sistema Operacional: {platform.system()} {platform.release()}")
    print(f"{AMARELO}[INFO]{RESET} Plataforma: android / termux")
    print(f"{AMARELO}[INFO]{RESET} Python: {sys.version.split()[0]}")
    print(f"{AMARELO}[INFO]{RESET} discord.py-self: {discord.__version__}")
    print()

# ═══════════════════════════════════════════════
# 🚀 INÍCIO DO BOT
# ═══════════════════════════════════════════════

inicializar_tela()

with open("config.json", encoding="utf-8") as f:
    cfg = json.load(f)

bot = commands.Bot(
    command_prefix="+",
    self_bot=True,
    help_command=None
)

@bot.event
async def on_ready():
    print(f"{AMARELO}[INFO]{RESET} Conectando ao Discord...")
    print(f"{VERDE}[SUCCESS]{RESET} Logado como: {bot.user}")
    print(f"{VERDE}[SUCCESS]{RESET} ID do usuário: {bot.user.id}")
    print(f"{AMARELO}[INFO]{RESET} Prefixo: +")
    print(f"{AMARELO}[INFO]{RESET} Status: dnd")
    print()
    info_sistema()
    print(f"{AMARELO}[INFO]{RESET} Carregando módulos...")

    for cog in ["cogs.seguranca", "cogs.ativar", "cogs.extra", "cogs.chat_ia"]:
        try:
            await bot.load_extension(cog)
            print(f"{VERDE}[SUCCESS]{RESET} Módulo carregado: {cog}")
        except Exception as e:
            print(f"{VERMELHO}[ERRO]{RESET} Falha ao carregar {cog}: {e}")

    print()
    print(f"{VERDE}[SUCCESS]{RESET} Bot pronto! Comandos disponíveis: {len(list(bot.commands))}")
    print(f"{AMARELO}[INFO]{RESET} Digite +help para ver os comandos{RESET}")
    print("-" * 55)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    print(f"{VERMELHO}[ERRO]{RESET} {error}")

try:
    bot.run(cfg["token"])
except Exception as e:
    print(f"{VERMELHO}[ERRO FATAL]{RESET} Não foi possível conectar: {e}")

