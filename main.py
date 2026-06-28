from fastapi import FastAPI
import uvicorn
from config import settings
from contextlib import asynccontextmanager
from database.session import create_db
from api.routers.words_api import router as words_api_router
from api.routers.words_web import router as words_web_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    yield


app = FastAPI(lifespan=lifespan, )
@app.get("/health_check")
async def health_check():
    return {'status': 'work!'}

app.include_router(words_api_router, tags=['Words'])
app.include_router(words_web_router)

if __name__ == "__main__":
    uvicorn.run('main:app', reload=settings.RELOAD, port=settings.PORT, host=settings.HOST)


