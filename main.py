import discord
import os
import random
from flask import Flask
from threading import Thread

# Webサーバーを起動してBotの24時間稼働を維持する関数
def keep_alive():
    app = Flask('')
    @app.route('/')
    def home():
        return "Bot is alive!"  # Botが生きていることを確認するメッセージ
    def run():
        # Renderの環境変数を使い、0.0.0.0と環境変数PORTでWebサーバーを起動
        app.run(host='0.0.0.0', port=os.environ.get('PORT', 8080))
    t = Thread(target=run)
    t.start()

# ランダムに選択する応答メッセージリスト
RANDOM_RESPONSES = [
    "「このうさぎさんは、笑うこともできるんです」﻿",
    "「どれだけ間が悪くとも、捕まえるまで絶対にあきらめません！」﻿",
    "「バリスタの力…！」﻿",
    "「ココアさんのバカー！」﻿",
    "「物理部好きです」"
]

# 認証情報の取得（環境変数から読み込む）
# RenderではReplitと同じくSecretsから読み込まれます。
TOKEN = os.getenv("DISCORD_TOKEN") 

# Botの設定（必要なインテントを設定）
intents = discord.Intents.default()
intents.message_content = True 

client = discord.Client(intents=intents)

# -----------------
# イベントハンドラ
# -----------------

# Botが起動し、Discordに接続したときに実行される
@client.event
async def on_ready():
    print('---------------------------------')
    print(f'Botがログインしました: {client.user.name}')
    print('---------------------------------')

# メッセージを受信したときに実行される
@client.event
async def on_message(message):
    # 自分のメッセージには反応しない
    if message.author == client.user:
        return

    # メンションに反応する処理
    if client.user.mentioned_in(message):
        response = random.choice(RANDOM_RESPONSES)
        await message.channel.send(f'{message.author.mention} {response}')
        return 

# -----------------
# Botの実行
# -----------------

# Botトークンが設定されている場合のみ実行
if TOKEN:
    # 24時間稼働Webサーバーを別スレッドで起動
    keep_alive() 
    # Botを起動
    client.run(TOKEN)
else:
    print("エラー: Botトークンが設定されていません。環境変数 DISCORD_TOKEN を設定してください。")
