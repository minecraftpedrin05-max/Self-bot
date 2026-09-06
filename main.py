import discord
import json
import sys
import os
from discord.ext import commands

# ✅ SEM INTENTS — na sua versão não precisa!
bot = commands.Bot(command_prefix="+", help_command=None)

# ──────────── CORES ────────────
VERDE = "\033[92m"
VERMELHO = "\033[91m"
AMARELO = "\033[93m"
CIANO = "\033[96m"
RESET = "\033[0m"

# ──────────── LOGO ────────────
def mostrar_logo():
    print(f"""{CIANO}
██╗   ██╗███████╗ ██████╗██╗  ██╗
██║   ██║██╔════╝██╔════╝██║ ██╔╝
██║   ██║█████╗  ██║     █████╔╝ 
╚██╗ ██╔╝██╔══╝  ██║     ██╔═██╗ 
 ╚████╔╝ ███████╗╚██████╗██║  ██╗
  ╚═══╝  ╚══════╝ ╚═════╝╚═╝  ╚═╝
{RESET}
{VERDE}VECK SelfBot{RESET} — Versão 1.0
{AMARELO}Desenvolvido por pedrin 💀{RESET}
{CIANO}Suporte: https://discord.gg/nmDUsAeRxP{RESET}
{'─'*55}""")

# ──────────── CONFIG ────────────
def carregar_config():
    caminho = os.path.join(os.path.dirname(__file__), "config.json")
    if not os.path.exists(caminho):
        print(f"{VERMELHO}[ERRO]{RESET} Arquivo config.json NÃO ENCONTRADO!")
        sys.exit(1)
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"{VERMELHO}[ERRO]{RESET} Erro no config.json: {e}")
        sys.exit(1)

# ──────────── ON READY ────────────
@bot.event
async def on_ready():
    print(f"\n{VERDE}[✅] BOT CONECTADO!{RESET}")
    print(f"   Usuário: {bot.user}")
    print(f"   ID: {bot.user.id}")
    print(f"{CIANO}{'─'*55}{RESET}\n")
    await carregar_cogs()
    print(f"\n{VERDE}[✅] BOT PRONTO — COMANDO +help{RESET}\n")

# ──────────── CARREGAR MÓDULOS ────────────
async def carregar_cogs():
    cogs = ["cogs.seguranca", "cogs.ativar", "cogs.chat_ia", "cogs.status",
            "cogs.limpeza", "cogs.informacao", "cogs.mensagens", "cogs.diversao"]
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f"{VERDE}[OK]{RESET} {cog}")
        except Exception as e:
            print(f"{VERMELHO}[ERRO]{RESET} {cog}: {e}")

# ──────────── AJUDA ────────────
@bot.command(name="help")
async def ajuda(ctx):
    await ctx.send(f"""{CIANO}
📋 VECK SelfBot — Comandos
{RESET}{'─'*40}
📢 +ativar        → Manda PV pra todos do server
🛡️ +parar         → Para tudo imediatamente
🎭 +jogar/ouvindo/assistindo [texto]
🧹 +limpar [qtd]  → Apaga suas mensagens
ℹ️ +eu / +servidor
💬 +dizer [texto]
🎮 +piada / +dado / +8ball
{'─'*40}
💀 Desenvolvido por pedrin
""")

# ──────────── INICIAR ────────────
if __name__ == "__main__":
    mostrar_logo()
    bot.config = carregar_config()
    try:
        print(f"{AMARELO}[⏳] Conectando ao Discord...{RESET}")
        bot.run(bot.config["token"])
    except Exception as e:
        print(f"{VERMELHO}[ERRO FATAL]{RESET} {e}")
        sys.exit(1)

