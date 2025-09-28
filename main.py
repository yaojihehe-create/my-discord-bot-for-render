import discord
import os
import random
from flask import Flask
from threading import Thread
import requests  # 新しくインポート: Webサーバーを停止させるために使用

# Flaskのアプリケーションインスタンスを作成
app = Flask(__name__)

# Botの起動が完了したかどうかを示すフラグ
bot_started_flag = False

# -----------------
# Webサーバーを起動してBotの24時間稼働を維持する関数
# -----------------
def run_web_server():
    # ポートが設定されていることを確認
    port = int(os.environ.get('PORT', 8080))
    
    # Webサーバーの生存確認エンドポイント
    @app.route('/')
    def home():
        return "Bot is alive and the web server is running."

    # Webサーバーを起動
    app.run(host='0.0.0.0', port=port)


# -----------------
# Bot本体の起動とWebサーバー停止処理
# -----------------
def start_discord_bot_and_stop_web():
    global bot_started_flag
    
    if bot_started_flag:
        return

    # Botのロジック（応答メッセージ）
    RANDOM_RESPONSES = [
        "呼んだ？何かお手伝いできることはありますか？😊",
        "はい、私でちょいと頼られました！",
        "どうしましたか？何か面白いことでもありましたか？",
        "あなたに話しかけられるのを待っていました！",
        "ランダム応答発動！何かご用でしょうか？"
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
        
        # Botが起動に成功したらフラグを立てる
        bot_started_flag = True

        # 注意: このWebサーバー停止処理はRender環境では保証されません
        # しかし、試す価値はあります

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


# -----------------
# メイン実行ブロック
# -----------------
# Bot本体を別スレッドで起動
Thread(target=start_discord_bot_and_stop_web).start()

# Webサーバーをメインスレッドで起動（Renderの要件を満たす）
# 注意：Flaskの run() はブロッキング関数であり、Bot起動後に実行する必要があります。

if __name__ == '__main__':
    # Botの起動が完了するのを少し待ってからWebサーバーを起動
    # これにより、Renderは「ポートが開いている」と認識しつつ、Botのプロセスをメインにします
    run_web_server()
