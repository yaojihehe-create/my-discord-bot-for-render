import discord
import os
import random
from flask import Flask
from threading import Thread
from pathlib import Path # 新しくインポート

# Flaskのアプリケーションインスタンスを作成
app = Flask('')
# Botが起動したことを示すログファイルのパスを定義
BOT_FLAG_FILE = Path("bot_running.log") 

# Botのロジック部分
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
        
        # Botが正常に起動した時点でフラグファイルを作成
        # これがBotが「生きている」ことを示す共有フラグになります。
        try:
            with open(BOT_FLAG_FILE, 'w') as f:
                f.write("Bot is running.")
            print("Bot起動フラグファイルを作成しました。")
        except Exception as e:
            print(f"フラグファイル作成エラー: {e}")

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
    # 共有フラグファイルが存在するかどうかをチェック
    if not BOT_FLAG_FILE.exists():
        # フラグファイルがない（Botが起動していない）場合のみ起動
        thread = Thread(target=start_discord_bot)
        thread.start()
        return "Discord Bot is initializing (Checking flag file)..."
    
    # フラグファイルが存在する場合（Botが起動済み）は、すぐにWebサーバーの応答を返す
    return "Discord Bot is running (Flag file found)."
