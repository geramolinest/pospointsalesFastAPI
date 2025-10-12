from fastapi import APIRouter

from .health_check_router import health_check_router
from .categories_router import categories_router


main_routerv1: APIRouter = APIRouter(prefix='/api/v1', tags=['V1'])


main_routerv1.include_router(health_check_router)
main_routerv1.include_router(categories_router)