from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from LicensePlate.asgi import application as django_app

from routers.license_plate import router as license_plate_router
from routers.authentication import router as auth_router


app = FastAPI()

v1 = FastAPI()
v1.include_router(
    license_plate_router,
    prefix="/license-plate"
)

v1.include_router(
    auth_router,
    prefix="/auth"
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/api/v1/", v1)
app.mount("/app", django_app, "django_app")
