import re
import random
import string
import hashlib
import datetime
import os
import socket
import threading
from math import ceil

# Função para gerar uma string aleatória de 5 letras minúsculas
def string_aleatoria_minuscula():
    letras = string.ascii_lowercase
    return ''.join(random.choice(letras) for _ in range(5))

# Função para extrair o nome do usuário a partir de uma mensagem de introdução
def obter_nome_usuario(intro):
    padrao = r"hi, meu nome eh (.+)"
    correspondencia = re.match(padrao, intro)
    if correspondencia:
        return correspondencia.group(1)
    else:
        return None

# Função para calcular o checksum de uma string usando MD5
def calcular_checksum(dados):
    return hashlib.md5(dados.encode('utf-8')).hexdigest()

# Classe para manipular pacotes e gerenciar retransmissões
class ManipuladorPacotes:
    ACK_TIMEOUT = 0.1  # Tempo limite para receber um ACK

    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.dicionario_pacotes = {}  # Dicionário para armazenar pacotes e seus estados

    # Inicia um temporizador para retransmitir pacotes caso o ACK não seja recebido
    def iniciar_temporizador(self, pacote, addr, num_seq_esperado):
        temporizador = threading.Timer(self.ACK_TIMEOUT, self.retransmitir_pacote, [pacote, addr, num_seq_esperado])
        temporizador.start()
        self.dicionario_pacotes[num_seq_esperado]["temporizador"] = temporizador

    # Retransmite o pacote caso o ACK não tenha sido recebido
    def retransmitir_pacote(self, pacote, addr, num_seq_esperado):
        if self.dicionario_pacotes[num_seq_esperado]["contagem_ack"] == 0:
            print("ACK não foi recebido a tempo, retransmitindo o pacote...")
            self.client_socket.sendto(pacote, addr)
            self.iniciar_temporizador(pacote, addr, num_seq_esperado)

    # O ACK confirma o recebimento de um pacote específico.
    def enviar_ack(self, num_seq, cliente):
        checksum = calcular_checksum(str(num_seq))
        conteudo_com_cabecalho = f"ACK|{num_seq}|{checksum}".encode('utf-8')
        self.client_socket.sendto(conteudo_com_cabecalho, cliente)

