import sys
import os

# Adiciona o diretório Back ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Back'))

# Adiciona o diretório raiz ao PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
if project_root not in sys.path:
    sys.path.append(project_root)


import uvicorn
from fastapi import FastAPI 

from puxador_bens.routers import puxador_bens_router
from puxador_compras.routers import puxador_compras_router
from puxador_credito.routers import puxador_credito_router
from puxador_convenio.routers import puxador_convenio_router
from puxador_educacao.routers import puxador_educacao_router

app = FastAPI()

app.include_router(puxador_bens_router.router)
app.include_router(puxador_compras_router.router)
app.include_router(puxador_credito_router.router)
app.include_router(puxador_convenio_router.router)
app.include_router(puxador_educacao_router.router)




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)