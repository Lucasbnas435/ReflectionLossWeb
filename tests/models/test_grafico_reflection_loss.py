import os

import pytest

from src.models.grafico_reflection_loss import GraficoReflectionLoss

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "..", "fixtures")
SAMPLE_FILE = os.path.join(FIXTURE_DIR, "exemplo_txt.txt")


# Subclasse concreta temporária para testes
class GraficoReflectionLossTeste(GraficoReflectionLoss):
    def plotar_grafico(self):
        return {"dummy": True}

    def baixar_dados_grafico(self):
        return "dummy.txt"


@pytest.fixture
def grafico():
    """
    Fixture para criar um objeto GraficoReflectionLoss com arquivo de teste.
    """
    return GraficoReflectionLossTeste(
        nome_arquivo_csv="dummy.csv",
        caminho_arquivo_txt=SAMPLE_FILE,
        unidade_frequencia="GHz",
        identificador_arquivo="teste123",
    )


def test_ler_dados_arquivo_txt(grafico):
    """
    Testa se _ler_dados_arquivo retorna uma lista de strings.
    """
    linhas = grafico._ler_dados_arquivo_txt()
    assert isinstance(linhas, list)
    assert len(linhas) > 0
    assert all(isinstance(linha, str) for linha in linhas)


def test_calcular_rl_tipo_retorno(grafico):
    """
    Testa se _calcular_rl retorna duas listas de floats.
    """
    linhas = grafico._ler_dados_arquivo_txt()
    espessura_amostra = 2.0  # mm
    frequencias, s11_v = grafico._calcular_rl(linhas, espessura_amostra)

    assert isinstance(frequencias, list)
    assert isinstance(s11_v, list)
    assert all(isinstance(f, float) for f in frequencias)
    assert all(isinstance(v, float) for v in s11_v)
    assert len(frequencias) == len(s11_v)


def test_calcular_rl_valores_consistentes(grafico):
    """
    Testa se os valores de RL estão dentro de um intervalo esperado.
    """
    linhas = grafico._ler_dados_arquivo_txt()
    espessura_amostra = 2.0  # mm
    _, s11_v = grafico._calcular_rl(linhas, espessura_amostra)

    # faixa de valores coerente com essa amostra e espessura
    for valor in s11_v:
        assert -0.7 <= valor <= 0.1


def test_calcular_rl_com_outra_espessura(grafico):
    """
    Testa cálculo com espessura diferente, garantindo que o retorno muda.
    """
    linhas = grafico._ler_dados_arquivo_txt()
    frequencias1, s11_v1 = grafico._calcular_rl(linhas, 2.0)
    frequencias2, s11_v2 = grafico._calcular_rl(linhas, 5.0)

    # Listas de frequencias devem ser iguais, mas RL deve mudar
    assert frequencias1 == frequencias2
    assert s11_v1 != s11_v2
