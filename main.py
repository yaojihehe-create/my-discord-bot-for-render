import discord
import os
import random
from flask import Flask
from threading import Thread

# Flaskのアプリケーションインスタンスを作成
app = Flask('')
# Botがすでに起動しているかどうかを記録するフラグ
app.bot_started = False 

# Botのロジック部分をカプセル化
def start_discord_bot():
    # ランダムに選択する応答メッセージリスト
    RANDOM_RESPONSES = [
        "「このうさぎさんは、笑うこともできるんです」﻿",
        "「どれだけ間が悪くとも、捕まえるまで絶対にあきらめません！」﻿",
        "「バリスタの力…！」﻿",
        "「ココアさんのバカー！」﻿",
        "「物理部好きです」"
    ]
    
    TOKEN = os.getenv("DISCORD_TOKEN") 
    intents = discord.Intents.default()
    intents.message_content = True 
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print('---------------------------------')
        print(f'Botがログインしました: {client.user.name}')
        print('---------------------------------')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if client.user.mentioned_in(message):
            response = random.choice(RANDOM_RESPONSES)
            await message.channel.send(f'{message.author.mention} {response}')
            return 
    
    if TOKEN:
        client.run(TOKEN)
    else:
        print("エラー: Botトークンが設定されていません。")

# WebアクセスがあったときにBotの起動を試みるエンドポイント
@app.route('/')
def home():
    # フラグを確認し、Botがまだ起動していない場合のみ起動する
    if not app.bot_started:
        thread = Thread(target=start_discord_bot)
        thread.start()
        app.bot_started = True # フラグを立てて、二度と起動させない
        return "Discord Bot is initializing..."
    return "Discord Bot is running."
