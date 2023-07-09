import sys
import json
import socket
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread
import login
import mainwindow
import guess
from time import sleep


class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.IP = "121.43.55.56"
        self.PORT = 5555
        self.client_socket.connect((self.IP, self.PORT))

    def send_data(self, msg):
        msg = json.dumps(msg).encode('utf-8')
        self.client_socket.send(msg)

    def get_data(self):
        msg = None
        while not msg:
            msg = self.client_socket.recv(1024).decode('utf-8')
            if msg:
                msg = json.loads(msg)
                match msg['event']:
                    case 'return_guess_players':
                        return msg['args']
                    case 'guess_start':
                        guess_form.thread_su.start()
                        return None

                print(msg)


class Login_Form(QtWidgets.QWidget, login.Ui_Form):
    def __init__(self):
        super(Login_Form, self).__init__()
        self.setupUi(self)

    def LoginButton_Clicked(self):
        global Username
        # self.textEdit.setText("?")
        self.close()
        Username = self.textEdit.toPlainText()
        client.send_data({'event': 'login', 'args': [Username]})
        mainwindow_form.show()


class MainWindow_Form(QtWidgets.QWidget, mainwindow.Ui_Form):
    def __init__(self):
        super(MainWindow_Form, self).__init__()
        self.setupUi(self)

    def Guess_Clicked(self):
        global Username
        client.send_data({'event': 'guess_join', 'args': [Username]})
        guess_form.show()
        guess_form.players_update_start()
        self.close()


class Guess_Form(QtWidgets.QWidget, guess.Ui_Form):
    def __init__(self):
        super(Guess_Form, self).__init__()
        self.setupUi(self)
        self.thread_pu = Guess_Pu()
        self.thread_su = Guess_Su()

    def players_update_start(self):
        self.thread_pu.start()

    def status_update_start(self):
        self.thread_su.start()

    def send_msg(self):
        pass

    def guess_start(self):
        global guess_status
        client.send_data({'event': 'guess_start', 'args': [None]})
        guess_status = True
        guess_form.button_start.close()


class Guess_Pu(QThread):  # players_update线程
    def __init__(self):
        super(Guess_Pu, self).__init__()

    def run(self):
        global Username,guess_status
        while True:
            client.send_data({'event': 'guess_players_update', 'args': [None]})
            msg = client.get_data()
            if msg:
                if Username == msg[0][4:] and not guess_status:
                    guess_form.button_start.show()
                else:
                    guess_form.button_start.close()
                msg = '当前在线玩家:\n'+'\n'.join(msg)
                guess_form.players.setText(msg)
            self.sleep(1)

class Guess_Su(QThread):  # players_update线程
    def __init__(self):
        super(Guess_Su, self).__init__()

    def run(self):
        global Username,guess_status
        while True:
            client.send_data({'event': 'guess_status_update', 'args': [None]})
            msg = client.get_data()
            print(12121)
            guess_form.status.setText(str(msg))
            if True and not guess_status:
                pass
            else:
                pass
            print(250)
            sleep(0.2)


if __name__ == '__main__':
    global guess_status
    app = QtWidgets.QApplication(sys.argv)
    Username = 'Steve'
    guess_status = False

    login_form = Login_Form()
    mainwindow_form = MainWindow_Form()
    guess_form = Guess_Form()
    login_form.show()
    # form_process = multiprocessing.Process(target=form)
    # form_process.start()
    # form_process.join()

    client = Client()

    sys.exit(app.exec_())
