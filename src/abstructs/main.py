from fastapi import FastAPI
from abstructs.routers import home, abstructs

app = FastAPI()

app.include_router(home.router)
app.include_router(abstructs.router)
