from fastapi import APIRouter

from api.v1.endpoints import admin, protected, public

api_v1_router = APIRouter()

for router in public.routers:
    api_v1_router.include_router(router)

protected.include_routers(api_v1_router)
admin.include_routers(api_v1_router)
