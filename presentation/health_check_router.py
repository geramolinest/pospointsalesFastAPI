from fastapi.routing import APIRouter

health_check_router: APIRouter = APIRouter(prefix='/health')


@health_check_router.get('')
async def health_check() -> dict[str,str]:
    return { 'msg': 'Health check passed!'}