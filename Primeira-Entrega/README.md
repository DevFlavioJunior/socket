# Chat UDP com Transferência de Arquivos

Este projeto implementa um chat simples utilizando sockets UDP, permitindo a troca de mensagens entre clientes e a transferência de arquivos fragmentados.

## Tecnologias Utilizadas
- Python
- Sockets UDP
- Threads para recepção de mensagens
- Manipulação de arquivos

## Como Funciona
O servidor UDP gerencia as conexões e retransmite mensagens para todos os clientes conectados. Os clientes podem enviar mensagens de texto e arquivos de forma fragmentada. 

### Recursos
✅ Múltiplos clientes podem se conectar ao servidor
✅ Transmissão de mensagens em tempo real
✅ Transferência de arquivos utilizando fragmentos
✅ Identificação de usuário por nome
✅ Comando `bye` para sair do chat

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
/chat-udp
│-- client.py
│-- server.py
│-- README.md
```

## Como Contribuir
Se quiser contribuir para este projeto, siga os seguintes passos:
1. Faça um fork do repositório
2. Crie uma branch com sua funcionalidade (`git checkout -b minha-funcionalidade`)
3. Commit suas alterações (`git commit -m 'Adicionando nova funcionalidade'`)
4. Faça um push para a branch (`git push origin minha-funcionalidade`)
5. Abra um Pull Request
