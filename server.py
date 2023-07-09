import socket
import threading
import json  # json.dumps(some)打包   json.loads(some)解包
import os
import os.path
import sys
import random
from time import sleep


IP = '172.23.176.80'
PORT = 5555     # 端口
users = []   # 0:userName 1:status
guess_owner = None
lock = threading.Lock()

def onlines():    # 统计当前在线人员
    online = []
    for i in range(len(users)):
        online.append(users[i][0])
    return online

class ChatServer(threading.Thread):
    global users, que, lock

    def __init__(self):         # 构造函数
        threading.Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.s.bind(IP,PORT)
        # self.s.listen(32)
        os.chdir(sys.path[0])
# 接受来自客户端的用户名，如果用户名为空，使用用户的IP与端口作为用户名。如果用户名出现重复，则在出现的用户名依此加上后缀“2”、“3”、“4”……
    def receive(self, conn, addr):             # 接收消息
        # user = conn.recv(1024)        # 用户名称
        # user = user.decode()
        # if user == '用户名不存在':
        #     user = addr[0] + ':' + str(addr[1])
        # tag = 1
        # temp = user
        # for i in range(len(users)):     # 检验重名，则在重名用户后加数字
        #     if users[i][0] == user:
        #         tag = tag + 1
        #         user = temp + str(tag)
        # users.append((user, conn))
        # USERS = onlines()
        # # 在获取用户名后便会不断地接受用户端发来的消息（即聊天内容），结束后关闭连接。
        user = None
        try:
            while True:
                msg = json.loads(conn.recv(1024).decode('utf-8'))
                print(msg)
                if msg['event'] == 'login':
                    user = msg['args'][0]
                    users.append([user, 'login'])
                else:
                    j = 0
                    for i in users: #获取用户存储位置
                        if user == i[0]:
                            break
                        j += 1 
                    match msg['event']:
                        case 'guess_join':
                            users[j][1] = 'guess_join'
                        case 'guess_players_update':
                            print('shit')
                            message = []
                            for i in users:
                                if i[1] == 'guess_join':
                                    u = i[0]
                                    message.append(u)
                            if guess_owner not in message:                              
                                guess_owner = random.randint(0, len(message))
                            print(guess_owner)
                            message = ['[房主]'+message[guess_owner]]+message[0:guess_owner]+message[guess_owner:]
                            print(message)
                            msg = {'event':'return_guess_players','args':[message]}
                            print(msg)
                            msg = json.dumps(msg).encode('utf-8')
                            print(msg)
                            conn.send(msg)
                                
                print(users)

               
            conn.close()
        # 如果用户断开连接，将该用户从用户列表中删除，然后更新用户列表。
        except:   
            j = 0
            for i in users:
                if user == i[0]:
                    users.pop(j)
                    break
                j+=1
                #pass
        conn.close()
  

    # 服务端在接受到数据后，会对其进行一些处理然后发送给客户端，如下图，对于聊天内容，服务端直接发送给客户端，而对于用户列表，便由json.dumps处理后发送。
    def sendData(self): # 发送数据
        pass

    def run(self):
        self.s.bind((IP,PORT))
        self.s.listen(16)
        q = threading.Thread(target=self.sendData)
        q.start()
        while True:
            conn, addr = self.s.accept()
            t = threading.Thread(target=self.receive, args=(conn, addr))
            t.start()
        self.s.close()
if __name__ == '__main__':
    cserver = ChatServer()
cserver.start()

