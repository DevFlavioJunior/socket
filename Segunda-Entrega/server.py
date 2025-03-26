import os
import socket
import threading
from math import ceil
import random
import string
import hashlib

# Função para calcular o checksum de uma string
def calcular_checksum(dados):
    return hashlib.md5(dados.encode('utf-8')).hexdigest()

# Função para gerar uma string aleatória de 5 letras minúsculas
def string_aleatoria_minuscula():
    letras = string.ascii_lowercase
    return ''.join(random.choice(letras) for _ in range(5))

# Classe que implementa o servidor
class Servidor:
    # Configurações do servidor
    SERVER_IP = "127.0.0.1"  # IP do servidor
    SERVER_PORT = 12345  # Porta do servidor
    BUFFER_SIZE = 1024  # Tamanho máximo do pacote
    ACK_TIMEOUT = 0.1  # Tempo limite para receber um ACK

    def __init__(self):
        # Inicializa o socket UDP e outras estruturas de dados
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.SERVER_IP, self.SERVER_PORT))
        self.pacotes_dict = {}  # Dicionário para armazenar pacotes enviados
        self.clientes = set()  # Conjunto de clientes conectados
        self.mensagens = {}  # Dicionário para armazenar mensagens recebidas

    # Inicia um temporizador para retransmissão de pacotes
    def iniciar_temporizador(self, pacote, endereco, num_seq):
        temporizador = threading.Timer(self.ACK_TIMEOUT, self.retransmitir_pacote, [pacote, endereco, num_seq])
        temporizador.start()
        self.pacotes_dict[(endereco, num_seq)]["temporizador"] = temporizador

    # Retransmite um pacote caso o ACK não seja recebido
    def retransmitir_pacote(self, pacote, endereco, num_seq):
        print(f"ACK não foi recebido para o pacote {num_seq}. Retransmitindo o pacote para o cliente {endereco}...")
        self.sock.sendto(pacote, endereco)
        self.iniciar_temporizador(pacote, endereco, num_seq)

    # Envia um arquivo para o cliente, dividindo-o em pacotes
    def enviar_arquivo(self, nome_arquivo, nome, cliente, endereco):
        with open(nome_arquivo, 'rb') as f:
            conteudo_arquivo = f.read()

        tamanho_total = len(conteudo_arquivo)
        total_pacotes = ceil(tamanho_total / (self.BUFFER_SIZE - 100))  # Calcula o número total de pacotes
        id_aleatorio = string_aleatoria_minuscula()  # Gera um ID aleatório para a mensagem

        for i in range(total_pacotes):
            inicio = i * (self.BUFFER_SIZE - 100)
            fim = inicio + (self.BUFFER_SIZE - 100)
            conteudo = conteudo_arquivo[inicio:fim].decode('utf-8')
            checksum = calcular_checksum(conteudo)  # Calcula o checksum do pacote
            num_seq = i + 1  # Número de sequência do pacote
            pacote = f"{id_aleatorio}|{total_pacotes}|{nome}|{endereco[0]}|{endereco[1]}|{conteudo}|{checksum}|{num_seq}".encode('utf-8')
            self.pacotes_dict[(cliente, num_seq)] = {"pacote": pacote, "contagem_ack": 0, "temporizador": None}
            self.sock.sendto(pacote, cliente)  # Envia o pacote
            self.iniciar_temporizador(pacote, cliente, num_seq)  # Inicia o temporizador para o pacote

    # Envia um ACK para o cliente
    def enviar_ack(self, num_seq, cliente):
        checksum = calcular_checksum(str(num_seq))
        mensagem_ack = f"ACK|{num_seq}|{checksum}".encode('utf-8')
        self.sock.sendto(mensagem_ack, cliente)

    # Envia uma mensagem para o cliente
    def enviar_mensagem(self, mensagem, nome, cliente, endereco, isAck=False):
        nome_arquivo = f'mensagem-s-{nome}.txt'
        if isAck:
            self.enviar_ack(mensagem, cliente)  # Envia um ACK se for necessário
        else:
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write(mensagem)  # Salva a mensagem em um arquivo temporário
            self.enviar_arquivo(nome_arquivo, nome, cliente, endereco)  # Envia o arquivo
            os.remove(nome_arquivo)  # Remove o arquivo temporário

    # Lida com as mensagens recebidas de um cliente
    def lidar_com_cliente(self, dados, endereco):
        try:
            if endereco not in self.clientes:
                self.clientes.add(endereco)  # Adiciona o cliente à lista de clientes conectados

            try:
                tipo_mensagem, *conteudo = dados.decode('utf-8').split('|')  # Decodifica a mensagem recebida
            except UnicodeDecodeError as e:
                print(f"Erro de decodificação de dados: {e}")
                return

            if tipo_mensagem == 'LOGIN':
                # Lida com o login de um cliente
                username = conteudo[0]
                mensagem_login = f"LOGIN| {username} entrou no chat."
                print(f'Usuário {endereco} com o username {username} entrou no chat.')
                for cliente in self.clientes:
                    if cliente != endereco:
                        self.sock.sendto(mensagem_login.encode('utf-8'), cliente)

            elif tipo_mensagem == "BYE":
                # Lida com a saída de um cliente
                username = conteudo[0]
                self.clientes.discard(endereco)
                mensagem = (f'Usuário {endereco} com o username {username} saiu no chat.')
                print(mensagem)
                for cliente in self.clientes:
                    if cliente != endereco:
                        self.sock.sendto(f"BYE|{mensagem}".encode('utf-8'), cliente)

            elif tipo_mensagem == "ACK":
                # Lida com o recebimento de um ACK
                num_seq = int(conteudo[0])
                checksum = conteudo[1]
                if checksum == calcular_checksum(str(num_seq)):
                    if self.pacotes_dict[(endereco, num_seq)]["contagem_ack"] >= 1:
                        # Retransmite o próximo pacote se o ACK for duplicado
                        self.retransmitir_pacote(self.pacotes_dict[(endereco, num_seq + 1)]["pacote"], endereco, num_seq + 1)
                        print(f"ACK duplicado recebido, retransmitindo pacote {num_seq} do cliente {endereco}...")
                        self.pacotes_dict[(endereco, num_seq)]["contagem_ack"] += 1
                    else:
                        self.pacotes_dict[(endereco, num_seq)]["contagem_ack"] = 1
                        print(f"ACK recebido para o pacote {num_seq} do cliente {endereco}")
                    self.pacotes_dict[(endereco, num_seq)]["temporizador"].cancel()
                else:
                    print(f"ACK {num_seq} do cliente {endereco} chegou corrompido.")

            elif tipo_mensagem in self.mensagens:
                # Lida com mensagens fragmentadas recebidas
                total_pacotes, nome, dados_pacote, checksum, num_seq = conteudo
                if num_seq in self.mensagens[tipo_mensagem]["pacotes"]:
                    print(f"Pacote já foi recebido pra esse num_seq {num_seq} para o cliente {endereco}, reenviando o ACK...")
                    self.enviar_mensagem(num_seq, nome, endereco, endereco, True)
                else:
                    if checksum == calcular_checksum(dados_pacote):
                        print(f"Checksum válido para o pacote {num_seq} do cliente {endereco}")
                        self.mensagens[tipo_mensagem]["pacotes"][num_seq] = dados_pacote
                        self.enviar_mensagem(num_seq, nome, endereco, endereco, True)
                        if len(self.mensagens[tipo_mensagem]["pacotes"]) == int(total_pacotes):
                            # Reconstrói a mensagem completa a partir dos pacotes recebidos
                            conteudo_arquivo = bytearray()
                            for i in range(1, int(total_pacotes) + 1):
                                conteudo_arquivo.extend(self.mensagens[tipo_mensagem]["pacotes"][str(i)].encode("utf-8"))
                            texto_mensagem = conteudo_arquivo.decode('utf-8')
                            print(f'Clientes: {self.clientes}')
                            for cliente in self.clientes:
                                if cliente != endereco:
                                    self.enviar_mensagem(texto_mensagem, nome, cliente, endereco)
                    else:
                        print(f"Checksum inválido para o pacote {dados_pacote} do cliente {endereco}")
                        if int(num_seq) > 1:
                            self.enviar_ack(int(num_seq) - 1, endereco)
            else:
                # Lida com mensagens não fragmentadas
                total_pacotes, nome, dados_pacote, checksum, num_seq = conteudo
                if checksum == calcular_checksum(dados_pacote):
                    print(f"Checksum válido para o pacote {num_seq} do cliente {endereco}")
                    self.mensagens[tipo_mensagem] = {"nome": nome, "pacotes": {num_seq: dados_pacote}}
                    self.enviar_mensagem(num_seq, nome, endereco, endereco, True)
                    if int(total_pacotes) == 1:
                        texto_mensagem = dados_pacote
                        for cliente in self.clientes:
                            if cliente != endereco:
                                self.enviar_mensagem(texto_mensagem, nome, cliente, endereco)
                else:
                    print(f"Checksum inválido para o pacote {dados_pacote} do cliente {endereco}")
                    if int(num_seq) > 1:
                        self.enviar_ack(int(num_seq) - 1, endereco)

        except Exception as e:
            print(f"Erro ao lidar com o cliente {endereco}: {e}, {type(e).__name__}, {e.args}")

    # Inicia o servidor e aguarda conexões
    def iniciar_servidor(self):
        print("Servidor iniciado")
        while True:
            try:
                dados, endereco = self.sock.recvfrom(self.BUFFER_SIZE)  # Recebe dados de um cliente
                threading.Thread(target=self.lidar_com_cliente, args=(dados, endereco)).start()  # Cria uma thread para lidar com o cliente
            except Exception as e:
                print(f"Erro no servidor: {e}, {type(e).__name__}, {e.args}")

# Cria uma instância do servidor e inicia o servidor
servidor = Servidor()
servidor.iniciar_servidor()