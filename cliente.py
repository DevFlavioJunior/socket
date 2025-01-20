import threading
from socket import *
import datetime

def main():
    try:
        server_ip = "127.0.0.1"
        server_port = 12000
        client = socket(AF_INET, SOCK_DGRAM)
        nickname = input("Digite seu nickname: ")
        escrever_arquivo("Se juntou a nós",server_ip,server_port,nickname,client)
        print("Conectado ao chat.")


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
                escrever_arquivo("Saiu",server_ip,server_port,nickname,client)
                print("Você saiu do chat.")
                break
            client.sendto(f"{nickname} : {message} {datahora()}".encode('utf-8'), (server_ip, server_port))
            escrever_arquivo(message,server_ip,server_port,nickname,client)

        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            break

    client.close() 


def receiveMessages(client):
    while True:
        try:
           
            message, _ = client.recvfrom(1024)
            print(f"\n{message.decode('utf-8')}")
        except:
            print(f"Erro ao receber mensagem (conexão perdida)")
            break  
     

    client.close() 

def escrever_arquivo(mensagem,server_ip,server_port,nickname,client):
    with open("chat.txt", "wb") as arquivo:
        arquivo.write(f"{nickname} : {mensagem} {datahora()}\n".encode('utf-8'))
        client.sendto("True".encode(), (server_ip, server_port))

def datahora():
    data = datetime.datetime.now()
    return data.strftime("%H:%M:%S %d/%m/%Y")

if __name__ == "__main__":
    main()
