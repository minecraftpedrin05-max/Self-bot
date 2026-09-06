import discord
import json
import sys
import os
from discord.ext import commands

# ──────────────────── CORES DO TERMINAL ────────────────────
VERDE = "\033[92m"
VERMELHO = "\033[91m"
AMARELO = "\033[93m"
CIANO = "\033[96m"
ROXO = "\033[95m"
RESET = "\033[0m"

# ──────────────────── LOGO INICIAL ────────────────────
def mostrar_logo():
    logo = f"""{CIANO}
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
{'─'*55}"""
    print(logo)

# ──────────────────── CARREGAR CONFIG ────────────────────
def carregar_config():
    caminho = os.path.join(os.path.dirname(__file__), "config.json")
    if not os.path.exists(caminho):
        print(f"{VERMELHO}[ERRO]{RESET} Arquivo config.json NÃO ENCONTRADO!")
        print(f"{AMARELO}Crie o arquivo com: token, dm_message, delay_segundos{RESET}")
        sys.exit(1)
    
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        print(f"{VERDE}[SUCCESS]{RESET} Configuração carregada!")
        return cfg
    except json.JSONDecodeError as e:
        print(f"{VERMELHO}[ERRO]{RESET} Erro no JSON do config.json: {e}")
        print(f"{AMARELO}Verifique se não faltou vírgula ou aspas!{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{VERMELHO}[ERRO]{RESET} Não foi possível ler config.json: {e}")
        sys.exit(1)

# ──────────────────── INICIALIZAR BOT ────────────────────
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="+", intents=intents, help_command=None)

# ──────────────────── EVENTOS ────────────────────
@bot.event
async def on_ready():
    print(f"\n{VERDE}[✅] BOT CONECTADO!{RESET}")
    print(f"   Usuário: {bot.user}")
    print(f"   ID: {bot.user.id}")
    print(f"   Servidores: {len(bot.guilds)}")
    print(f"   Membros total: {sum(g.member_count for g in bot.guilds)}")
    print(f"{CIANO}{'─'*55}{RESET}\n")

    # Carrega config nos dados do bot pros cogs acessarem
    bot.config = carregar_config()
    bot.em_execucao = True
    bot.mensagens_mandadas = 0
    bot.erros_detectados = 0

    # Carregar todos os módulos
    await carregar_cogs()
    print(f"\n{VERDE}[✅] TODOS OS MÓDULOS CARREGADOS — BOT PRONTO!{RESET}\n")

# ──────────────────── CARREGAR MÓDULOS ────────────────────
async def carregar_cogs():
    cogs = [
        "cogs.seguranca",
        "cogs.ativar",
        "cogs.chat_ia",
        "cogs.status",
        "cogs.limpeza",
        "cogs.informacao",
        "cogs.mensagens",
        "cogs.diversao"
    ]

    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f"{VERDE}[SUCCESS]{RESET} Módulo carregado: {cog}")
        except Exception as e:
            print(f"{VERMELHO}[ERRO]{RESET} Falha ao carregar {cog}")
            print(f"   → {type(e).__name__}: {e}")

# ──────────────────── AJUDA PERSONALIZADA ────────────────────
@bot.command(name="help")
async def ajuda(ctx):
    msg = f"""{CIANO}
📋 VECK SelfBot — Comandos Disponíveis
{RESET}{'─'*40}

📢 DIVULGAÇÃO
  +ativar        → Manda PV pra todos os membros do servidor

🛡️ SEGURANÇA
  +parar         → Para TUDO imediatamente
  +modo_seguro   → Delay 15s, proteção máxima
  +modo_normal   → Volta ao padrão
  +status_seguranca → Mostra contadores e estado

🎭 STATUS
  +jogar [texto]     → Status: Jogando...
  +ouvindo [texto]   → Status: Ouvindo...
  +assistindo [texto]→ Status: Assistindo...
  +parar_status      → Remove status

🧹 LIMPEZA
  +limpar [qtd]  → Apaga suas mensagens (padrão: 10)

ℹ️ INFORMAÇÃO
  +eu            → Seus dados da conta
  +servidor      → Dados do servidor atual

💬 MENSAGENS
  +dizer [texto] → Manda mensagem apagando o comando
  +maiusculo / +minusculo / +inverter

🎮 DIVERSÃO
  +piada / +dado / +8ball [pergunta]

{'─'*40}
💀 Desenvolvido por pedrin
{CIANO}IA Groq ativa no PV automaticamente{RESET}
"""
    await ctx.send(msg)

# ──────────────────── INICIAR ────────────────────
if __name__ == "__main__":
    mostrar_logo()
    bot.config = carregar_config()
    
    try:
        print(f"{AMARELO}[⏳] Conectando ao Discord...{RESET}")
        bot.run(bot.config["token"])
    except discord.LoginFailure:
        print(f"{VERMELHO}[ERRO]{RESET} Token INVÁLIDO ou expirado!")
        print(f"{AMARELO}Verifique o token no config.json{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{VERMELHO}[ERRO FATAL]{RESET} {type(e).__name__}: {e}")
        sys.exit(1)
