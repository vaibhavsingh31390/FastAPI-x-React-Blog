import fastapi
from core.config import Settings

app = fastapi.FastAPI(title=Settings.PROJECT_NAME, version=Settings.PROJECT_VERSION)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}



