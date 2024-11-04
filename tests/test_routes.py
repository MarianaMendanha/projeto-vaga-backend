# tests/test_routes.py

import pytest
from unittest.mock import patch, MagicMock
from app.models import Department, Collaborator


# Classe mock para simular objetos de colaboradores
class MockCollaborator:
    def __init__(self, id, full_name, department_id, have_dependents):
        self.id = id
        self.full_name = full_name
        self.department_id = department_id
        self.have_dependents = have_dependents


# Função de teste para verificar a rota que retorna todos os departamentos
def test_get_departments(client, init_database):
    # Usando patch para substituir a classe Department pelo mock
    with patch('app.routes.Department') as mock_department:
        # Criando objetos mock para departamentos
        mock_dept1 = MagicMock()
        mock_dept1.id = 1
        mock_dept1.name = 'HR'  # Simulando um departamento de Recursos Humanos

        mock_dept2 = MagicMock()
        mock_dept2.id = 2
        mock_dept2.name = 'Engineering'  # Simulando um departamento de Engenharia

        # Configurando o retorno da consulta mockada para retornar os departamentos simulados
        mock_department.query.all.return_value = [mock_dept1, mock_dept2]

        # Fazendo uma requisição GET à rota de departamentos
        response = client.get('/departments')
        # Verificando se o status da resposta é 200 (OK)
        assert response.status_code == 200
        # Verificando se o conteúdo da resposta contém os departamentos esperados
        assert response.json == [
            {'id': 1, 'name': 'HR'},
            {'id': 2, 'name': 'Engineering'}
        ]


# Função de teste para verificar a rota que retorna os colaboradores de um departamento específico
def test_get_collaborators(client, init_database):
    with patch('app.routes.Collaborator') as mock_collaborator, patch('app.routes.Department') as mock_department:
        # Criando um mock para o departamento
        mock_dept = MagicMock()
        mock_dept.id = 1
        # Simulando que o departamento com ID 1 existe
        mock_department.query.get.return_value = mock_dept

        # Configurando o retorno da consulta mockada para retornar colaboradores simulados
        mock_collaborator.query.filter_by.return_value.all.return_value = [
            MockCollaborator(1, 'Mariana Cruz', 1, False),
            MockCollaborator(1, 'Mariana Mendanha', 1, True)
        ]

        # Fazendo uma requisição GET à rota de colaboradores do departamento 1
        response = client.get('/departments/1/collaborators')

        # Verificando se o status da resposta é 200 (OK)
        assert response.status_code == 200
        # Verificando se o conteúdo JSON da resposta está correto
        assert response.json == [
            {'full_name': 'Mariana Cruz', 'have_dependents': False},
            {'full_name': 'Mariana Mendanha', 'have_dependents': True}
        ]


def test_get_collaborators_department_not_found(client, init_database):
    with patch('app.routes.Collaborator') as mock_collaborator:
        # Simulando que não há colaboradores
        mock_collaborator.query.filter_by.return_value.all.return_value = []

        response = client.get('/departments/999/collaborators')  # ID inválido
        assert response.status_code == 404  # Verifica se retorna 404
        assert response.json['message'] == 'Departamento não encontrado'


# Teste para adicionar um departamento
def test_add_department(client, init_database):
    # Dados para o novo departamento
    new_department = {'name': 'Marketing'}

    # Fazendo uma requisição POST para criar um novo departamento
    response = client.post('/department', json=new_department)

    # Verificando se o status da resposta é 201 (Created)
    assert response.status_code == 201
    # Verificando se a mensagem da resposta é a esperada
    assert response.json['message'] == 'Department added successfully!'

    # Verificando se o departamento foi realmente adicionado ao banco de dados
    added_department = Department.query.filter_by(name='Marketing').first()
    assert added_department is not None
    assert added_department.name == 'Marketing'


# Teste para criar um colaborador
def test_create_collaborator(client, init_database):
    # Primeiro, precisamos garantir que um departamento existe para adicionar um colaborador
    new_department = {'name': 'Sales'}
    # Criar um departamento para o colaborador
    client.post('/department', json=new_department)

    # Dados para o novo colaborador
    new_collaborator = {
        'full_name': 'Mariana Cruz',
        'department_id': 1,  # Presumindo que o ID do departamento 'Sales' é 1
        'have_dependents': False
    }

    # Fazendo uma requisição POST para criar um novo colaborador
    response = client.post('/collaborator', json=new_collaborator)

    # Verificando se o status da resposta é 201 (Created)
    assert response.status_code == 201
    # Verificando se a mensagem da resposta é a esperada
    assert response.json['message'] == 'Collaborator created successfully'

    # Verificando se o colaborador foi realmente adicionado ao banco de dados
    added_collaborator = Collaborator.query.filter_by(
        full_name='Mariana Cruz').first()
    assert added_collaborator is not None
    assert added_collaborator.full_name == 'Mariana Cruz'
    assert added_collaborator.department_id == 1


# Teste para adicionar um departamento com dados inválidos
def test_add_department_invalid(client, init_database):
    # Dados para um novo departamento sem nome
    invalid_department = {}

    # Fazendo uma requisição POST para criar um novo departamento
    response = client.post('/department', json=invalid_department)

    # Verificando se o status da resposta é 400 (Bad Request)
    assert response.status_code == 400


# Teste para criar um colaborador com dados inválidos
def test_create_collaborator_invalid(client, init_database):
    # Dados para um novo colaborador sem nome
    invalid_collaborator = {
        'department_id': 1,  # Presumindo que o ID do departamento existe
        'have_dependents': False
    }

    # Fazendo uma requisição POST para criar um novo colaborador
    response = client.post('/collaborator', json=invalid_collaborator)

    # Verificando se o status da resposta é 400 (Bad Request)
    assert response.status_code == 400
