from fastapi import APIRouter, Depends
from api.v1.endpoints.protected import comment, post, user
from api.dependencies.auth import get_current_user


__all__ = ["comment", "post", "user", "routers"]

dependencies = [Depends(get_current_user)]

routers = [
    user.router,
    post.router,
    comment.router,
]


def include_routers(parent: APIRouter) -> None:
    for router in routers:
        parent.include_router(router, dependencies=dependencies)
