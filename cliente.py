import threading
from socket import*

def main():
    try:

        server_ip = "127.0.0.1"
        server_port = 12000
        client = socket(AF_INET, SOCK_DGRAM)
        nickname = input("Digite seu nickname: ")
        client.sendto(f"<{nickname}>Se juntou a nós".encode('utf-8'), (server_ip, server_port))
        sendMessages(client, server_ip, server_port)

    except Exception as e:
        print(f"Erro ao criar socket: {e}")
        return
    
def sendMessages(client, server_ip, server_port):
    while True:
        try:
            message = input("Digite a mensagem: ")
            client.sendto(message.encode(), (server_ip, server_port))

        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            break

if __name__ == "__main__":
    main()            
  