import time
import asyncio
from datetime import datetime
from discord.ext import commands

class SegurancaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # ═══════════ CONTROLES GLOBAIS DE SEGURANÇA ═══════════
        # Sinalizador de execução — quando fica False, TUDO para imediatamente
        self.bot.em_execucao = True

        # Contadores de atividade
        self.bot.mensagens_mandadas = 0
        self.bot.mensagens_no_intervalo = 0
        self.bot.erros_detectados = 0
        self.bot.rate_limit_atingido = False

        # ═══════════ LIMITES DE SEGURANÇA ═══════════
        # Limite padrão de mensagens por hora — NÃO recomendado passar disso
        self.limite_por_hora_normal = 80
        self.limite_por_hora_seguro = 50
        self.limite_atual = self.limite_por_hora_normal

        # Controle de tempo
        self.tempo_inicio_intervalo = time.time()
        self.duracao_intervalo = 3600  # 1 hora em segundos

        # Detecção de comportamento suspeito
        self.contador_bloqueios = 0
        self.mensagens_ignoradas = 0
        self.ultima_verificacao = time.time()

        # Modo de operação
        self.modo_seguro_ativo = False
        self.pausa_automatica = False

        print("🛡️ [SEGURANÇA] Sistema inicializado com todos os módulos carregados")
        print(f"🛡️ [SEGURANÇA] Limite atual: {self.limite_atual} mensagens/hora")
        print(f"🛡️ [SEGURANÇA] Modo seguro: {'ATIVADO' if self.modo_seguro_ativo else 'DESATIVADO'}")

    # ═══════════ EVENTO QUANDO BOT FICA PRONTO ═══════════
    @commands.Cog.listener()
    async def on_ready(self):
        print("\n" + "═"*60)
        print("🛡️  SISTEMA DE SEGURANÇA — ATIVO E MONITORANDO")
        print("═"*60)
        print(f"✅ Modo de operação: {'SEGURO' if self.modo_seguro_ativo else 'NORMAL'}")
        print(f"✅ Limite de mensagens: {self.limite_atual} por hora")
        print(f"✅ Contador de mensagens: {self.bot.mensagens_mandadas}")
        print(f"✅ Erros registrados: {self.bot.erros_detectados}")
        print("═"*60 + "\n")

    # ═══════════ COMANDO +PARAR — PARA TUDO IMEDIATAMENTE ═══════════
    @commands.command(name="parar")
    async def parar_tudo(self, ctx):
        """🛑 Para QUALQUER processo rodando no bot AGORA"""

        # Desativa a execução — qualquer loop em massa vai verificar e parar
        self.bot.em_execucao = False
        self.pausa_automatica = False

        # Reseta contadores de atividade
        self.bot.mensagens_mandadas = 0
        self.bot.mensagens_no_intervalo = 0
        self.tempo_inicio_intervalo = time.time()

        # Log no terminal
        print("\n" + "█"*60)
        print("🛑 COMANDO +PARAR EXECUTADO — TODOS OS PROCESSOS ENCERRADOS")
        print(f"🛑 Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"🛑 Mensagens mandadas nesta sessão: {self.bot.mensagens_mandadas}")
        print("█"*60 + "\n")

        # Resposta no chat
        mensagem = """
🛑 ═══════════════════════════════════════════════
   PARANDO TUDO AGORA!
   Todos os processos foram encerrados imediatamente.
   Bot em modo de espera — seguro para continuar.
═══════════════════════════════════════════════════
        """
        await ctx.send(mensagem, delete_after=5)

    # ═══════════ COMANDO +MODO_SEGURO — PROTEÇÃO MÁXIMA ═══════════
    @commands.command(name="modo_seguro")
    async def ativar_modo_seguro(self, ctx):
        """🛡️ Ativa proteção MÁXIMA — delay sobe, limite cai"""

        self.modo_seguro_ativo = True
        self.limite_atual = self.limite_por_hora_seguro

        # Ajusta o delay no config se disponível
        if hasattr(self.bot, "config") and "delay_segundos" in self.bot.config:
            self.bot.config["delay_segundos"] = 15

        # Log no terminal
        print("\n🛡️ [MODO SEGURO] PROTEÇÃO MÁXIMA ATIVADA")
        print(f"🛡️ Delay alterado para: 15 segundos")
        print(f"🛡️ Limite alterado para: {self.limite_atual} mensagens por hora")
        print("🛡️ Recomendado: não enviar mais de 50 pessoas por vez\n")

        mensagem = f"""
🛡️ ═══════════════════════════════════════
   🛡️  MODO SEGURO ATIVADO — PROTEÇÃO MÁXIMA
═══════════════════════════════════════════
⏱️  Delay entre mensagens: 15 segundos
📊 Limite por hora: {self.limite_atual} mensagens
⚠️  Recomendação: máximo 30-40 pessoas por vez
═══════════════════════════════════════════
        """
        await ctx.send(mensagem, delete_after=6)

    # ═══════════ COMANDO +MODO_NORMAL — VOLTA AO PADRÃO ═══════════
    @commands.command(name="modo_normal")
    async def ativar_modo_normal(self, ctx):
        """🔄 Volta ao modo padrão — delay 5s, limite 80/hora"""

        self.modo_seguro_ativo = False
        self.limite_atual = self.limite_por_hora_normal

        if hasattr(self.bot, "config") and "delay_segundos" in self.bot.config:
            self.bot.config["delay_segundos"] = 5

        print("\n✅ [MODO NORMAL] Configurações padrão restauradas")
        print(f"✅ Delay: 5 segundos | Limite: {self.limite_atual}/hora\n")

        mensagem = f"""
✅ ═══════════════════════════════════════
   MODO NORMAL — Configurações padrão
═══════════════════════════════════════════
⏱️  Delay: 5 segundos
📊 Limite: {self.limite_atual} mensagens por hora
⚠️  Atenção: não use em servidores muito grandes!
═══════════════════════════════════════════
        """
        await ctx.send(mensagem, delete_after=5)

    # ═══════════ COMANDO +STATUS_SEGURANÇA — RELATÓRIO COMPLETO ═══════════
    @commands.command(name="status_seguranca")
    async def mostrar_status(self, ctx):
        """📊 Mostra relatório completo de segurança e estatísticas"""

        # Calcula tempo restante do intervalo
        tempo_passado = time.time() - self.tempo_inicio_intervalo
        minutos_restantes = max(0, int((self.duracao_intervalo - tempo_passado) / 60))
        porcentagem = int((self.bot.mensagens_no_intervalo / self.limite_atual) * 100) if self.limite_atual > 0 else 0

        barra = "█" * int(porcentagem / 5) + "░" * (20 - int(porcentagem / 5))

        status_msg = f"""
📊 ═══════════════════════════════════════════════════════
   RELATÓRIO DE SEGURANÇA — VECK SelfBot
══════════════════════════════════════════════════════════
✅ ESTADO:        {'EXECUTANDO' if self.bot.em_execucao else 'PARADO'}
🛡️ MODO:         {'SEGURO (proteção máxima)' if self.modo_seguro_ativo else 'NORMAL'}
📩 MENSAGENS ENVIADAS: {self.bot.mensagens_mandadas}
📊 DESTE PERÍODO:     {self.bot.mensagens_no_intervalo}/{self.limite_atual} ({porcentagem}%)
   [{barra}]
⏱️ TEMPO RESTANTE:    {minutos_restantes} minutos até reset do contador
⚠️ ERROS DETECTADOS:   {self.bot.erros_detectados}
🚫 BLOQUEIOS:         {self.contador_bloqueios}
⏱️ DELAY ATUAL:       {self.bot.config.get('delay_segundos', 5)} segundos
══════════════════════════════════════════════════════════
💀 Desenvolvido por pedrin | VECK SelfBot
        """
        await ctx.send(status_msg, delete_after=12)

    # ═══════════ COMANDO +RESET_CONTADOR — ZERA TUDO MANUALMENTE ═══════════
    @commands.command(name="reset_contador")
    async def resetar_contadores(self, ctx):
        """🔄 Zera todos os contadores de atividade e erros"""

        self.bot.mensagens_mandadas = 0
        self.bot.mensagens_no_intervalo = 0
        self.bot.erros_detectados = 0
        self.contador_bloqueios = 0
        self.tempo_inicio_intervalo = time.time()
        self.bot.rate_limit_atingido = False

        print("🔄 [SEGURANÇA] TODOS os contadores foram resetados manualmente")

        await ctx.send("""
🔄 ═══════════════════════════════════════
   CONTADORES RESETADOS COM SUCESSO
═══════════════════════════════════════════
✅ Mensagens enviadas: 0
✅ Erros detectados: 0
✅ Bloqueios: 0
✅ Tempo de intervalo reiniciado
═══════════════════════════════════════════
        """, delete_after=5)

    # ═══════════ MÉTODOS INTERNOS DE VERIFICAÇÃO ═══════════
    # Esses métodos são chamados automaticamente pelo sistema de divulgação

    def verificar_limite_hora(self) -> bool:
        """
        Verifica se ainda pode enviar mensagens dentro do limite por hora.
        Retorna True = pode continuar, False = parar/pausar
        """
        agora = time.time()

        # Reset automático do contador a cada hora
        if agora - self.tempo_inicio_intervalo >= self.duracao_intervalo:
            self.bot.mensagens_no_intervalo = 0
            self.tempo_inicio_intervalo = agora
            print(f"\n🔄 [SEGURANÇA] Contador de hora resetado automaticamente — {datetime.now().strftime('%H:%M:%S')}")

        # Verifica se atingiu o limite
        if self.bot.mensagens_no_intervalo >= self.limite_atual:
            print(f"\n🚨 [SEGURANÇA] LIMITE ATINGIDO! {self.bot.mensagens_no_intervalo}/{self.limite_atual} mensagens")
            print(f"🚨 [SEGURANÇA] Pausa automática ativada — aguarde 1 hora ou use +reset_contador")
            self.pausa_automatica = True
            return False
        else:
            self.pausa_automatica = False

        return True

    def registrar_mensagem_enviada(self):
        """Registra cada mensagem enviada nos contadores"""
        self.bot.mensagens_mandadas += 1
        self.bot.mensagens_no_intervalo += 1

        # A cada 10 mensagens, mostra o progresso no terminal
        if self.bot.mensagens_mandadas % 10 == 0:
            porcentagem = int((self.bot.mensagens_no_intervalo / self.limite_atual) * 100)
            print(f"📩 [PROGRESSO] {self.bot.mensagens_no_intervalo}/{self.limite_atual} — {porcentagem}% do limite")

    def registrar_erro(self, tipo_erro: str = "desconhecido", detalhes: str = "") -> bool:
        """
        Registra erros de comunicação com o Discord.
        Retorna True = deve PARAR completamente, False = pode continuar
        """
        self.bot.erros_detectados += 1
        agora = datetime.now().strftime("%H:%M:%S")

        # Classifica o tipo de erro
        if "rate limit" in tipo_erro.lower() or "429" in str(tipo_erro):
            self.bot.rate_limit_atingido = True
            print(f"\n🚨 [{agora}] RATE LIMIT DETECTADO! O Discord está restringindo as requisições.")
            print(f"   → Detalhes: {detalhes}")
            print(f"   → RECOMENDAÇÃO: Aumente o delay ou ative +modo_seguro IMEDIATAMENTE")
        elif "bloqueado" in tipo_erro.lower() or "cannot send messages" in str(tipo_erro).lower():
            self.contador_bloqueios += 1
            print(f"\n⚠️ [{agora}] MENSAGEM BLOQUEADA — A pessoa fechou PV ou Discord bloqueou")
            print(f"   → Detalhes: {detalhes}")
            if self.contador_bloqueios >= 5:
                print(f"🚨 [{agora}] MUITAS MENSAGENS BLOQUEADAS — Possível detecção de spam! PARANDO!")
                return True  # Deve parar
        elif "unauthorized" in tipo_erro.lower() or "401" in str(tipo_erro):
            print(f"\n🔴 [{agora}] ERRO DE AUTORIZAÇÃO — Token inválido ou expirado!")
            print(f"   → Atualize o token no config.json")
            return True
        else:
            print(f"⚠️ [{agora}] Erro registrado: {tipo_erro}")
            if detalhes:
                print(f"   → Detalhes: {detalhes}")

        # Se acumular 5 erros de qualquer tipo, avisa pra parar
        if self.bot.erros_detectados >= 5:
            print(f"\n🚨 [{agora}] {self.bot.erros_detectados} ERROS ACUMULADOS — RECOMENDADO PARAR AGORA!")
            return True

        return False

    def verificar_atividade_suspeita(self) -> bool:
        """
        Verifica padrões que podem levantar suspeita no Discord.
        Retorna True = atividade normal, False = suspeito/detectado
        """
        # Muitos bloqueios seguidos = alerta vermelho
        if self.contador_bloqueios >= 10:
            print("🚨 [ALERTA CRÍTICO] 10+ mensagens bloqueadas — Discord pode estar monitorando!")
            return False

        # Rate limit repetido = alerta
        if self.bot.rate_limit_atingido and self.bot.erros_detectados >= 3:
            print("🚨 [ALERTA] Rate limit repetido — padrão de detecção de spam!")
            return False

        return True

async def setup(bot):
    await bot.add_cog(SegurancaCog(bot))
    print("🛡️ [SEGURANÇA] Módulo de segurança carregado com sucesso — sistema completo ativo")
        
