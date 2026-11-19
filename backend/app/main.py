from fastapi import FastAPI

from prometheus_fastapi_instrumentator import Instrumentator


from app.controllers.url_controller import url_controller
from app.controllers.auth_controller import auth_controller

app = FastAPI()

Instrumentator().instrument(app).expose(app,endpoint="/metrics")
app.include_router(auth_controller)
app.include_router(url_controller)

@app.get("/health_check")
def health_check():
    return {
        "status": "OK",
        "message": "All Good"
    }