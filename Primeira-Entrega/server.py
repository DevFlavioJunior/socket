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

mensagens_pendentes = {}

def tratamento_de_mensagem(data, address):
    """Processa a mensagem recebida de um cliente."""
    try:
        if address not in clients:
            # Novo cliente conectando
            username = data.decode().split("eh ")[1].strip()
            clients[address] = username
            print(f"{username} entrou na sala.")
            server.sendto(f"Bem-vindo {username}!".encode(), address)
            broadcast_message(f"{username} entrou na sala.".encode(), address)
        else:
            message = data.decode()

            if message == 'EOF':
                # Quando receber 'EOF', junta os fragmentos e envia para todos
                full_message = ''.join(mensagens_pendentes.get(address, []))
                mensagens_pendentes[address] = []  # Limpa os fragmentos armazenados
                
                username = clients[address]
                formatted_message = f"{address[0]}:{address[1]}/~{username}: {full_message} {datahora()}"
                broadcast_message(formatted_message.encode(), address)
            else:
                # Adiciona fragmento à lista de mensagens pendentes do cliente
                mensagens_pendentes.setdefault(address, []).append(message)

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