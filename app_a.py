# bot2.py
import os
import discord
from dotenv import load_dotenv
from api_gpt import get_movie_guessing_game_response

load_dotenv()
bot2_token = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client2 = discord.Client(intents=intents)

# 두 번째 봇의 메시지 기록 저장
bot2_messages = []

@client2.event
async def on_ready():
    print(f'{client2.user} 봇2가 온라인 상태입니다!')

@client2.event
async def on_message(message):
    # 첫 번째 봇의 시작 신호를 감지하고 인사말을 보냄
    if message.content == "!startgame" and message.author != client2.user:
        bot2_messages.append({"role": "user", "content": "반가워요! 게임 규칙을 설명해드릴게요."})
        response = get_movie_guessing_game_response(bot2_messages)
        bot2_messages.append({"role": "assistant", "content": response})
        await message.channel.send("반가워요! 게임 규칙을 설명해드릴게요.")
        await message.channel.send(response)

    elif message.author.bot and message.author != client2.user:
        bot2_messages.append({"role": "user", "content": message.content})
        response = get_movie_guessing_game_response(bot2_messages)
        bot2_messages.append({"role": "assistant", "content": response})
        await message.channel.send(response)

client2.run(bot2_token)
