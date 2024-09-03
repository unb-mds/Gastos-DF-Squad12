import pytest
import os

# Caminho do script a ser testado
script_path = os.path.join(os.path.dirname(__file__), 'licitacoes_automatico.py')

def test_script_execution():
    try:
        # Executa o script como um módulo para garantir que ele não gera exceções
        exec(open(script_path).read())
        assert True  # Se não houver exceções, o teste passa
    except Exception as e:
        pytest.fail(f"O script falhou com a exceção: {e}")
