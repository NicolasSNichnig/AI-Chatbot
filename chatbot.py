from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")

if not API_KEY:
    print("Erro: API_KEY não encontrada no arquivo .env")
    exit(1)

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)

PASTA_CONVERSAS = "conversas"

def criar_pasta_conversas():
    if not os.path.exists(PASTA_CONVERSAS):
        os.makedirs(PASTA_CONVERSAS)
        print(f"Pasta '{PASTA_CONVERSAS}/' criada!\n")

def listar_conversas():
    criar_pasta_conversas()
    
    caminho_pasta = PASTA_CONVERSAS
    arquivos = [f for f in os.listdir(caminho_pasta) if f.endswith('.json')]
    
    if arquivos:
        print("\nConversas existentes:")
        for i, arq in enumerate(arquivos, 1):
            caminho_completo = os.path.join(caminho_pasta, arq)
            try:
                with open(caminho_completo, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    qtd = len([m for m in dados if m['role'] != 'system'])
                    print(f"  {i}. {arq} ({qtd} mensagens)")
            except:
                print(f"  {i}. {arq}")
        print()
        return arquivos
    else:
        print("  (Nenhuma conversa salva ainda)\n")
        return []

def carregar_memoria(arquivo):
    criar_pasta_conversas()
    
    caminho_completo = os.path.join(PASTA_CONVERSAS, arquivo)
    
    if os.path.exists(caminho_completo):
        try:
            with open(caminho_completo, 'r', encoding='utf-8') as f:
                historico = json.load(f)
                print(f"Carregado: {arquivo} ({len(historico)-1} mensagens)")
                return historico
        except:
            print("Erro ao carregar. Iniciando nova conversa.")
            return [{"role": "system", "content": "Responda em português."}]
    else:
        print(f"Criando nova conversa: {arquivo}")
        return [{"role": "system", "content": "Responda em português."}]

def salvar_memoria(arquivo, mensagens):
    criar_pasta_conversas()
    
    caminho_completo = os.path.join(PASTA_CONVERSAS, arquivo)
    try:
        with open(caminho_completo, 'w', encoding='utf-8') as f:
            json.dump(mensagens, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Erro ao salvar: {e}")
        return False

def apagar_memoria(arquivo):
    caminho_completo = os.path.join(PASTA_CONVERSAS, arquivo)
    if os.path.exists(caminho_completo):
        os.remove(caminho_completo)
        return True
    return False

def obter_caminho_completo(arquivo):
    return os.path.join(PASTA_CONVERSAS, arquivo)

print("\nChatbot NVIDIA - DeepSeek-V4")
print("="*50)

criar_pasta_conversas()

listar_conversas()

print("Opções:")
print("  1 - Carregar conversa existente")
print("  2 - Criar nova conversa")
print("  3 - Apagar uma conversa")
print()

opcao = input("Escolha (1/2/3): ").strip()

if opcao == "1":
    arquivos = [f for f in os.listdir(PASTA_CONVERSAS) if f.endswith('.json')]
    if arquivos:
        print("\nConversas disponíveis:")
        for i, arq in enumerate(arquivos, 1):
            print(f"  {i}. {arq}")
        escolha = input("\nDigite o número: ").strip()
        try:
            ARQUIVO_MEMORIA = arquivos[int(escolha)-1]
        except:
            print("Opção inválida. Criando nova conversa...")
            nome = input("Nome da nova conversa (sem .json): ").strip()
            ARQUIVO_MEMORIA = f"{nome if nome else 'conversa'}.json"
    else:
        print("Nenhuma conversa encontrada. Criando nova...")
        nome = input("Nome da nova conversa (sem .json): ").strip()
        ARQUIVO_MEMORIA = f"{nome if nome else 'conversa'}.json"

elif opcao == "3":
    arquivos = [f for f in os.listdir(PASTA_CONVERSAS) if f.endswith('.json')]
    if arquivos:
        print("\nConversas para apagar:")
        for i, arq in enumerate(arquivos, 1):
            print(f"  {i}. {arq}")
        escolha = input("\nDigite o número para apagar: ").strip()
        try:
            arquivo_apagar = arquivos[int(escolha)-1]
            confirmar = input(f"Tem certeza que quer apagar '{arquivo_apagar}'? (s/n): ").strip()
            if confirmar.lower() == 's':
                caminho_apagar = os.path.join(PASTA_CONVERSAS, arquivo_apagar)
                os.remove(caminho_apagar)
                print(f"{arquivo_apagar} apagado!\n")
            else:
                print("Operação cancelada.\n")
        except:
            print("Opção inválida.\n")
    nome = input("Nome da nova conversa (sem .json): ").strip()
    ARQUIVO_MEMORIA = f"{nome if nome else 'conversa'}.json"

else:
    nome = input("Nome da nova conversa (sem .json): ").strip()
    ARQUIVO_MEMORIA = f"{nome if nome else 'conversa'}.json"

messages = carregar_memoria(ARQUIVO_MEMORIA)

print("\n" + "="*50)
print("Comandos:")
print("  • 'sair' - Encerra e SALVA conversa")
print("  • 'historico' - Mostra toda conversa")
print("  • 'limpar' - Limpa memória atual")
print("  • 'apagar_memoria' - Apaga ESTE arquivo")
print("  • 'tamanho_memoria' - Mostra quantas mensagens")
print("  • 'salvar_como' - Salva conversa com outro nome")
print("="*50)
print()

while True:
    user = input("Você: ").strip()
    
    if user.lower() == "sair":
        if salvar_memoria(ARQUIVO_MEMORIA, messages):
            print(f"\nMemória salva em: {PASTA_CONVERSAS}/{ARQUIVO_MEMORIA}")
        print("Até logo!\n")
        break
    
    if user.lower() == "historico":
        print("\nHISTÓRICO DA CONVERSA:")
        print("-"*40)
        for msg in messages:
            if msg['role'] == 'system':
                continue
            papel = "Você" if msg['role'] == 'user' else "IA"
            print(f"{papel}: {msg['content']}")
        print("-"*40)
        print(f"Total: {len(messages)-1} mensagens trocadas")
        print(f"Arquivo: {PASTA_CONVERSAS}/{ARQUIVO_MEMORIA}\n")
        continue
    
    if user.lower() == "limpar":
        messages = [messages[0]]
        salvar_memoria(ARQUIVO_MEMORIA, messages)
        print("Memória limpa! Arquivo atualizado.\n")
        continue
    
    if user.lower() == "apagar_memoria":
        if apagar_memoria(ARQUIVO_MEMORIA):
            messages = [messages[0]]
            print(f"ARQUIVO '{ARQUIVO_MEMORIA}' apagado! Conversa reiniciada.\n")
        else:
            print(f"Arquivo '{ARQUIVO_MEMORIA}' não encontrado.\n")
        continue
    
    if user.lower() == "tamanho_memoria":
        qtd = len([m for m in messages if m['role'] != 'system'])
        print(f"Memória atual: {qtd} mensagens")
        print(f"Arquivo: {PASTA_CONVERSAS}/{ARQUIVO_MEMORIA}\n")
        continue
    
    if user.lower() == "salvar_como":
        novo_nome = input("Novo nome para o arquivo (sem .json): ").strip()
        if novo_nome:
            novo_arquivo = f"{novo_nome}.json"
            if salvar_memoria(novo_arquivo, messages):
                print(f"Conversa salva como: {PASTA_CONVERSAS}/{novo_arquivo}\n")
            else:
                print("Erro ao salvar.\n")
        continue
    
    if not user:
        continue
    
    messages.append({"role": "user", "content": user})
    
    print("Processando... ", end="", flush=True)
    
    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=1,
            top_p=0.95,
            max_tokens=16384,
            extra_body={"chat_template_kwargs": {"thinking": False}},
            stream=False 
        )
        
        resposta = completion.choices[0].message.content
        
        print(f"\rIA: {resposta}\n")
        messages.append({"role": "assistant", "content": resposta})
        
        salvar_memoria(ARQUIVO_MEMORIA, messages)
        
    except Exception as e:
        print(f"\rErro: {e}\n")