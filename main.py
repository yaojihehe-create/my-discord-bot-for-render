import discord
import os
import random

# Flask と Thread のインポートは削除

# ランダムに選択する応答メッセージリスト
RANDOM_RESPONSES = [
    "「このうさぎさんは、笑うこともできるんです」﻿",
    "「どれだけ間が悪くとも、捕まえるまで絶対にあきらめません！」﻿",
    "「バリスタの力…！」﻿",
    "「ココアさんのバカー！」﻿",
    "「物理部好きです」"
]

# 認証情報の取得（環境変数から読み込む）
TOKEN = os.getenv("DISCORD_TOKEN") 

# Botの設定（必要なインテントを設定）
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

    # メンションに反応する処理
    if client.user.mentioned_in(message):
        response = random.choice(RANDOM_RESPONSES)
        await message.channel.send(f'{message.author.mention} {response}')
        return 

# -----------------
# Botの実行
# -----------------

if TOKEN:
    # 24時間稼働用の keep_alive() の呼び出しは削除
    client.run(TOKEN)
else:
    print("エラー: Botトークンが設定されていません。環境変数 DISCORD_TOKEN を設定してください。")
