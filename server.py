from socket import*
from datetime import datetime

# Configurações do servidor
SERVER_IP = '127.0.0.1'  # IP do servidor
SERVER_PORT = 12345      # Porta do servidor
BUFFER_SIZE = 1024       # Tamanho máximo do pacote

# Dicionário para armazenar clientes conectados
clients = {}

# Cria o socket UDP
server = socket(AF_INET, SOCK_DGRAM)
server.bind((SERVER_IP, SERVER_PORT))

print(f"Servidor iniciado em {SERVER_IP}:{SERVER_PORT}")

def datahora():
    """Função para retornar a data e hora atual."""
    return datetime.now().strftime("%H:%M:%S %d/%m/%Y")

def broadcast_message(message, sender_address):
    """Envia a mensagem para todos os clientes conectados, exceto o remetente."""
    for client_address in clients:
        if client_address != sender_address:
            server.sendto(message, client_address)

def tratamento_de_mensagem(data, address):
    """Processa a mensagem recebida de um cliente (mensagens ou fragmentos de arquivo)."""
    try:
        if address not in clients:
            # Novo cliente se conectando
            username = data.decode().split("eh ")[1].strip()
            clients[address] = username
            print(f"{username} entrou na sala.")
            # Mensagem de boas-vindas para o novo cliente
            welcome_message = f"Bem-vindo {username}!"
            server.sendto(welcome_message.encode(), address)
            # Broadcast para os outros clientes
            broadcast_message(f"{username} entrou na sala.".encode(), address)
        else:
            # A mensagem é um fragmento de arquivo ou uma mensagem de texto
            message = data.decode()
            
            # Se a mensagem for 'EOF', significa que o arquivo foi completamente enviado
            if message == 'EOF':
                print(f"Arquivo completo recebido de {clients[address]}")
            elif message.strip().lower() == 'bye':
                # Cliente saindo
                username = clients[address]
                print(f"{username} saiu da sala.")
                del clients[address]
                # Broadcast para os outros clientes
                broadcast_message(f"{username} saiu da sala.".encode(), address)
            else:
                username = clients[address]
                formatted_message = f"{address[0]}:{address[1]}/~{username}: {message} {datahora()}"
                #print(formatted_message)
                # Broadcast da mensagem para todos os outros clientes
                broadcast_message(formatted_message.encode(), address)
    except Exception as e:
        print(f"Erro ao processar a mensagem de {address}: {e}")

while True:
    try:
        # Recebe dados do cliente
        data, address = server.recvfrom(BUFFER_SIZE)
        tratamento_de_mensagem(data, address)
    except Exception as e:
        print(f"Erro: {e}")
        break

server.close()
