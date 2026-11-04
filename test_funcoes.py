import re
from unittest.mock import patch
import pytest
from funcoes import (
    acessar_sistema,
    atender_proximo_cliente,
    classificar_produto,
    criar_identificacao,
    gerar_codigo,
    inverter_palavras,
    validar_documento,
)


# Exercício 1
def test_sem_estoque():
    assert classificar_produto(0) == "Sem estoque"

def test_estoque_baixo():
    assert classificar_produto(3) == "Estoque baixo"

def test_estoque_normal():
    assert classificar_produto(10) == "Estoque normal"

def test_estoque_alto():
    assert classificar_produto(50) == "Estoque alto"

def test_quantidade_negativa():
    assert classificar_produto(-1) == "Quantidade inválida"


# Exercício 2
def test_frase_varias_palavras():
    assert (
        inverter_palavras("Python é muito interessante")
        == "interessante muito é Python"
    )


def test_frase_uma_palavra():
    assert inverter_palavras("Python") == "Python"


def test_frase_vazia():
    assert inverter_palavras("") == ""


def test_frase_espacos_extras():
    assert inverter_palavras("  Python   é   legal  ") == "legal é Python"


def test_frase_numeros_e_letras():
    assert inverter_palavras("teste 123 abc 456") == "456 abc 123 teste"


# ---------------------------------------------------------------------------
# Exercício 3
# ---------------------------------------------------------------------------


def test_documento_11_digitos():
    assert validar_documento("12345678900") is True


def test_documento_formatado():
    assert validar_documento("123.456.789-00") is True


def test_documento_menos_de_11_digitos():
    assert validar_documento("1234567890") is False


def test_documento_mais_de_11_digitos():
    assert validar_documento("123456789012") is False


def test_documento_com_letras():
    assert validar_documento("1234567890a") is False


def test_documento_vazio():
    assert validar_documento("") is False


# ---------------------------------------------------------------------------
# Exercício 4
# ---------------------------------------------------------------------------


def test_gerar_codigo_formato():
    assert re.fullmatch(r"USR-\d{4}", gerar_codigo())


@patch("funcoes.gerar_codigo")
def test_mensagem_gerada_corretamente(mock_gerar):
    mock_gerar.return_value = "USR-1234"
    assert (
        criar_identificacao("Carlos")
        == "Usuário Carlos cadastrado com código USR-1234."
    )


@patch("funcoes.gerar_codigo")
def test_gerar_codigo_foi_chamada(mock_gerar):
    mock_gerar.return_value = "USR-1234"
    criar_identificacao("Carlos")
    mock_gerar.assert_called()


@patch("funcoes.gerar_codigo")
def test_gerar_codigo_chamada_uma_vez(mock_gerar):
    mock_gerar.return_value = "USR-1234"
    criar_identificacao("Carlos")
    mock_gerar.assert_called_once()


@pytest.mark.parametrize("codigo", ["USR-0001", "USR-5555", "USR-9999"])
@patch("funcoes.gerar_codigo")
def test_diferentes_codigos(mock_gerar, codigo):
    mock_gerar.return_value = codigo
    assert criar_identificacao("Carlos").endswith(f"código {codigo}.")


@pytest.mark.parametrize("nome", ["Carlos", "Maria", "João"])
@patch("funcoes.gerar_codigo")
def test_nomes_diferentes(mock_gerar, nome):
    mock_gerar.return_value = "USR-1234"
    assert (
        criar_identificacao(nome)
        == f"Usuário {nome} cadastrado com código USR-1234."
    )


# ---------------------------------------------------------------------------
# Exercício 5
# ---------------------------------------------------------------------------


@patch("funcoes.verificar_permissao")
def test_usuario_com_permissao(mock_perm):
    mock_perm.return_value = True
    assert acessar_sistema("carlos") == "Acesso autorizado"


@patch("funcoes.verificar_permissao")
def test_usuario_sem_permissao(mock_perm):
    mock_perm.return_value = False
    assert acessar_sistema("intruso") == "Acesso negado"


@patch("funcoes.verificar_permissao")
def test_verificar_permissao_foi_chamada(mock_perm):
    mock_perm.return_value = True
    acessar_sistema("carlos")
    mock_perm.assert_called_once()


@patch("funcoes.verificar_permissao")
def test_verificar_permissao_usuario_correto(mock_perm):
    mock_perm.return_value = True
    acessar_sistema("maria")
    mock_perm.assert_called_once_with("maria")


@pytest.mark.parametrize(
    "permissao, esperado",
    [(True, "Acesso autorizado"), (False, "Acesso negado")],
)
@patch("funcoes.verificar_permissao")
def test_mock_dois_cenarios(mock_perm, permissao, esperado):
    mock_perm.return_value = permissao
    assert acessar_sistema("qualquer") == esperado


# ---------------------------------------------------------------------------
# Exercício 6
# ---------------------------------------------------------------------------


@patch("funcoes.registrar_atendimento")
@patch("funcoes.obter_proximo_cliente")
def test_atendimento_realizado(mock_obter, mock_registrar):
    mock_obter.return_value = "Ana"
    mock_registrar.return_value = True
    assert atender_proximo_cliente() == "Atendimento realizado"


@patch("funcoes.registrar_atendimento")
@patch("funcoes.obter_proximo_cliente")
def test_fila_vazia(mock_obter, mock_registrar):
    mock_obter.return_value = None
    assert atender_proximo_cliente() == "Fila vazia"


@patch("funcoes.registrar_atendimento")
@patch("funcoes.obter_proximo_cliente")
def test_falha_ao_registrar(mock_obter, mock_registrar):
    mock_obter.return_value = "Ana"
    mock_registrar.return_value = False
    assert atender_proximo_cliente() == "Falha no atendimento"


@patch("funcoes.registrar_atendimento")
@patch("funcoes.obter_proximo_cliente")
def test_obter_proximo_cliente_foi_chamada(mock_obter, mock_registrar):
    mock_obter.return_value = "Ana"
    mock_registrar.return_value = True
    atender_proximo_cliente()
    mock_obter.assert_called_once()


@patch("funcoes.registrar_atendimento")
@patch("funcoes.obter_proximo_cliente")
def test_registrar_chamado_com_cliente_correto(mock_obter, mock_registrar):
    mock_obter.return_value = "Bruno"
    mock_registrar.return_value = True
    atender_proximo_cliente()
    mock_registrar.assert_called_once_with("Bruno")


@patch("funcoes.registrar_atendimento")
@patch("funcoes.obter_proximo_cliente")
def test_registrar_nao_chamado_com_fila_vazia(mock_obter, mock_registrar):
    mock_obter.return_value = None
    atender_proximo_cliente()
    mock_registrar.assert_not_called()
