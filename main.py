import discord
import os
import random
from flask import Flask
from threading import Thread

# -----------------
# Webサーバーを起動してBotの24時間稼働を維持する関数
# -----------------
def keep_alive():
    app = Flask('')
    @app.route('/')
    def home():
        return "Bot is alive!"
    # Renderの環境変数を使い、0.0.0.0と環境変数PORTでWebサーバーを起動
    # Webサーバーは別スレッドで実行され、Botの起動をブロックしない
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 8080))
    # 注意：RenderがこのWebサーバーを複数回起動しようとするのが問題の原因でした

# ランダムに選択する応答メッセージリスト
RANDOM_RESPONSES = [
    "「このうさぎさんは、笑うこともできるんです」﻿",
    "「どれだけ間が悪くとも、捕まえるまで絶対にあきらめません！」﻿",
    "「バリスタの力…！」﻿",
    "「ココアさんのバカー！」﻿",
    "「物理部好きです」"
]

# 認証情報の取得
TOKEN = os.getenv("DISCORD_TOKEN") 
intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

# -----------------
# イベントハンドラ
# -----------------
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

# -----------------
# Botの実行
# -----------------
if TOKEN:
    # 24時間稼働Webサーバーを別スレッドで起動
    Thread(target=keep_alive).start()
    # Botを起動
    client.run(TOKEN)
else:
    print("エラー: Botトークンが設定されていません。")
