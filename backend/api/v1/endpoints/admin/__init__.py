from fastapi import APIRouter, Depends
from api.v1.endpoints.admin import category, tag, user
from api.dependencies.auth import get_current_admin

__all__ = ["category", "tag", "user", "routers"]

dependencies = [Depends(get_current_admin)]

routers = [
    user.router,
    category.router,
    tag.router,
]

def include_routers(parent: APIRouter) -> None:
    for router in routers:
        parent.include_router(router, dependencies=dependencies)