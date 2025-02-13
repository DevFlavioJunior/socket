# Projeto de Chat UDP

Este projeto consiste em um sistema de chat utilizando comunicação via UDP, composto por um servidor e um cliente. O servidor recebe e transmite mensagens de múltiplos clientes, enquanto o cliente envia e recebe mensagens, incluindo o envio de arquivos fragmentados.

## Funcionalidades

- **Servidor UDP**:
  - Aceita múltiplos clientes.
  - Envia e recebe mensagens em tempo real.
  - Notifica a entrada e saída de usuários na sala de chat.
  - Suporte para envio e recebimento de arquivos fragmentados.
  
- **Cliente UDP**:
  - Conecta-se ao servidor.
  - Envia mensagens de texto e arquivos para o servidor.
  - Recebe mensagens do servidor em tempo real.
  - Suporte para desconectar-se da sala de chat com a mensagem "bye".

## Tecnologias Usadas

- Python 3
- Bibliotecas:
  - `socket` para comunicação UDP.
  - `threading` para multi-threading, permitindo enviar e receber mensagens simultaneamente.
  - `os` para manipulação de arquivos temporários.

## Como Rodar o Projeto

### 1. Configuração do Servidor

1. Clone o repositório:
   ```bash
   git clone https://github.com/DevFlavioJunior/socket.git
