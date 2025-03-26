import socket
import threading

# Configurações do cliente
SERVER_IP = '127.0.0.1'  # IP do servidor
SERVER_PORT = 12345      # Porta do servidor
BUFFER_SIZE = 1024       # Tamanho máximo do pacote

# Cria o socket UDP
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def receber_mensagens():
    # Função para receber mensagens e arquivos fragmentados do servidor.
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
            mensagem = input()
            
            if mensagem.strip().lower() == 'bye':
                client.sendto(b'bye', (SERVER_IP, SERVER_PORT))
                print("Saindo do chat...")
                client.close()
                break

            # Fragmenta mensagens longas manualmente
            for i in range(0, len(mensagem), BUFFER_SIZE):
                fragment = mensagem[i:i + BUFFER_SIZE]
                client.sendto(fragment.encode(), (SERVER_IP, SERVER_PORT))

            # Envia um delimitador indicando fim da mensagem completa
            client.sendto(b'EOF', (SERVER_IP, SERVER_PORT))

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