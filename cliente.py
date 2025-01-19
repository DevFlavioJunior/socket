import threading
from socket import *
import datetime

def main():
    try:
        server_ip = "127.0.0.1"
        server_port = 12000
        client = socket(AF_INET, SOCK_DGRAM)
        nickname = input("Digite seu nickname: ")
        client.sendto(f"{nickname} : Se juntou a nós {datahora()}".encode('utf-8'), (server_ip, server_port))

        
        threading.Thread(target=receiveMessages, args=(client,), daemon=True).start()

        sendMessages(client, nickname, server_ip, server_port)

    except Exception as e:
        print(f"Erro ao criar socket: {e}")
        return

def sendMessages(client, nickname, server_ip, server_port):
    while True:
        try:
            message = input("Digite sua mensagem (ou 'exit' para sair): ").strip().lower()
            if message == "exit":
                client.sendto(f"{nickname} : Saiu {datahora()}".encode('utf-8'), (server_ip, server_port))
                print("Você saiu do chat.")
                break
            client.sendto(f"{nickname} : {message} {datahora()}".encode('utf-8'), (server_ip, server_port))

        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            break

    client.close() 

def receiveMessages(client):
    while True:
        try:
            message, _ = client.recvfrom(2048)
            print(f"\n{message.decode('utf-8')}")
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
            break

def datahora():
    data = datetime.datetime.now()
    return data.strftime("%H:%M:%S %d/%m/%Y")

if __name__ == "__main__":
    main()
