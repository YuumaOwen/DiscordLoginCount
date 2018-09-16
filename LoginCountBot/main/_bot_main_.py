import discord
import datetime
from bot_module._module_ import discord_list as dl
from bot_module._module_ import discord_cmd as cmd
from bot_module._module_ import discord_log as log
from bot_module._module_ import discrd_count as count
from bot_module._utility_ import _utillity_ as ut

client = discord.Client()
#discordクライアントに接続

tl = ut().time_list()
#Bot起動時の日付取得

id_list = dl().login_menber()
today_id_list = dl().today_login_menber()
#今日ログインしたユーザーとデータがあるユーザーを参照

#list設定
@client.event
async def on_ready():
    print('|-----------|')
    print('|ログイン完了|')
    print('|-----------|')
@client.event
async def on_message(message):

    global id_list
    global today_id_list
    global tl

    n = datetime.datetime.now()
    nt = [n.month,n.day]
  
    sender = message.author
    user_id = str(sender.id)
    #変数初期設定
    if message.server != None:#DMに送った場合は無視する
        server_id = str(message.server.id)
        if tl[0] != nt[0] or tl[1] != nt[1]:#日付が変更された場合
            print(tl, nt)
            tl = ut().time_list()#日付更新
            today_id_list = []
            print("日付変更")
        if user_id + server_id in id_list:
            count().word_count(user_id, server_id, len(message.content))
            # 基本動作　文字数の加算
            if user_id + server_id not in today_id_list:#メッセージの送り主が今日すでにメッセージを送っているか判断
                
                count().login_count(user_id, server_id)
                today_id_list.append(user_id + server_id)
                

                log_ = "ユーザーログイン\t" + sender.name+str(n)+ "\n"
                print(log_,end="")
                log().tlogin_log(log_ )
                #logファイルに保存
        else:#データーベースにユーザーデータを登録する
            cmd().new_menber(sender.name, user_id, server_id, len(message.content))
            id_list.append(user_id + server_id)
            today_id_list.append(user_id + server_id)

            log_ = "ユーザー登録\t" + sender.name +str(n)+ "\n"
            print(log_,end="")
            log().user_log(log_)
            # logファイルに記録
        
        #command
        if message.content==".mc":

            log_ = ".mc\t"+sender.name+str(n)+"\n"
            print(log_,end="")
            log().cmd_log(log_)

            await client.send_message(message.channel, cmd().mc(user_id, server_id))
        elif message.content==".lc":

            log_ = ".lc\t"+sender.name+str(n)+"\n"
            print(log_,end="")
            log().cmd_log(log_)

            await client.send_message(message.channel,cmd().lc(user_id, server_id))
        elif message.content==".md":

            log_ = ".md\t"+sender.name+str(n)+"\n"
            print(log_,end="")
            log().cmd_log(log_)

            await client.send_message(message.channel, cmd().md(user_id, server_id))
        elif message.content==".help":
            log_ = ".help\t"+sender.name+str(n)+"\n"
            print(log_,end="")
            log().cmd_log(log_)
            await client.send_message(message.channel,cmd().help())

        
client.run("ここにbotのトークンを入れる")