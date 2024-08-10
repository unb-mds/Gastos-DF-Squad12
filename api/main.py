from dotenv import load_dotenv
import os

load_dotenv()

# Agora o PYTHONPATH será configurado conforme o arquivo .env
import sys
sys.path.insert(0, os.getenv('PYTHONPATH'))

import uvicorn
from fastapi import FastAPI 

from puxador_bens.routers import puxador_bens_router

app = FastAPI()

app.include_router(puxador_bens_router.router)




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)