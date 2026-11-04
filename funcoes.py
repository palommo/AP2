import random

# Exercício 1 
def classificar_produto(quantidade):
    if quantidade < 0:
        return "Quantidade inválida"
    if quantidade == 0:
        return "Sem estoque"
    if quantidade <= 5:
        return "Estoque baixo"
    if quantidade <= 20:
        return "Estoque normal"
    return "Estoque alto"


# Exercício 2
def inverter_palavras(texto):
    palavras = texto.split()
    return " ".join(reversed(palavras))


# Exercício 3
def validar_documento(documento):
    limpo = documento.replace(".", "").replace("-", "")
    return limpo.isascii() and limpo.isdigit() and len(limpo) == 11


# Exercício 4
def gerar_codigo():
    return f"USR-{random.randint(1000, 9999)}"

def criar_identificacao(nome):
    codigo = gerar_codigo()
    return f"Usuário {nome} cadastrado com código {codigo}."


# Exercício 5
USUARIOS_AUTORIZADOS = {"admin", "carlos", "maria"}

def verificar_permissao(usuario):
    return usuario in USUARIOS_AUTORIZADOS

def acessar_sistema(usuario):
    if verificar_permissao(usuario):
        return "Acesso autorizado"
    return "Acesso negado"


# Exercício 6
FILA_CLIENTES = ["Ana", "Bruno", "Carla"]

def obter_proximo_cliente():
    if FILA_CLIENTES:
        return FILA_CLIENTES.pop(0)
    return None

def registrar_atendimento(cliente):
    return True

def atender_proximo_cliente():
    cliente = obter_proximo_cliente()
    if not cliente:
        return "Fila vazia"
    if registrar_atendimento(cliente):
        return "Atendimento realizado"
    return "Falha no atendimento"
