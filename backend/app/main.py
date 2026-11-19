from fastapi import FastAPI, Response

from prometheus_fastapi_instrumentator import Instrumentator


from app.controllers.url_controller import url_controller
from app.controllers.auth_controller import auth_controller

app = FastAPI()

Instrumentator().instrument(app).expose(app,endpoint="/metrics")


@app.get(
    "/favicon.ico",
    include_in_schema=False
)
def favicon():
    return Response(status_code=204)


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/health_check")
def health_check():
    return {
        "status": "OK",
        "message": "All Good"
    }

app.include_router(auth_controller)
app.include_router(url_controller)


