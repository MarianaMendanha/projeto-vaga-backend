from . import db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class Department(db.Model):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    collaborators = relationship('Collaborator', back_populates='department')


class Collaborator(db.Model):
    __tablename__ = 'collaborators'
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey(
        'departments.id'), nullable=False)
    have_dependents = Column(Boolean, default=False)
    department = relationship("Department", back_populates="collaborators")
