from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

Base = declarative_base()

class TaskState(PyEnum):
    TO_DO = 'to-do'
    DOING = 'doing'
    DONE = 'done'

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    boards = relationship('Board', backref='user', lazy=True)

class Board(Base):
    __tablename__ = 'boards'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tasks = relationship('Task', backref='board', lazy=True)
    contributors = relationship('Contributor', backref='board', lazy=True)

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String(200), nullable=False)
    state = Column(Enum(TaskState), nullable=False, default=TaskState.TO_DO)
    board_id = Column(Integer, ForeignKey('boards.id'), nullable=False)

class Contributor(Base):
    __tablename__ = 'contributors'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    board_id = Column(Integer, ForeignKey('boards.id'), nullable=False)
    role = Column(String(20), nullable=False)

