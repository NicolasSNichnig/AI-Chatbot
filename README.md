# Chatbot NVIDIA com Memória Persistente

## Sobre o Projeto

Chatbot que utiliza API da NVIDIA NIM. Mantém histórico de conversas em arquivos JSON na pasta 'conversas'. Permite múltiplas sessões independentes.

https://github.com/user-attachments/assets/ae393b14-6a7c-4e8c-9943-96a9e746855f

## Requisitos

- Python 3.8+
- Pip
- Conta NVIDIA (API Key gratuita em build.nvidia.com)

## Instalação

### Linux

```bash
mkdir -p ~/nvidia_chatbot
cd ~/nvidia_chatbot
python3 -m venv venv
source venv/bin/activate
pip install openai python-dotenv
```

### Windows 

```mkdir %USERPROFILE%\nvidia_chatbot
cd %USERPROFILE%\nvidia_chatbot
python -m venv venv
venv\Scripts\activate
pip install openai python-dotenv
```

## Configuração

Crie um arquivo .env com o conteúdo:
```
API_KEY=sua_chave_api_aqui  
BASE_URL=https://integrate.api.nvidia.com/v1  
MODEL=Seu_ModeloIA  
```

## Obter API Key

https://build.nvidia.com/explore/discover

## Arquivos necessários

- chatbot.py (código principal)
- .env (configurações)

## Executar
Necessário estar na pasta criada para o chatbot

Linux: ```./iniciar.sh```  
Windows: ```python chatbot.py```  
