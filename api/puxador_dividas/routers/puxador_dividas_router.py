from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from pydantic import BaseModel
from datetime import date
from Back.puxador_dividas import puxador_dividas


router = APIRouter(prefix="/puxador-dividas")

# A data deve ser no formato americano YYYY-MM-DD.
# Se o formato estiver incorreto ou se as datas não forem fornecidas, o FastAPI retornará um erro 422 de validação.

class DateRange(BaseModel):
    published_since: date
    published_until: date

@router.post("/")
async def post_dividas(date_range: DateRange):
    
    result = await puxador_dividas(date_range)
    
    if isinstance(result, int):
        # Se o resultado for um código de status, retorne um erro
        raise HTTPException(status_code=result, detail=f"Erro ao acessar a API: {result}")

    return result

