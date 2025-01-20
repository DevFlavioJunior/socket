import socket

clients = []

def main():
    try:
        server_port = 12000
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(('', server_port))
        print("Servidor pronto para receber mensagens")
    except Exception as e:
        print(f"Erro ao criar socket: {e}")
        return
    
    try:
        while True:
            try:
                
                message, client_address = server.recvfrom(1024)
                if message:
                  arquivo = ler_arquivo()
                  server.sendto(arquivo.encode('utf-8'), client_address)
               
                if client_address not in clients:
                    clients.append(client_address)

                for client in clients:
                    if client != client_address:
                        try:
                          server.sendto(arquivo.encode('utf-8'), client_address)
                        except Exception as e:
                            print(f"Erro ao enviar para {client}: {e}")
                            deleteclient(client, server)  
                            
            except:
                continue  
    except KeyboardInterrupt:
        print("\nServidor interrompido manualmente.")
    finally:
        server.close()
        print("\nServidor fechado.")

def deleteclient(client, server):
    if client in clients:
        clients.remove(client)
        print(f"Cliente {client} desconectado.")
    else:
        print(f"Cliente {client} não encontrado.")

def ler_arquivo():
    with open("chat.txt", "rb") as arquivo:
        return arquivo.read().decode('utf-8')
if __name__ == "__main__":
    main()
