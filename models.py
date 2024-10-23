from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# Association table for User-Household relationship
user_household = Table('user_household', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('household_id', Integer, ForeignKey('households.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128))
    
    households = relationship('Household', secondary=user_household, back_populates='users')
    tasks = relationship('Task', back_populates='creator')
    assigned_tasks = relationship('Taskboard', back_populates='assigned_user')

    def __repr__(self):
        return f'<User {self.username}>'

class Household(Base):
    __tablename__ = 'households'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    
    users = relationship('User', secondary=user_household, back_populates='households')
    tasks = relationship('Task', back_populates='household')

    def __repr__(self):
        return f'<Household {self.name}>'

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    complexity = Column(Integer)  # You can define a scale, e.g., 1-5
    estimated_time = Column(Integer)  # In minutes
    created_at = Column(DateTime, default=datetime.utcnow)
    
    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship('User', back_populates='tasks')
    
    household_id = Column(Integer, ForeignKey('households.id'))
    household = relationship('Household', back_populates='tasks')
    
    taskboard = relationship('Taskboard', back_populates='task', uselist=False)

    def __repr__(self):
        return f'<Task {self.title}>'

class Taskboard(Base):
    __tablename__ = 'taskboard'
    id = Column(Integer, primary_key=True)
    
    task_id = Column(Integer, ForeignKey('tasks.id'), unique=True)
    task = relationship('Task', back_populates='taskboard')
    
    assigned_user_id = Column(Integer, ForeignKey('users.id'))
    assigned_user = relationship('User', back_populates='assigned_tasks')
    
    status = Column(String(20), default='To Do')  # e.g., 'To Do', 'In Progress', 'Done'
    assigned_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Taskboard {self.task.title} - {self.assigned_user.username}>'