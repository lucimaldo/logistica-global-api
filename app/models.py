from sqlalchemy import Column, Integer, String, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String, unique=True, index=True)
    contrasena = Column(String)
    rol = Column(String, default="Usuario")
    activo = Column(Boolean, default=True)

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    endpoints = Column(JSON)
    activo = Column(Boolean, default=True)

class OrchestrationRule(Base):
    __tablename__ = "orchestration_rules"

    id = Column(Integer, primary_key=True, index=True)
    servicio_origen = Column(String)
    servicio_destino = Column(String)
    reglas = Column(JSON)
    activo = Column(Boolean, default=True)

class AccessLog(Base):
    __tablename__ = "access_logs"

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String)
    endpoint = Column(String)
    metodo = Column(String)
    parametros = Column(JSON)
    timestamp = Column(String)
    estado = Column(String)