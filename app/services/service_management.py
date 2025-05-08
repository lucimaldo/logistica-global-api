from sqlalchemy.orm import Session
from datetime import datetime
import logging

from app import models, schemas

logger = logging.getLogger(__name__)

def get_service_info(db: Session, service_id: int):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return service

def register_service(db: Session, service: schemas.ServiceCreate):
    db_service = models.Service(
        nombre=service.nombre,
        descripcion=service.descripcion,
        endpoints=service.endpoints
    )
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service