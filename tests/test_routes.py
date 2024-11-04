# tests/test_routes.py

import pytest
from unittest.mock import patch, MagicMock
from app.models import Department, Collaborator
from app.services import DepartmentService, CollaboratorService


# Classe mock para simular objetos de colaboradores
class MockCollaborator:
    def __init__(self, id, full_name, department_id, have_dependents):
        self.id = id
        self.full_name = full_name
        self.department_id = department_id
        self.have_dependents = have_dependents


# Função de teste para verificar a rota que retorna todos os departamentos
def test_get_departments(client, init_database):
    with patch('app.services.DepartmentService.get_all_departments') as mock_get_all_departments:
        # Criando objetos mock para departamentos
        mock_dept1 = MagicMock()
        mock_dept1.id = 1
        mock_dept1.name = 'HR'

        mock_dept2 = MagicMock()
        mock_dept2.id = 2
        mock_dept2.name = 'Engineering'

        # Configurando o retorno da consulta mockada
        mock_get_all_departments.return_value = [mock_dept1, mock_dept2]

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
    with patch('app.services.CollaboratorService.get_collaborators_by_department') as mock_get_collaborators:
        # Configurando o retorno mockado para colaboradores
        mock_get_collaborators.return_value = [
            MockCollaborator(1, 'Mariana Cruz', 1, False),
            MockCollaborator(2, 'Mariana Mendanha', 1, True)
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
    with patch('app.services.CollaboratorService.get_collaborators_by_department') as mock_get_collaborators:
        # Simulando que não há colaboradores
        mock_get_collaborators.return_value = []

        response = client.get('/departments/999/collaborators')  # ID inválido
        assert response.status_code == 404  # Verifica se retorna 404
        assert response.json['message'] == 'Departamento não encontrado'


# Teste para adicionar um departamento
def test_add_department(client, init_database):
    new_department = {'name': 'Marketing'}

    with patch('app.services.DepartmentService.create_department') as mock_create_department:
        mock_create_department.return_value = MagicMock(id=3, name='Marketing')

        response = client.post('/department', json=new_department)

        assert response.status_code == 201
        assert response.json['message'] == 'Department added successfully!'


# Teste para criar um colaborador
def test_create_collaborator(client, init_database):
    new_department = {'name': 'Sales'}
    client.post('/department', json=new_department)

    new_collaborator = {
        'full_name': 'Mariana Cruz',
        'department_id': 1,
        'have_dependents': False
    }

    with patch('app.services.CollaboratorService.create_collaborator') as mock_create_collaborator:
        mock_create_collaborator.return_value = MagicMock(
            id=1, **new_collaborator)

        response = client.post('/collaborator', json=new_collaborator)

        assert response.status_code == 201
        assert response.json['message'] == 'Collaborator created successfully'


# Teste para adicionar um departamento com dados inválidos
def test_add_department_invalid(client, init_database):
    invalid_department = {}
    response = client.post('/department', json=invalid_department)
    assert response.status_code == 400

# Teste para criar um colaborador com dados inválidos


def test_create_collaborator_invalid(client, init_database):
    invalid_collaborator = {
        'department_id': 1,
        'have_dependents': False
    }
    response = client.post('/collaborator', json=invalid_collaborator)
    assert response.status_code == 400
