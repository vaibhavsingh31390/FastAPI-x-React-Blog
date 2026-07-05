import fastapi
from config.main_settings import SETTINGS
from api.v1.router import api_v1_router

app = fastapi.FastAPI(title=SETTINGS.PROJECT_NAME, version=SETTINGS.PROJECT_VERSION)
app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
