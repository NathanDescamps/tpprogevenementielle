import socket
import psutil
import os

def serveur():
    msg = ""
    conn = None
    server_socket = None
    while msg != "fin" :
        msg = ""
        server_socket = socket.socket()
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", 10015))

        server_socket.listen(1)
        print('Serveur en attente de connexion')
        while msg != "fin" and msg != "retour":
            msg = ""
            try :
                conn, addr = server_socket.accept()
                print (addr)
            except ConnectionError:
                print ("erreur de connection")
                break
            else :
                while msg != "fin" and msg != "retour" and msg != "deconnexion":
                    msg = conn.recv(1024).decode()
                    print ("Received from client: ", msg)
                    if msg == "infcpu":
                        nombrecpu = os.cpu_count()
                        cpupourcentage = psutil.cpu_percent()
                        cpustatistiques = psutil.cpu_stats()
                        msg = (f'Il y a {nombrecpu}, utilisé pour {cpupourcentage}, et les stats sont {cpustatistiques}')
                    elif msg == "infexploitation":
                        systemexploit = os.name
                        msg = (f'Le système utilisé est {systemexploit}')
                    elif msg == "infaddresseip":
                        msg = (f"laddresse ip de cette machine est {socket.gethostbyname(socket.gethostname())}")
                    elif msg == "infram":
                        pid = os.getpid()
                        python_process = psutil.Process(pid)
                        memoryUse = python_process.memory_info()[0]/2.**30
                        mmoirevirtu2 = (psutil.virtual_memory()[3]/2.**30)
                        msg = (f"la RAM utilisé vaut : {memoryUse} GB et la ram totale vaut : {mmoirevirtu2} GB.")
                    elif msg == "infnommachine":
                        nommachine = socket.gethostname()
                        msg = (f"Le nom de cette machine est : {nommachine}")
                    conn.send(msg.encode())
            conn.close()
        print ("Connexion avec le client terminé !")
        server_socket.close()
        print ("Serveur s'est éteint avec succès !")

if __name__ == '__main__':
    serveur()