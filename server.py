import socket
import threading
import json  # json.dumps(some)打包   json.loads(some)解包
import os
import os.path
import sys
import random
from time import sleep


#IP = '172.23.176.80'
IP = '127.0.0.1'
PORT = 5555     # 端口
users = []   # 0:userName 1:status

guess_owner = [None, None]
guess_status = None

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
        global guess_owner,guess_status
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
                            message = []
                            owner_alive = False
                            for i in users:
                                if i[1] == 'guess_join':
                                    message.append(i[0])
                                    if i[0] == guess_owner[1]:
                                        owner_alive = True
                            if not owner_alive:                         
                                temp = random.randint(0, len(message))
                                guess_owner = [temp, message[0]]
                            message.pop(guess_owner[0])
                            message = ['[房主]'+guess_owner[1]]+message
                            print('guess',message)
                            msg = {'event':'return_guess_players','args':message}
                            msg = json.dumps(msg).encode('utf-8')
                            conn.send(msg)
                        case 'guess_start':
                            guess_status = 1
                            msg = {'event':'guess_start','args':[None]}
                            msg = json.dumps(msg).encode('utf-8')
                            conn.send(msg)
                            pass
                        case 'guess_status_update':
                            pass
                                
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

