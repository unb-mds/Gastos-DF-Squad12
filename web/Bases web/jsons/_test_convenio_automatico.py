import pytest
from convenio_automatico import process_gazettes

def test_process_gazettes_execution():
    try:
        process_gazettes()
        assert True  # Se não houver exceções, o teste passa
    except Exception as e:
        pytest.fail(f"process_gazettes falhou com a exceção: {e}")

