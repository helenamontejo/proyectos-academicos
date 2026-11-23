from pydantic import BaseModel
from typing import Optional

# DTO de respuesta
class MasajeDTO(BaseModel):
    id: int
    nombre: str
    duracion: int
    precio: float
    individual: bool
    user_id: str
    filename: Optional[str] = None

    class Config:
        from_attributes = True


# DTO de creación
class MasajeCreateDTO(BaseModel):
    nombre: str
    duracion: int
    precio: float
    individual: bool
    user_id: str
    filename: Optional[str] = None