import os

import pytest

from src.models.dados_vna import DadosVna

# Caminho para a pasta de fixtures
FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "..", "fixtures")
SAMPLE_CSV = os.path.join(FIXTURE_DIR, "files", "csv_enviado", "exemplo.csv")
OUTPUT_TXT = os.path.join(FIXTURE_DIR, "files", "txt_gerado", "mm_exemplo.txt")


@pytest.fixture
def dados_vna(monkeypatch):
    """
    Fixture que cria um objeto DadosVna apontando para o CSV de teste.
    Monkeypatch é usado para sobrescrever os caminhos para evitar dependência da variável de ambiente.
    """
    monkeypatch.setenv("STATIC_FOLDER_PATH", FIXTURE_DIR)
    identificador = "exemplo"
    return DadosVna(identificador_arquivo=identificador)


def test_propriedades_iniciais(dados_vna):
    # Antes de ler o CSV, apenas identificador e caminhos devem estar definidos
    assert dados_vna.identificador_arquivo == "exemplo"
    assert os.path.basename(dados_vna.caminho_arquivo_csv) == "exemplo.csv"
    assert os.path.basename(dados_vna.caminho_arquivo_txt) == "mm_exemplo.txt"


def test_ler_csv(dados_vna):
    # Lê o CSV e verifica se os atributos são populados corretamente
    dados_vna.ler_csv()

    assert isinstance(dados_vna.frequencia_corte, float)
    assert isinstance(dados_vna.unidade_frequencia, str)
    assert isinstance(dados_vna.comprimento_suporte_amostra, float)
    assert isinstance(dados_vna.distancia_amostra, float)
    assert isinstance(dados_vna.espessura_amostra, float)
    assert isinstance(dados_vna.ifbw, float)
    assert isinstance(dados_vna.power, float)
    assert dados_vna.nome_banda in [
        "Banda X",
        "Banda Ku",
        "Banda K",
        "Banda Ka",
        "Não reconhecida",
    ]


def test_gerar_arquivo_txt(dados_vna):
    # Força a sobrescrição do caminho do TXT para não sobrescrever arquivos reais
    dados_vna._DadosVna__caminho_arquivo_txt = OUTPUT_TXT
    dados_vna._DadosVna__caminho_arquivo_csv = SAMPLE_CSV

    # Gera o arquivo TXT
    dados_vna.gerar_arquivo_txt()

    # Verifica se o arquivo TXT foi criado
    assert os.path.exists(OUTPUT_TXT)

    # Verifica se o conteúdo tem linhas
    with open(OUTPUT_TXT, "r", encoding="utf-8") as f:
        linhas = f.readlines()
    assert len(linhas) > 0
    assert "\t" in linhas[0]

    # Limpa arquivo de saída após o teste
    os.remove(OUTPUT_TXT)
