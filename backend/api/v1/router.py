from fastapi import APIRouter

from api.v1.endpoints import admin, protected, public

api_v1_router = APIRouter()


public.include_routers(api_v1_router)
protected.include_routers(api_v1_router)
admin.include_routers(api_v1_router)
