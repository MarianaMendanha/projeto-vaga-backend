from .models import Department, Collaborator
from . import db


class DepartmentService:
    @staticmethod
    def get_all_departments():
        """Retorna todos os departamentos."""
        return Department.query.all()

    @staticmethod
    def get_department_by_id(department_id):
        """Retorna um departamento pelo ID."""
        return Department.query.get(department_id)

    @staticmethod
    def create_department(name):
        """Cria um novo departamento."""
        new_department = Department(name=name)
        db.session.add(new_department)
        db.session.commit()
        return new_department

    @staticmethod
    def get_collaborators_in_department(department_id):
        """Retorna todos os colaboradores de um departamento específico."""
        department = DepartmentService.get_department_by_id(department_id)
        return department.collaborators if department else None


class CollaboratorService:
    @staticmethod
    def create_collaborator(full_name, department_id, have_dependents=False):
        """Cria um novo colaborador."""
        new_collaborator = Collaborator(
            full_name=full_name, department_id=department_id, have_dependents=have_dependents)
        db.session.add(new_collaborator)
        db.session.commit()
        return new_collaborator

    @staticmethod
    def get_collaborators_by_department(department_id):
        """Retorna todos os colaboradores de um departamento específico."""
        return Collaborator.query.filter_by(department_id=department_id).all()
