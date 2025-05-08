from sqlalchemy.orm import Session

from app import models, schemas

def authorize_access(db: Session, current_user: schemas.User, request: schemas.AuthorizeRequest):
    # Verificar si el usuario tiene acceso a los recursos solicitados
    authorized = False
    
    # Lógica de autorización basada en roles
    if current_user.rol == "Administrador":
        authorized = True
    elif current_user.rol == "Orquestador":
        # Verificar si los recursos están permitidos para orquestadores
        allowed_resources = ["orquestar", "informacion-servicio", "actualizar-reglas-orquestacion"]
        authorized = all(resource in allowed_resources for resource in request.recursos)
    elif current_user.rol == "Usuario":
        # Usuarios normales solo pueden acceder a información
        authorized = all(resource == "informacion-servicio" for resource in request.recursos)
    
    return {"autorizado": authorized, "rol_usuario": current_user.rol}