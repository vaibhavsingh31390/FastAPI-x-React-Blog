from fastapi import APIRouter

from api.v1.endpoints import category, post, tag, user

api_v1_router = APIRouter()

api_v1_router.include_router(user.router)
api_v1_router.include_router(post.router)
api_v1_router.include_router(category.router)
api_v1_router.include_router(tag.router)
