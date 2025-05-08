from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import timedelta

from app import models, schemas, services
from app.database import SessionLocal, engine
from app.security import (
    authenticate_user,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Orquestación de Servicios - Logística Global",
    description="API para la automatización de orquestación de servicios REST",
    version="1.0.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints de Autenticación
@app.post("/autenticar-usuario", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: SessionLocal = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.nombre_usuario, "rol": user.rol},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/autorizar-acceso")
async def authorize_access(
    request: schemas.AuthorizeRequest,
    current_user: schemas.User = Depends(get_current_user),
    db: SessionLocal = Depends(get_db)
):
    return services.auth.authorize_access(db, current_user, request)

# Endpoints de Orquestación
@app.post("/orquestar")
async def orchestrate_service(
    request: schemas.OrchestrationRequest,
    current_user: schemas.User = Depends(get_current_user),
    db: SessionLocal = Depends(get_db)
):
    if current_user.rol not in ["Orquestador", "Administrador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para orquestar servicios"
        )
    return services.orchestration.orchestrate_service(db, request)

# Endpoints de Gestión de Servicios
@app.get("/informacion-servicio/{service_id}", response_model=schemas.ServiceInfo)
async def get_service_info(
    service_id: int,
    current_user: schemas.User = Depends(get_current_user),
    db: SessionLocal = Depends(get_db)
):
    return services.service_management.get_service_info(db, service_id)

@app.post("/registrar-servicio", response_model=schemas.ServiceInfo)
async def register_service(
    service: schemas.ServiceCreate,
    current_user: schemas.User = Depends(get_current_user),
    db: SessionLocal = Depends(get_db)
):
    if current_user.rol != "Administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden registrar servicios"
        )
    return services.service_management.register_service(db, service)

@app.put("/actualizar-reglas-orquestacion")
async def update_orchestration_rules(
    rules: schemas.OrchestrationRulesUpdate,
    current_user: schemas.User = Depends(get_current_user),
    db: SessionLocal = Depends(get_db)
):
    if current_user.rol != "Orquestador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los orquestadores pueden actualizar reglas"
        )
    return services.orchestration.update_orchestration_rules(db, rules)