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
                # Espera por mensagens de clientes
                message, client_address = server.recvfrom(1024)
                print(f"{client_address[0]+':'+ str(client_address[1])}: {message.decode('utf-8')}")
                
                # Adiciona cliente à lista, se não estiver presente
                if client_address not in clients:
                    clients.append(client_address)

                # Envia a mensagem para todos os outros clientes
                for client in clients:
                    if client != client_address:
                        try:
                            server.sendto(message, client)
                        except Exception as e:
                            print(f"Erro ao enviar para {client}: {e}")
                            deleteclient(client, server)  # Chama a função para remover o cliente
                            
            except Exception as e:
                print(f"Erro ao receber mensagem: {e}")

    except KeyboardInterrupt:
        print("\nServidor interrompido manualmente.")
    finally:
        server.close()
        print("Servidor fechado.")

def deleteclient(client, server):
    if client in clients:
        clients.remove(client)
        print(f"Cliente {client} desconectado.")
    else:
        print(f"Cliente {client} não encontrado.")

if __name__ == "__main__":
    main()
