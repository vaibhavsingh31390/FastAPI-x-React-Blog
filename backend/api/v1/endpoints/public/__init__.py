from fastapi import APIRouter
from api.v1.endpoints.public import auth, category, post, tag, user

__all__ = ["auth", "category", "post", "tag", "user", "routers"]

routers = [
    auth.router,
    user.router,
    post.router,
    category.router,
    tag.router,
]

def include_routers(parent: APIRouter) -> None:
    for router in routers:
        parent.include_router(router)