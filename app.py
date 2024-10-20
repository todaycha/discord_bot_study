import io
import os

import discord
import httpx
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv("DISCORD_BOT_TOKEN")

# 클라이언트 생성
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

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
            return data[0]['url']  # 고양이 이미지 URL 반환
    except Exception as e:
        print(f'고양이 이미지를 가져오는 데 실패했습니다: {e}')
        return ''

# 메시지 수신 이벤트 처리
@client.event
async def on_message(message):
    # 봇 자신이 보낸 메시지는 무시
    if message.author.bot:
        return

    # 메시지에 따라 명령어 처리
    content = message.content.lower()  # 소문자로 변환하여 처리

    if content == '!ping':
        # !ping 명령어를 입력하면 pong 응답
        await message.channel.send('Pong!')
    elif content == '!cat':
        # !cat 명령어를 입력하면 고양이 사진 전송
        cat_image_url = await get_cat_image()
        if cat_image_url:
            file = await fetch_image(cat_image_url)
            if file:
                await message.channel.send(
                    content='여기 귀여운 고양이 사진이 있어요!',  # 메시지 내용
                    file=file
                )
            else:
                await message.channel.send('고양이 사진을 가져오는 데 실패했습니다.')
        else:
            await message.channel.send('고양이 사진을 가져오는 데 실패했습니다.')
    else:
        # 다른 메시지는 에코 기능으로 그대로 응답
        await message.channel.send(f'받은 메시지: {message.content}')

# 이미지를 다운로드하여 Discord에 전송 가능한 파일 객체로 변환하는 함수
async def fetch_image(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            # 바이너리 데이터를 BytesIO로 감싸서 discord.File에 전달
            image_data = io.BytesIO(response.content)
            return discord.File(fp=image_data, filename="cat.jpg")
        else:
            print("이미지를 다운로드할 수 없습니다.")
            return None

# Discord 봇 토큰으로 로그인
client.run(bot_token)
