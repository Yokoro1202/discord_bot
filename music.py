import discord
import os

#ffmpegに接続するためのpathを追加
os.environ["PATH"] += ":/Applications"
# 自分のBotのアクセストークンに置き換える
TOKEN = '******'

#ローカルに存在する音声ファイルを格納
files = list()

#ローカルに存在する音声ファイルを取得
#音声ファイルは'.m4a'にのみ対応
file_list = os.listdir("music")
for f in file_list:
    if(f.endswith('.m4a')):
        files.append(f)
files.sort()
    
#動作するコマンドを格納
command = {}
command['/command'] = '使用できるコマンドを出力します'
command['/list'] = '再生可能なファイルを出力します'
command['/play example.m4a'] = '指定したファイルの音声を出力します'
command['/stop'] = '再生している音声を停止します'
command['/pause'] = '再生している音声を一時停止します'
command['/resume'] = '一時停止している音声を再生します'
command['/leave'] = 'Botを切断できます'


intents = discord.Intents.default()
intents.message_content = True

# 接続に必要なオブジェクトを生成
client = discord.Client(intents=intents)

#botが動作する関数を定義.
#

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
