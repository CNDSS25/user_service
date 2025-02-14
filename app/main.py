from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(
    title="User Service API",
    description="API für Benutzeroperationen",
    version="1.0.0",
    docs_url='/docs',
    redoc_url='/docs',
    openapi_url='/openapi.json',
    root_path='/api/user',
)

#TODO: Make it hexagonal, pls
origins = [
    "http://localhost:3000","http://localhost:80", "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)