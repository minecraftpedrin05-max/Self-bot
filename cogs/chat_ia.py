import json
import re
from groq import Groq
import discord
from discord.ext import commands

with open("config.json", encoding="utf-8") as f:
    cfg = json.load(f)

client = Groq(api_key=cfg["groq_key"])
LINK_SERVIDOR = "https://discord.gg/kvTg7GxvR"

# Histórico de conversas por usuário
historico = {}

class ChatIA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignora mensagens do próprio bot ou de bots
        if message.author == self.bot.user or message.author.bot:
            return

        # Só responde em mensagem direta (PV)
        if not isinstance(message.channel, discord.DMChannel):
            return

        user_id = message.author.id
        texto = message.content.strip()

        # Inicializa histórico se for primeira mensagem
        if user_id not in historico:
            historico[user_id] = []

        historico[user_id].append({"role": "user", "content": texto})
        # Mantém só as últimas 6 mensagens pra não ficar grande
        historico[user_id] = historico[user_id][-6:]

        # Prompt que DIZ pra IA como se comportar
        sistema = f"""Você é uma pessoa conversando no Discord. Seja natural, amigável e direto.
Se o usuário disser que NÃO vai entrar, que não quer, ou recusar de qualquer forma — TENTE CONVENCER ele de forma educada mas insistente.
Diga que o servidor é bom, que vale a pena, peça pra dar uma chance. Sempre mencione o link: {LINK_SERVIDOR}
Se ele fizer qualquer pergunta, responda normalmente e depois traga o assunto do servidor de leve.
Não fale que você é IA, seja direto e humano. Seja breve! Responda em português."""

        try:
            resposta = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": sistema},
                    *historico[user_id]
                ],
                temperature=0.7,
                max_tokens=350
            )

            texto_resposta = resposta.choices[0].message.content.strip()
            historico[user_id].append({"role": "assistant", "content": texto_resposta})

            await message.channel.send(texto_resposta)
            print(f"[IA] PV de {message.author}: {texto} → {texto_resposta[:60]}...")

        except Exception as e:
            print(f"[ERRO IA] {e}")
            await message.channel.send("Eita, deu um bug aqui 😅 Pode falar de novo?")


async def setup(bot):
    await bot.add_cog(ChatIA(bot))

