import os
import tempfile
from unittest.mock import patch

import pytest

from src.models.grafico_mu_epsilon import GraficoMuEpsilon


@pytest.fixture(autouse=True)
def setup_env(monkeypatch):
    """Configura variáveis de ambiente e diretórios temporários."""
    base_path = tempfile.mkdtemp(prefix="static_test_")
    os.makedirs(
        os.path.join(base_path, "images", "graficos_gerados"), exist_ok=True
    )
    os.makedirs(os.path.join(base_path, "files", "saidas"), exist_ok=True)
    monkeypatch.setenv("STATIC_FOLDER_PATH", base_path)
    return base_path


@pytest.fixture
def sample_txt(tmp_path):
    """Cria um arquivo .txt com dados simulados de frequência, epsilon e mu."""
    txt_path = tmp_path / "sample.txt"
    txt_content = (
        "8.0\t2.1\t0.3\t1.2\t0.2\n"
        "9.0\t2.3\t0.4\t1.3\t0.3\n"
        "10.0\t2.5\t0.5\t1.4\t0.4\n"
    )
    txt_path.write_text(txt_content)
    return str(txt_path)


def test_ler_dados_arquivo_txt(sample_txt):
    """Testa a leitura de dados do arquivo txt."""
    grafico = GraficoMuEpsilon(
        nome_arquivo_csv="teste.csv",
        caminho_arquivo_txt=sample_txt,
        unidade_frequencia="GHz",
        identificador_arquivo="123",
    )
    freq, eps, eps_p, mu, mu_p = grafico._ler_dados_arquivo_txt()
    assert len(freq) == 3
    assert eps[0] == 2.1
    assert mu_p[-1] == 0.4


@patch("matplotlib.pyplot.figure")
@patch("matplotlib.pyplot.plot")
def test_plotar_grafico(mock_plot, mock_fig, sample_txt, setup_env):
    """Testa a geração e salvamento do gráfico."""
    grafico = GraficoMuEpsilon(
        nome_arquivo_csv="teste.csv",
        caminho_arquivo_txt=sample_txt,
        unidade_frequencia="GHz",
        identificador_arquivo="abc123",
    )
    result = grafico.plotar_grafico()
    assert "nome_arquivo_imagem" in result
    assert result["nome_arquivo_imagem"].endswith(".png")
    assert os.path.exists(setup_env)


def test_baixar_dados_grafico(sample_txt, setup_env):
    grafico = GraficoMuEpsilon(
        nome_arquivo_csv="teste.csv",
        caminho_arquivo_txt=sample_txt,
        unidade_frequencia="GHz",
        identificador_arquivo="xyz789",
    )
    path_saida = grafico.baixar_dados_grafico()
    assert os.path.exists(path_saida)
    with open(path_saida, "r", encoding="utf-8") as f:
        conteudo = f.read()
    assert "F(GHz)" in conteudo
    assert "mu''" in conteudo
