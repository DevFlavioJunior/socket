import socket
import threading


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
            
            # Exibe a mensagem de boas-vindas ou qualquer outra
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

        except Exception as e:
            print(f"Erro ao receber a mensagem: {e}")
            break

def enviar_mensagem():
    """Função para enviar mensagens, possivelmente fragmentadas."""
    while True:
        try:
            # Solicita a mensagem ao usuário
            mensagem = input()

            # Se o usuário digitar 'bye', envia a mensagem de desconexão
            if mensagem.strip().lower() == 'bye':
                client.sendto(b'bye', (SERVER_IP, SERVER_PORT))
                print("Saindo do chat...")
                client.close()
                break

            # Cria o arquivo .txt com a mensagem
            filename = 'message.txt'
            with open(filename, 'w') as file:
                file.write(mensagem)

            # Fragmenta o arquivo e envia para o servidor
            with open(filename, 'r') as file:
                while True:
                    fragment = file.read(BUFFER_SIZE)
                    if not fragment:
                        break
                    client.sendto(fragment.encode(), (SERVER_IP, SERVER_PORT))

            # Envia o delimitador EOF
            client.sendto(b'EOF', (SERVER_IP, SERVER_PORT))

        except Exception as e:
            print(f"Erro ao enviar a mensagem: {e}")
            break

# Função para conectar ao servidor
def conectar():
    try:
        print("Conectando ao servidor...")

        # Tentativas para obter um nickname válido
        for i in range(5, 0, -1):  # Contagem regressiva das tentativas
            print("Comando para se conectar: hi, meu nome eh 'SEU_NOME'")
            nickname = input("Digite o comando corretamente: ").strip()

            if nickname.startswith("hi, meu nome eh"):
                nickname = nickname.split("eh")[1].strip()
                break  # Sai do loop ao obter um nome válido
            else:
                print(f"Comando incorreto! Você tem mais {i-1} tentativas.")

        else:
            print("Número máximo de tentativas excedido! Encerrando conexão.")
            return

        # Envia o nome de usuário para o servidor
        client.sendto(f"hi, meu nome eh {nickname}".encode(), (SERVER_IP, SERVER_PORT))
        print(f"Usuário {nickname} conectado ao servidor.")

        # Inicia a thread para receber mensagens
        receber_thread = threading.Thread(target=receber_mensagens, daemon=True)
        receber_thread.start()

        # Inicia o envio de mensagens
        enviar_mensagem()

    except Exception as e:
        print(f"Erro ao conectar ao servidor: {e}")

# Chama a função de conectar
if __name__ == '__main__':
    conectar()
