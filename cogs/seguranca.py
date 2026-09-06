import time
import random
import asyncio
import discord
from discord.ext import commands

class Seguranca(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # 🚨 ESTADOS DA CONTA
        self.estado_alerta = False
        self.acesso_limitado = False
        self.bloqueio_dm = False
        self.tentativas_falhas = 0
        self.mensagens_sem_resposta = 0
        
        # 📊 Contadores
        self.mensagens_enviadas = 0
        self.mensagens_por_janela = 0
        self.janela_inicio = time.time()
        self.dia_inicio = time.time()
        
        # ⚠️ LIMITES DE SEGURANÇA (conservador = mais seguro)
        self.MAX_POR_JANELA = 10        # 10 DMs em 2 min
        self.JANELA_SEGUNDOS = 120
        self.MAX_POR_DIA = 35           # 35 por dia
        self.MAX_FALHAS = 4             # 4 falhas = ALERTA MÁXIMO
        self.MAX_SEM_RESPOSTA = 6
        
        # 🕐 SIMULAÇÃO HUMANA
        self.delay_base = 10           # Delay mínimo
        self.delay_aleatorio = 8       # Variação pra mais
        self.probabilidade_pausa = 0.25 # 25% de chance de fazer pausa longa
        self.ultima_acao = time.time()
        self.em_pausa = False

    # 🎭 SIMULAÇÃO PRINCIPAL — faz o tempo ficar IRREGULAR
    def tempo_humano(self):
        """Retorna um delay ALEATÓRIO e NATURAL, nunca igual"""
        base = self.delay_base
        variacao = random.uniform(-3, self.delay_aleatorio)
        return max(5, base + variacao)  # Nunca menos de 5s

    # 🎭 SIMULA DIGITAÇÃO — espera como se estivesse escrevendo
    async def simular_digitacao(self, canal, min_seg=2, max_seg=6):
        """Mostra 'digitando' e espera tempo aleatório antes de enviar"""
        async with canal.typing():
            await asyncio.sleep(random.uniform(min_seg, max_seg))

    # 🎭 PAUSA ALEATÓRIA — às vezes para por minutos, como uma pessoa
    async def pausa_aleatoria(self):
        """25% de chance de fazer uma pausa longa natural"""
        if random.random() < self.probabilidade_pausa:
            duracao = random.uniform(45, 180)  # 45s a 3min
            print(f"[😴] Pausa natural de {int(duracao)}s...")
            self.em_pausa = True
            await asyncio.sleep(duracao)
            self.em_pausa = False
            return True
        return False

    def resetar_janela(self):
        agora = time.time()
        if agora - self.janela_inicio > self.JANELA_SEGUNDOS:
            self.mensagens_por_janela = 0
            self.janela_inicio = agora
        if agora - self.dia_inicio > 86400:
            self.mensagens_enviadas = 0
            self.dia_inicio = agora
            self.tentativas_falhas = 0
            self.mensagens_sem_resposta = 0
            self.estado_alerta = False

    # 🚨 VERIFICA RISCO ANTES DE TUDO
    def verificar_risco(self):
        self.resetar_janela()
        
        if self.acesso_limitado:
            return False, "🔴 ACESSO LIMITADO — Discord restringiu a conta"
        if self.bloqueio_dm:
            return False, "🔴 DM BLOQUEADO — sistema antispam ativou"
        if self.estado_alerta:
            return False, "🟡 ALERTA ATIVO — esperando normalizar"
        if self.em_pausa:
            return False, "😴 Em pausa natural..."
        
        if self.mensagens_por_janela >= self.MAX_POR_JANELA:
            self.estado_alerta = True
            return False, f"🟡 Limite de janela atingido ({self.mensagens_por_janela})"
        if self.mensagens_enviadas >= self.MAX_POR_DIA:
            return False, f"🟡 Limite diário atingido ({self.mensagens_enviadas})"
        if self.tentativas_falhas >= self.MAX_FALHAS:
            self.estado_alerta = True
            return False, f"🔶 {self.tentativas_falhas} falhas seguidas — risco alto"
        if self.mensagens_sem_resposta >= self.MAX_SEM_RESPOSTA:
            return False, "🟠 Possível shadow ban — ninguém responde"
        
        return True, "✅ Seguro"

    def registrar_envio(self):
        self.mensagens_enviadas += 1
        self.mensagens_por_janela += 1
        self.tentativas_falhas = 0
        self.ultima_acao = time.time()
        print(f"[📊] Hoje: {self.mensagens_enviadas} | Janela: {self.mensagens_por_janela}/{self.MAX_POR_JANELA}")

    def registrar_falha(self):
        self.tentativas_falhas += 1
        if self.tentativas_falhas >= self.MAX_FALHAS:
            self.estado_alerta = True

    # 🛡️ TRATAMENTO DE ERROS — PEGA NA HORA QUE O DISCORD OLHA
    async def tratar_erro(self, erro):
        erro_str = str(erro).lower()
        
        # 🔴 ACESSO LIMITADO (código 50007 / barra vermelha)
        if "50007" in erro_str or "limited access" in erro_str:
            self.acesso_limitado = True
            print("\n" + "!"*70)
            print("🚨🚨 ACESSO LIMITADO DETECTADO 🚨🚨")
            print("-> Discord colocou RESTRIÇÃO na conta!")
            print("-> RESOLVA no celular e NÃO USE por 2-4 horas")
            print("!"*70 + "\n")
            return "PARAR_TUDO"
        
        # 🔴 DM BLOQUEADO / abrindo rápido
        if "40003" in erro_str or "opening direct messages too fast" in erro_str:
            self.bloqueio_dm = True
            print("\n" + "!"*70)
            print("🚨 DM BLOQUEADO — antispam detectou velocidade 🚨")
            print("-> PARANDO 1 HORA inteira!")
            print("!"*70 + "\n")
            return "PARAR_1H"
        
        # ⚡ RATE LIMIT GLOBAL
        if isinstance(erro, discord.HTTPException) and getattr(erro, 'status', None) == 429:
            self.estado_alerta = True
            print("\n" + "!"*70)
            print("⚡ RATE LIMIT GLOBAL — Discord MONITORANDO ⚡")
            print("-> PARANDO 20 MINUTOS!")
            print("!"*70 + "\n")
            return "PARAR_20MIN"
        
        # 🔐 CAPTCHA / Verificação
        if "captcha" in erro_str or "verification" in erro_str or "challenge" in erro_str:
            self.estado_alerta = True
            print("\n" + "="*70)
            print("🔐 CAPTCHA PEDIDO — Discord te sinalizou!")
            print("-> RESOLVA AGORA no celular e PARE por 2 HORAS")
            print("="*70 + "\n")
            return "PARAR_2H"
        
        self.registrar_falha()
        return "CONTINUAR"

    # 📩 MONITORA PV — reset alerta quando alguém responde
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return
        if isinstance(message.channel, discord.DMChannel):
            print(f"[📩 PV] {message.author}: {message.content[:40]}")
            self.mensagens_sem_resposta = 0
            self.tentativas_falhas = 0
            if self.estado_alerta and self.tentativas_falhas == 0:
                self.estado_alerta = False  # Sinal de vida = conta ok

async def setup(bot):
    await bot.add_cog(Seguranca(bot))

