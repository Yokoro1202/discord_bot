import discord
import os

#ffmpegに接続するためのpathを追加
os.environ["PATH"] += ":/Applications"
# 自分のBotのアクセストークンに置き換えてください
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
    '''
    #/joinでbotが自分のボイスチャンネルに接続
    if message.content == '/join':
        if message.author.voice is None:
            await message.channel.send("あなたはボイスチャンネルに接続していません")
            return
        await message.author.voice.channel.connect()
        await message.channel.send("接続しました")
    '''
    #/commandで使用できるコマンドを一覧
    if message.content == '/command':
        embed = discord.Embed(title='コマンド一覧', colour=0x00ff00)
        for k, v in command.items():
            embed.add_field(name=f'{k}', value=f'{v}', inline = False)
        await message.channel.send(embed=embed)

    #/listで出力できる音声を一覧
    elif message.content == '/list':
        embed = discord.Embed(title='再生可能リスト', colour=0x00ff00)
        fields_count = 0
        for f in files:
            embed.add_field(name=f'{f}', value='',inline = False)
            fields_count += 1
            if fields_count >= 25:
                await message.channel.send(embed=embed)
                embed = discord.Embed(title='続き', colour=0x00ff00)
                fields_count = 0
        if fields_count != 0:
            await message.channel.send(embed=embed)
    
    #/playでボイスチャンネルに接続、音楽を流す
    elif message.content.startswith('/play') == True:
        if message.author.voice is None:
            await message.channel.send('あなたはボイスチャンネルに接続していません')
            return
        #ボイスチャンネルにbotがいなければ、接続
        if message.guild.voice_client is None:
            await message.author.voice.channel.connect()
        #再生されているのに/playを入力した時の警告
        playing = message.guild.voice_client.is_playing()
        if playing is True:
            embed = discord.Embed(title='Error!',description='/stop, /pauseで音声を停止してから/playを入力してください', colour=0xff0000)
            await message.channel.send(embed=embed)
            return
        #音声ファイルが入力されていなければ知らせる
        if message.content.endswith('.m4a') == False:
            await message.channel.send('/listで出力された音声ファイルを入力してください。例:/play example.m4a')
            return
        #入力された音声ファイルを再生する.message.content[6:]は'/play 'の後の文字列(ファイル名)を取得
        correct_play = False
        for f in files:
            if f == message.content[6:]:
                message.guild.voice_client.play(discord.FFmpegOpusAudio(f'./music/{f}'))
                correct_play = True
        #入力された音声ファイルが無ければ知らせる
        if message.content.endswith('.m4a') == True and correct_play == False:
            await message.channel.send('入力された音声ファイルは存在しません。/listから得られる正しい音声ファイルを入力してください')
    
    #/stopで再生している音楽を停止
    elif message.content == '/stop':
        playing = message.guild.voice_client.is_playing()
        if playing is True:
            message.guild.voice_client.stop()
            await message.channel.send(f'停止しました')
            return

    #/pauseで再生している音楽を一時停止
    elif message.content == '/pause':
        playing = message.guild.voice_client.is_playing()
        if playing is True:
            message.guild.voice_client.pause()
            await message.channel.send(f'一時停止しました')
            return

    #/resumeで一時停止した音楽を再生
    elif message.content == '/resume':
        playing = playing = message.guild.voice_client.is_playing()
        if playing is False:
            message.guild.voice_client.resume()
            return

    #/leaveでボイスチャンネルから切断
    elif message.content == '/leave':
        if message.guild.voice_client is None:
            await message.channel.send("Botはボイスチャンネルに接続していません")
            return

        playing = message.guild.voice_client.is_playing()
        #音声を停止してから切断
        if playing is True:
            message.guild.voice_client.stop()

        await message.guild.voice_client.disconnect()
        await message.channel.send("切断しました")

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
