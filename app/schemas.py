from typing import Optional, List
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    nombre_usuario: Optional[str] = None
    rol: Optional[str] = None

class User(BaseModel):
    nombre_usuario: str
    rol: str
    activo: Optional[bool] = None

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    nombre_usuario: str
    contrasena: str
    rol: str = "Usuario"

class AuthorizeRequest(BaseModel):
    recursos: List[str]
    rol_usuario: str

class OrchestrationRequest(BaseModel):
    servicio_destino: str
    parametros_adicionales: dict

class ServiceInfo(BaseModel):
    id: int
    nombre: str
    descripcion: str
    endpoints: dict
    activo: bool

    class Config:
        orm_mode = True

class ServiceCreate(BaseModel):
    nombre: str
    descripcion: str
    endpoints: dict

class OrchestrationRulesUpdate(BaseModel):
    reglas: dict