# Chat UDP com Transferência de Arquivos

Este projeto implementa um servidor de chat com transferência confiável de arquivos usando o protocolo UDP e o mecanismo RDT 3.0 (Reliable Data Transfer), desenvolvido como parte da disciplina IF975 - Redes de Computadores.

## Tecnologias Utilizadas
- Python
- Sockets UDP
- Programação concorrente com Threads

## Mecanismos de Confiabilidade
- Protocolo RDT 3.0
- Checksum MD5
- Controle de sequência (ACKs e números de sequência)
- Temporizadores e retransmissão
- Fragmentação/Reconstrução de datagramas

## Como Funciona
O servidor UDP gerencia as conexões de múltiplos clientes e retransmite mensagens utilizando o protocolo RDT 3.0 para garantir transferência confiável. Os clientes enviam mensagens e arquivos fragmentados em pacotes com checksum e números de sequência, enquanto o servidor confirma cada recebimento com ACKs e trata retransmissões em caso de perdas ou erros. O sistema mantém a ordem das mensagens e notifica a entrada/saída de usuários no chat.

### Recursos
✅ Múltiplos clientes podem se conectar ao servidor
✅ Transmissão de mensagens em tempo real
✅ Fragmentação Inteligente de arquivos (>1024 bytes) com reconstrução automática
✅ Identificação de usuário por nome
✅ Formato Padronizado de mensagens:
    <IP>:<PORTA>/~<nome>: <msg> <hora>
✅ Sistema de Comandos:
    - hi, meu nome eh <nome> - Conexão inicial
    - bye - Desconexão graciosa

## Como Clonar e Executar

### 1. Clonar o Repositório
Abra um terminal e execute:
```sh
git clone https://github.com/DevFlavioJunior/socket.git
cd socket
```

### 2. Instalar Dependências
Certifique-se de ter o Python instalado e execute:
```sh
pip install -r requirements.txt  # Se houver um arquivo de dependências
```

### 3. Iniciar o Servidor
Execute o seguinte comando para iniciar o servidor:
```sh
python server.py
```

### 4. Iniciar um Cliente
Abra outro terminal e execute:
```sh
python client.py
```
Digite um nome de usuário e comece a enviar mensagens!

## Estrutura do Projeto
```
/SOCKET
│
├── /Primeira-Entrega
│   ├── client.py          
│   ├── README.md             
│   └── server.py             
│
├── /Segunda-Entrega
│   ├── client.py          
│   ├── README.md             
│   └── server.py             
│
└── README.md               

## Como Contribuir
Se quiser contribuir para este projeto, siga os seguintes passos:
1. Faça um fork do repositório
2. Crie uma branch com sua funcionalidade (`git checkout -b minha-funcionalidade`)
3. Commit suas alterações (`git commit -m 'Adicionando nova funcionalidade'`)
4. Faça um push para a branch (`git push origin minha-funcionalidade`)
5. Abra um Pull Request