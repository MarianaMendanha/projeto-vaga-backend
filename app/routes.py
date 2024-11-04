from flask import Blueprint, render_template, jsonify, request
from . import db
from .models import Department, Collaborator
from .services import DepartmentService, CollaboratorService
from flasgger import swag_from

api = Blueprint('api', __name__)


@api.route('/')
def index_home():
    return render_template('index.html', title='Bem-vindos', message='Esta é a minha aplicação Flask!')


@api.route('/departments', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Lista de departamentos retornada com sucesso',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'}
                    }
                }
            }
        },
        500: {
            'description': 'Erro ao buscar departamentos'
        }
    }
})
def get_departments():
    try:
        departments = DepartmentService.get_all_departments()
        return jsonify([{'id': dept.id, 'name': dept.name} for dept in departments])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/departments/<int:dept_id>/collaborators', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'dept_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de colaboradores retornada com sucesso',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'full_name': {'type': 'string'},
                        'have_dependents': {'type': 'boolean'}
                    }
                }
            }
        },
        404: {
            'description': 'Departamento não encontrado'
        }
    }
})
def get_collaborators(dept_id):
    collaborators = CollaboratorService.get_collaborators_by_department(
        dept_id)
    if not collaborators:
        return jsonify({'message': 'Departamento não encontrado'}), 404

    return jsonify([{'full_name': coll.full_name, 'have_dependents': coll.have_dependents} for coll in collaborators])


@api.route('/department', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Departamento adicionado com sucesso'
        },
        400: {
            'description': 'Erro na requisição'
        }
    }
})
def add_department():
    data = request.get_json()
    if 'name' not in data:
        return {"error": "O nome do departamento é obrigatório."}, 400

    new_department = DepartmentService.create_department(data['name'])
    return jsonify({'message': 'Department added successfully!'}), 201


@api.route('/collaborator', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'full_name': {
                        'type': 'string',
                        'example': 'John Doe',
                        'description': 'Nome completo do colaborador'
                    },
                    'department_id': {
                        'type': 'integer',
                        'example': 1,
                        'description': 'ID do departamento ao qual o colaborador pertence'
                    },
                    'have_dependents': {
                        'type': 'boolean',
                        'example': True,
                        'description': 'Indica se o colaborador tem dependentes'
                    }
                },
                'required': ['full_name', 'department_id']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Colaborador criado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Colaborador criado com sucesso'
                    }
                }
            }
        },
        400: {
            'description': 'Erro de validação'
        }
    }
})
def create_collaborator():
    data = request.get_json()
    if 'full_name' not in data or 'department_id' not in data:
        return {"error": "Nome completo e ID do departamento são obrigatórios."}, 400

    new_collaborator = CollaboratorService.create_collaborator(
        full_name=data['full_name'],
        department_id=data['department_id'],
        have_dependents=data.get('have_dependents', False)
    )
    return jsonify({'message': 'Collaborator created successfully'}), 201
