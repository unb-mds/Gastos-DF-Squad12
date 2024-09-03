import pytest
from compras_automatico import fetch_and_process_data

def test_process_gazettes_execution():
    try:
        fetch_and_process_data('2024-01-01', '2024-01-02')
        assert True  # Se não houver exceções, o teste passa
    except Exception as e:
        pytest.fail(f"process_gazettes falhou com a exceção: {e}")

