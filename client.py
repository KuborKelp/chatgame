from socket import *

def send_data(msg):
    global tcp_socket
    tcp_socket = socket(AF_INET, SOCK_STREAM)
    server_ip = "121.43.55.56"
    server_port = 5555
    tcp_socket.connect((server_ip, server_port))
    send_data({'event': 'login', 'args': [username]})
    tcp_socket.send("send_data".encode("gbk"))
    #tcp_socket.send(msg)
    from_server_msg = tcp_socket.recv(1024)
    print(from_server_msg.decode("gbk"))
    tcp_socket.close()
