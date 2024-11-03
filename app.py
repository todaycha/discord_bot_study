# app.py
import io
import os
import discord
import httpx
from dotenv import load_dotenv
from api_gpt import get_movie_guessing_game_response  # Import the function

load_dotenv()
bot_token = os.getenv("DISCORD_BOT_TOKEN")

# 클라이언트 생성
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# 게임 상태 저장 변수
game_messages = []

# 봇이 준비되었을 때 실행되는 코드
@client.event
async def on_ready():
    print(f'{client.user} 봇이 온라인 상태입니다!')

# 고양이 사진을 가져오는 함수
async def get_cat_image():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get('https://api.thecatapi.com/v1/images/search')
            data = response.json()
            return data[0]['url']
    except Exception as e:
        print(f'고양이 이미지를 가져오는 데 실패했습니다: {e}')
        return ''

# 이미지를 다운로드하여 Discord에 전송 가능한 파일 객체로 변환하는 함수
async def fetch_image(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            image_data = io.BytesIO(response.content)
            return discord.File(fp=image_data, filename="cat.jpg")
        else:
            print("이미지를 다운로드할 수 없습니다.")
            return None

# 메시지 수신 이벤트 처리
@client.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

    if content == '!ping':
        await message.channel.send('Pong!')
    elif content == '!cat':
        cat_image_url = await get_cat_image()
        if cat_image_url:
            file = await fetch_image(cat_image_url)
            if file:
                await message.channel.send(content='여기 귀여운 고양이 사진이 있어요!', file=file)
            else:
                await message.channel.send('고양이 사진을 가져오는 데 실패했습니다.')
        else:
            await message.channel.send('고양이 사진을 가져오는 데 실패했습니다.')
    elif content.startswith('!moviegame'):
        game_messages.clear()  # Reset game state for new session
        game_messages.append({"role": "user", "content": "게임을 시작합니다!"})
        assistant_reply = get_movie_guessing_game_response(game_messages)
        game_messages.append({"role": "assistant", "content": assistant_reply})
        await message.channel.send(assistant_reply)
    elif game_messages:  # If the game has started
        game_messages.append({"role": "user", "content": message.content})
        assistant_reply = get_movie_guessing_game_response(game_messages)
        game_messages.append({"role": "assistant", "content": assistant_reply})
        await message.channel.send(assistant_reply)
    else:
        await message.channel.send(f'받은 메시지: {message.content}')

# Discord 봇 토큰으로 로그인
client.run(bot_token)
