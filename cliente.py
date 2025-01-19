import threading
from socket import*
import datetime

def main():
    try:

        server_ip = "127.0.0.1"
        server_port = 12000
        client = socket(AF_INET, SOCK_DGRAM)
        nickname = input("Digite seu nickname: ")
        client.sendto(f"{nickname} : Se juntou a nós {datahora()}".encode('utf-8'), (server_ip, server_port))
        sendMessages(client,nickname,server_ip, server_port)

    except Exception as e:
        print(f"Erro ao criar socket: {e}")
        return
    
def sendMessages(client,nickname,server_ip, server_port):
    while True:
        try:
            message = input("Digite sua mensagem: exit para sair").lower()
            if message == "bye":
                client.sendto(f"{nickname} : Saiu {datahora()}".encode('utf-8'), (server_ip, server_port))
                break
            client.sendto(message.encode(), (server_ip, server_port))

        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            break


def datahora():
    data = datetime.datetime.now()
    return data.strftime("%H:%M:%S %d/%m/%Y")

if __name__ == "__main__":
    main()            
  