# Classe principal do cliente
class Cliente:
    # Configurações do servidor
    SERVER_IP = "127.0.0.1"  # IP do servidor
    SERVER_PORT = 12345  # Porta do servidor
    BUFFER_SIZE = 1024  # Tamanho máximo do pacote

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(10)  # Define o tempo limite para operações de socket
        self.manipulador_pacotes = ManipuladorPacotes(self.client_socket)
        self.mensagens = {}  # Dicionário para armazenar mensagens recebidas
        self.saiu = False  # Flag para indicar se o cliente saiu
        self.iniciar_thread_recebimento()  # Inicia a thread para receber mensagens

    # Inicia uma thread para receber mensagens do servidor
    def iniciar_thread_recebimento(self):
        thread_recebimento = threading.Thread(target=self.receber_mensagens)
        thread_recebimento.daemon = True
        thread_recebimento.start()

    # Envia um arquivo para o servidor
    def enviar_arquivo(self, nome_arquivo, nome):
        with open(nome_arquivo, 'rb') as f:
            conteudo_arquivo = f.read()
        tamanho_total = len(conteudo_arquivo)
        total_pacotes = ceil(tamanho_total / (self.BUFFER_SIZE - 100))  # Divide o arquivo em pacotes
        id_aleatorio = string_aleatoria_minuscula()  # Gera um ID aleatório para o arquivo
        num_seq_esperado = 0
        for i in range(total_pacotes):
            inicio = i * (self.BUFFER_SIZE - 100)
            fim = inicio + (self.BUFFER_SIZE - 100)
            conteudo = conteudo_arquivo[inicio:fim].decode('utf-8')
            checksum = calcular_checksum(conteudo)
            num_seq_esperado = i + 1
            pacote = f"{id_aleatorio}|{total_pacotes}|{nome}|{conteudo}|{checksum}|{num_seq_esperado}".encode('utf-8')
            self.manipulador_pacotes.dicionario_pacotes[num_seq_esperado] = {"pacote": pacote, "contagem_ack": 0, "temporizador": None}
            self.client_socket.sendto(pacote, (self.SERVER_IP, self.SERVER_PORT))
            self.manipulador_pacotes.iniciar_temporizador(pacote, (self.SERVER_IP, self.SERVER_PORT), num_seq_esperado)

    # Envia uma mensagem para o servidor
    def enviar_mensagem(self, mensagem, nome, eh_ack=False):
        if eh_ack:
            self.manipulador_pacotes.enviar_ack(mensagem, (self.SERVER_IP, self.SERVER_PORT))
        else:
            nome_arquivo = f'mensagem-c-{nome}.txt'
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write(mensagem)
            self.enviar_arquivo(nome_arquivo, nome)
            os.remove(nome_arquivo)

    # Envia uma mensagem de login para o servidor
    def enviar_mensagem_login(self, nome):
        mensagem_login = f"LOGIN|{nome}".encode('utf-8')
        self.client_socket.sendto(mensagem_login, (self.SERVER_IP, self.SERVER_PORT))

    # Envia uma mensagem de saída para o servidor
    def enviar_mensagem_sair(self, nome):
        mensagem_sair = f"BYE|{nome}".encode('utf-8')
        self.client_socket.sendto(mensagem_sair, (self.SERVER_IP, self.SERVER_PORT))

    # Recebe mensagens do servidor
    def receber_mensagens(self):
        while True:
            try:
                # Recebe dados do servidor
                dados, _ = self.client_socket.recvfrom(self.BUFFER_SIZE)
                # Decodifica os dados recebidos e separa o tipo de mensagem e seu conteúdo
                tipo_mensagem, *conteudo = dados.decode('utf-8').split('|')
                
                # Processa mensagens de login
                if tipo_mensagem == "LOGIN":
                    print(*conteudo)
                
                # Processa mensagens de saída
                elif tipo_mensagem == "BYE":
                    print(*conteudo)
                
                # Processa mensagens de ACK
                elif tipo_mensagem == "ACK":
                    num_seq = int(conteudo[0])
                    checksum = conteudo[1]
                    # Verifica se o checksum do ACK é válido
                    if checksum == calcular_checksum(str(num_seq)):
                        # Verifica se o ACK já foi recebido anteriormente
                        if self.manipulador_pacotes.dicionario_pacotes[num_seq]["contagem_ack"] >= 1:
                            # Retransmite o próximo pacote se o ACK for duplicado
                            self.manipulador_pacotes.retransmitir_pacote(
                                self.manipulador_pacotes.dicionario_pacotes[num_seq + 1]["pacote"],
                                (self.SERVER_IP, self.SERVER_PORT), num_seq + 1)
                            print("ACK duplicado detectado, retransmitindo o pacote...")
                            self.manipulador_pacotes.dicionario_pacotes[num_seq]["contagem_ack"] += 1
                        else:
                            # Marca o ACK como recebido com sucesso
                            self.manipulador_pacotes.dicionario_pacotes[num_seq]["contagem_ack"] = 1
                            print(f"ACK recebido com sucesso para o pacote {num_seq}")
                        # Cancela o temporizador do pacote
                        self.manipulador_pacotes.dicionario_pacotes[num_seq]["temporizador"].cancel()
                    else:
                        print(f"ACK {num_seq} chegou corrompido.")
                
                # Processa pacotes de dados já existentes na lista de mensagens
                elif tipo_mensagem in self.mensagens:
                    total_pacotes, nome, ip_remetente, porta_remetente, pacote, checksum, num_seq = conteudo
                    # Verifica se o pacote já foi recebido anteriormente
                    if num_seq in self.mensagens[tipo_mensagem]["pacotes"]:
                        print(f"O pacote com o número de sequência {num_seq} já foi recebido anteriormente. Reenviando o ACK...")
                        self.enviar_mensagem(num_seq, nome, True)
                    else:
                        # Verifica se o checksum do pacote é válido
                        if checksum == calcular_checksum(pacote):
                            print(f"Pacote {num_seq} recebido com checksum válido.")
                            self.enviar_mensagem(num_seq, nome, True)
                            self.mensagens[tipo_mensagem]["pacotes"][num_seq] = pacote
                            # Verifica se todos os pacotes foram recebidos
                            if int(total_pacotes) == len(self.mensagens[tipo_mensagem]["pacotes"]):
                                data_atual = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")
                                pacotes_reunidos = ""
                                # Reúne os pacotes na ordem correta
                                for i in range(1, int(total_pacotes) + 1):
                                    pacotes_reunidos += self.mensagens[tipo_mensagem]["pacotes"][str(i)]
                                mensagem_final = f"{ip_remetente}:{porta_remetente}/~{nome}: {pacotes_reunidos} {data_atual}"
                                print(mensagem_final)
                                print()
                        else:
                            print(f"Pacote {num_seq} recebido com checksum inválido: {pacote}")
                            # Reenvia o ACK do pacote anterior em caso de erro
                            if int(num_seq) > 1:
                                self.enviar_mensagem(int(num_seq) - 1, nome, True)
                
                # Processa pacotes de dados novos
                else:
                    total_pacotes, nome, ip_remetente, porta_remetente, pacote, checksum, num_seq = conteudo
                    # Verifica se o checksum do pacote é válido
                    if checksum == calcular_checksum(pacote):
                        print(f"Checksum válido para o pacote {num_seq}")
                        self.enviar_mensagem(num_seq, nome, True)
                        self.mensagens[tipo_mensagem] = {"nome": nome, "pacotes": {num_seq: pacote}}
                        # Verifica se o pacote é único
                        if total_pacotes == '1':
                            data_atual = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")
                            mensagem_final = f"{ip_remetente}:{porta_remetente}/~{nome}: {pacote} {data_atual}"
                            print(mensagem_final)
                            print()
                    else:
                        print(f"Checksum inválido para o pacote {pacote}")
                        # Reenvia o ACK do pacote anterior em caso de erro
                        if int(num_seq) > 1:
                            self.enviar_mensagem(int(num_seq) - 1, nome, True)
            
            # Trata o timeout do socket
            except socket.timeout:
                continue
            
            # Trata outros erros
            except Exception as e:
                print(f"Erro ao receber mensagem: {e}")

# Instancia o cliente e inicia o loop principal
cliente = Cliente()
print("Pra se conectar a sala digite 'hi, meu nome eh <nome_do_usuario>':")

while not cliente.saiu:
    intro = input()
    if intro.startswith("hi, meu nome eh "):
        nome = obter_nome_usuario(intro)
        cliente.enviar_mensagem_login(nome)
        print(f"Olá, {nome}! Vamos começar o chat! Digite sua mensagem a seguir")
        while True:
            mensagem = input()
            if mensagem.lower() == "bye":
                cliente.enviar_mensagem_sair(nome)
                cliente.saiu = True
                break
            cliente.enviar_mensagem(mensagem, nome)
    else:
        print("Comando inválido! Por favor, digite 'hi, meu nome eh <nome_do_usuario>' para se conectar à sala:")
