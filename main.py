import discord
import os
import random
from flask import Flask

# Flaskのアプリケーションインスタンスを作成（Webサーバー機能）
# RenderのWebサービスとして起動するために必要
app = Flask(__name__)

# -----------------
# Webサーバー機能（Renderの生存確認用）
# -----------------
# RenderがBotが生きているか確認するアクセスに応答します
@app.route('/')
def home():
    return "Discord Bot is running and the web server is alive."


# -----------------
# Discord Bot本体の起動関数
# -----------------
def run_discord_bot():
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
    
    # Botトークンが設定されている場合のみ実行
    if TOKEN:
        # Botを起動
        client.run(TOKEN)
    else:
        print("エラー: Botトークンが設定されていません。環境変数 DISCORD_TOKEN を設定してください。")


# -----------------
# メイン実行ブロック
# -----------------
# このファイルが「Bot本体」として直接実行された場合にBotを起動
if __name__ == '__main__':
    run_discord_bot()
# gunicornがこのファイルをWebサーバーとして実行する場合、appインスタンスが使用されます。
