import discord
import os
import random
from flask import Flask
from threading import Thread
import time
import multiprocessing # 【重要】マルチプロセス制御のためにインポート

# Flaskのアプリケーションインスタンスを作成
app = Flask(__name__) 

# 【重要】Botの起動状態を追跡するためのグローバル変数（各プロセスで独立）
bot_start_attempted = False

# -----------------
# Discord Bot本体の起動関数
# -----------------
def run_discord_bot():
    # 応答メッセージリスト (長文を含むため、Pythonの複数行文字列で記述)
    RANDOM_RESPONSES = [
    "「このうさぎさんは、笑うこともできるんです」",
    "「どれだけ間が悪くとも、捕まえるまで絶対にあきらめません！」",
    "「バリスタの力…！」",
    "「ココアさんのバカー！」",
    "「物理部好きです」",
    "「お姉ちゃんはいりません」",
    "「私、口下手なので...。急にどうでもいい話とかできませんし...」",
    "「おじいちゃん、コーヒーの匂いが好きです。緑茶やハーブティーの匂いも素敵ですけど…また一つ、安らぐ匂いが見つかったみたいです」",
    # 応答リストの最後の要素が前の要素と結合されないように、カンマを追加し、記述を修正
    "「私、今、笑ってる写真はいりません。私にとってココアさんは、子を崖から突き落とすライオン。這い上がってきた時だけ、笑った写真を撮らせてあげます。たぶん」"
    ]

    TOKEN = os.getenv("DISCORD_TOKEN") 
    intents = discord.Intents.default()
    intents.message_content = True 
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        # 【デバッグ用】ログにプロセスIDを出力し、Botが1つしか起動していないか確認
        print(f'Bot PID: {os.getpid()} - Botがログインしました: {client.user.name}') 

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
            
        # メンションされた場合のみ応答
        if client.user.mentioned_in(message):
            response = random.choice(RANDOM_RESPONSES)
            await message.channel.send(f'{message.author.mention} {response}')
            return 

    if TOKEN:
        try:
            # Botを実行
            client.run(TOKEN)
        except Exception as e:
            print(f"Discord Bot 起動失敗 (PID: {os.getpid()}): {e}")
    else:
        print("エラー: Botトークンが設定されていません。")

# -----------------
# Webサーバーのエンドポイント (gunicornがアクセスする場所)
# -----------------
@app.route('/')
def home():
    global bot_start_attempted
    
    # ---------------------------------------------------------------------------------
    # 【最重要の修正点】プロセス名でチェックを行う
    # gunicornはワーカーをforkして起動するため、Botはメインワーカーでのみ起動を試みます。
    # ---------------------------------------------------------------------------------
    if not bot_start_attempted and multiprocessing.current_process().name == 'MainProcess':
        print(f"Webアクセスを検知 (PID: {os.getpid()})。Discord Botの起動を試みます...")
        
        # フラグを立てて、このワーカーでは再起動しないようにする
        bot_start_attempted = True
        
        # Botを別スレッドで起動
        Thread(target=run_discord_bot).start()
        
        # 初回起動時は応答が遅れるため、Initializingを返す
        return "Discord Bot is initializing... (Please check Discord in 10 seconds)"
        
    # Bot起動試行済みの場合は、Renderのヘルスチェックに応答
    return "Bot is alive!"
