import discord
import os
import random
from flask import Flask
from threading import Thread

# Flaskのアプリケーションインスタンスを作成
# RenderはこれをWebサーバーとして認識します。
app = Flask('')

# Botの実行を別スレッドで処理する関数
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
    # Webアクセス時にBotが起動していない場合のみ、Botを別スレッドで起動
    # これにより、Webサーバーは応答し続け、Botは独立して動作します。
    if not hasattr(app, 'bot_thread'):
        app.bot_thread = Thread(target=start_discord_bot)
        app.bot_thread.start()
        return "Discord Bot is initializing..."
    return "Discord Bot is running."

# Botを直接実行するのではなく、Render/gunicornにWebアプリ（app）を渡します。
