import socket
import threading
import os

# Configurações do cliente
SERVER_IP = '127.0.0.1'  # IP do servidor
SERVER_PORT = 12345      # Porta do servidor
BUFFER_SIZE = 1024       # Tamanho máximo do pacote

# Cria o socket UDP
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def receber_mensagens():
    """Função para receber mensagens e arquivos fragmentados do servidor."""
    fragments = []  # Lista para armazenar fragmentos de arquivos

    while True:
        try:
            # Recebe a mensagem do servidor
            message, _ = client.recvfrom(BUFFER_SIZE)
            
            # Exibe a mensagem de boas-vindas
            print(f"Mensagem recebida: {message.decode()}")

            # Verifica se a mensagem contém a palavra "EOF" indicando fim do arquivo
            if message == b'EOF':
                print("Fim do arquivo recebido.")
                full_message = b''.join(fragments)
                print("Conteúdo do arquivo:")
                print(full_message.decode())  # Exibe o conteúdo do arquivo
                break

            # Caso contrário, armazena o fragmento
            fragments.append(message)
            # print(f"Fragmento recebido. {len(fragments)} fragmentos recebidos até agora...")

        except Exception as e:
            print(f"Erro ao receber a mensagem: {e}")
            break


def enviar_mensagem():
    while True:
        try:
            # Solicita uma mensagem do usuário
            mensagem = input()
            
            # Verifica se o usuário digitou 'bye' para sair
            if mensagem.strip().lower() == 'bye':
                client.sendto(b'bye', (SERVER_IP, SERVER_PORT))
                print("Saindo do chat...")
                client.close()
                break
            
            # Cria um arquivo temporário com a mensagem
            with open('mensagem.txt', 'w') as file:
                file.write(mensagem)
            
            # Fragmenta e envia o arquivo
            with open('mensagem.txt', 'rb') as file:
                while True:
                    fragment = file.read(BUFFER_SIZE)
                    if not fragment:
                        break
                    # Envia o fragmento
                    client.sendto(fragment, (SERVER_IP, SERVER_PORT))
            
            # Envia o 'EOF' após todos os fragmentos
            client.sendto(b'EOF', (SERVER_IP, SERVER_PORT))
            
            # Remove o arquivo temporário após o envio
            os.remove('mensagem.txt')
        
        except Exception as e:
            print(f"Erro ao enviar a mensagem: {e}")
            break

# Função para conectar ao servidor
def conectar():
    try:
        print("Conectando ao servidor...")

        # Solicita o nome de usuário
        nickname = input("Digite seu nome de usuário: ").strip()
        while not nickname:
            print("Nome de usuário não pode ser vazio. Tente novamente.")
            nickname = input("Digite seu nome de usuário: ").strip()

        # Envia o nome de usuário para o servidor
        client.sendto(f"hi, meu nome eh {nickname}".encode(), (SERVER_IP, SERVER_PORT))

        print(f"Usuário {nickname} conectado ao servidor.")

        # Inicia a thread para receber mensagens
        threading.Thread(target=receber_mensagens, daemon=True).start()
        
        # Inicia o envio de mensagens
        enviar_mensagem()

    except Exception as e:
        print(f"Erro ao conectar ao servidor: ==> {e}")

# Chama a função de conectar
if __name__ == '__main__':
    conectar()