from PyQt5.QtWidgets import *
import socket, threading,sys

########################################################################################################################
#Client

class Client(threading.Thread):

    def __init__(self, host, port):
        super().__init__()
        self.__host = host
        self.__port = port
        self.__sock = socket.socket()
    def __connect(self) -> int:
        try :
            self.__sock.connect((self.__host,self.__port))
        except ConnectionRefusedError:
            print ("serveur non lancé ou mauvaise information")
            return -1
        except ConnectionError:
            print ("erreur de connection")
            return -1
        else :
            print ("connexion réalisée")
            return 0

    def __dialogue(self):
        msg = ""
        while msg != "kill" and msg != "disconnect" and msg != "reset":
            msg = input("client: ")
            self.__sock.send(msg.encode())
            msg = self.__sock.recv(1024).decode()
            print(msg)
        self.__sock.close()

    def send_and_receive(self, msg):
        self.__sock.send(msg.encode())
        resultat = self.__sock.recv(1024).decode()
        return resultat

    def run(self):
        if (self.__connect() ==0):
            self.__dialogue()

########################################################################################################################
#GUI

class SAEinterface(QMainWindow):
    def __init__(self):
        super().__init__()

        widget = QWidget()
        grid = QGridLayout()

        self.setCentralWidget(widget)
        widget.setLayout(grid)

        connexion = QPushButton("Connexion")
        connexion.clicked.connect(self.on_se_connecte)
        deconnexion = QPushButton("Déconnexion")
        #deconnexion.clicked.connect(self.on_se_deconnecte)
        ping_serveur_via_client = QPushButton("Ping du serveur")
        #ping_serveur_via_client .clicked.connect(self.on_ping_serveur)
        sendcommand = QPushButton("envoyer la commande au serveur ")
        sendcommand.clicked.connect(self.on_send_command)
        self.__lescommandes = QComboBox()
        self.__lescommandes.addItems(['infcpu', 'infram', 'infexploitation', 'infaddresseip','infnommachine'])
        self.__port = QLabel("Port(fixe) :")
        self.__port1 = QLineEdit("10015")
        self.__ip = QLabel("Adresse IP :")
        self.__lesipenliste = QComboBox()
        self.__choisirfichiertxt = QPushButton('choisir un fichier avec vos IP')
        self.__choisirfichiertxt.clicked.connect(self.search_and_add_text_file)
        self.resultcommand = QTextEdit()
        self.setWindowTitle("serv.io")


        grid.addWidget(connexion, 3, 0, 1, 1)
        grid.addWidget(deconnexion,3 , 1, 1 ,2)
        grid.addWidget(ping_serveur_via_client, 7, 0, 1,3)
        grid.addWidget(sendcommand, 5, 0, 1, 3)
        grid.addWidget(self.__lescommandes, 4, 0, 1, 3)
        grid.addWidget(self.__port, 2 ,0 )
        grid.addWidget(self.__port1, 2 ,1, 1, 2 )
        grid.addWidget(self.__ip, 1 ,0 )
        grid.addWidget(self.__lesipenliste, 1, 1, 1, 2)
        grid.addWidget(self.__choisirfichiertxt, 0, 0, 1,3 )
        grid.addWidget(self.resultcommand, 8, 0, 1, 3)

    def search_and_add_text_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier texte", "", "Fichiers texte (*.txt)")
        if file_name:
            if file_name.endswith('.txt'):
                with open(file_name, 'r') as f:
                    lines = f.readlines()
                    ips = []
                    for line in lines:
                        ips += line.split()
                    self.__lesipenliste.addItems(ips)

    def on_se_connecte(self):
        ip = self.__lesipenliste.currentText()
        port = int(self.__port1.text())
        self.client = Client(ip, port)
        self.client.start()

    def on_send_command(self):
        command = self.__lescommandes.currentText()
        self.resultcommand.append(command)
        self.client.send_and_receive(command)
        self.resultcommand.append(self.client.send_and_receive(command))

                    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SAEinterface()
    window.show()
    app.exec()