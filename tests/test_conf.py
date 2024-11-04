# tests/test_conf.py

class TestConfig:
    """Configurações específicas para os testes."""
    TESTING = True  # Ativa o modo de teste
    DEBUG = False  # Desativa o modo de debug
    # Banco de dados em memória para testes
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # Desativa o rastreamento de modificações
    SQLALCHEMY_TRACK_MODIFICATIONS = False
