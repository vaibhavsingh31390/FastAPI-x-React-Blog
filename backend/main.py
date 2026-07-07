import fastapi
from fastapi.middleware.cors import CORSMiddleware

from api.v1.router import api_v1_router
from config.main_settings import SETTINGS

app = fastapi.FastAPI(title=SETTINGS.PROJECT_NAME, version=SETTINGS.PROJECT_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=SETTINGS.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
