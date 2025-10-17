import os
from unittest.mock import patch

import pytest

from src.models.grafico_espessura_dinamica import GraficoEspessuraDinamica
from src.models.grafico_espessura_fixa import GraficoEspessuraFixa
from src.models.grafico_espessura_variavel import GraficoEspessuraVariavel


@pytest.fixture(autouse=True)
def setup_env(monkeypatch, tmp_path):
    base_path = tmp_path / "static_test"
    (base_path / "images" / "graficos_gerados").mkdir(parents=True)
    (base_path / "files" / "saidas").mkdir(parents=True)
    monkeypatch.setenv("STATIC_FOLDER_PATH", str(base_path))
    return str(base_path)


# Simula conteúdo de um arquivo .txt real (mockado)
@pytest.fixture
def sample_txt(tmp_path):
    txt_path = tmp_path / "sample.txt"
    txt_content = (
        "8.0\t2.1\t0.3\t1.2\t0.2\n"
        "9.0\t2.3\t0.4\t1.3\t0.3\n"
        "10.0\t2.5\t0.5\t1.4\t0.4\n"
    )
    txt_path.write_text(txt_content)
    return str(txt_path)


# Lista de classes derivadas de GraficoReflectionLoss
@pytest.mark.parametrize(
    "GraficoClass,extra_args",
    [
        (GraficoEspessuraFixa, {"espessura_amostra": 2.5}),
        (GraficoEspessuraDinamica, {}),
        (GraficoEspessuraVariavel, {}),
    ],
)
class TestSubclassesGraficoReflectionLoss:
    """Testes para as subclasses de GraficoReflectionLoss."""

    @patch("matplotlib.pyplot.figure")
    @patch("matplotlib.pyplot.plot")
    def test_plotar_grafico(
        self,
        mock_plot,
        mock_fig,
        GraficoClass,
        extra_args,
        sample_txt,
        setup_env,
    ):
        """Testa geração do gráfico (plotar_grafico)."""
        grafico = GraficoClass(
            nome_arquivo_csv="teste.csv",
            caminho_arquivo_txt=sample_txt,
            unidade_frequencia="GHz",
            identificador_arquivo="abc123",
            **extra_args,
        )

        result = grafico.plotar_grafico()
        assert "caminho_imagem" in result
        assert result["caminho_imagem"].endswith(".png")
        assert os.path.exists(setup_env)

    def test_baixar_dados_grafico(
        self, GraficoClass, extra_args, sample_txt, setup_env
    ):
        grafico = GraficoClass(
            nome_arquivo_csv="teste.csv",
            caminho_arquivo_txt=sample_txt,
            unidade_frequencia="GHz",
            identificador_arquivo="xyz789",
            **extra_args,
        )
        path_saida = grafico.baixar_dados_grafico()
        assert os.path.exists(path_saida)
