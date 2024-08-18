from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from pydantic import BaseModel
from datetime import date
from Back.Puxador_convenio import puxador_convenio


router = APIRouter(prefix="/puxador-convenio")

# A data deve ser no formato americano YYYY-MM-DD.
# Se o formato estiver incorreto ou se as datas não forem fornecidas, o FastAPI retornará um erro 422 de validação.

class DateRange(BaseModel):
    published_since: date
    published_until: date

@router.post("/")
async def post_convenio(date_range: DateRange):
    
    result = await puxador_convenio(date_range)
    
    if isinstance(result, int):
        # Se o resultado for um código de status, retorne um erro
        raise HTTPException(status_code=result, detail=f"Erro ao acessar a API: {result}")

    return result

