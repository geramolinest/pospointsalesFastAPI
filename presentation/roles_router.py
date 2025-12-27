from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException, Query

from application.features.roles.commands import AddRoleCommand, AsignRole
from application.features.roles.queries import GetRolesQuery

from application.dto.security import AddRole as AddRoleDTO, GetRole, AsignRole as AsignRoleDTO

from application.features.security import authorize

from domain.entities import APIResponse

roles_router: APIRouter = APIRouter(prefix="/roles", tags=["roles"])

@roles_router.post("/create", status_code=status.HTTP_201_CREATED)
@authorize(['admin'])
async def create_role(role: AddRoleDTO, command: Annotated[AddRoleCommand, Depends(AddRoleCommand)]) -> APIResponse[GetRole]:
    result: APIResponse[GetRole] = await command.add_role( role )

    if result.status_code > 299:
        raise HTTPException(status_code=result.status_code, detail= { **result.model_dump() })
    
    return result

@roles_router.get("/")
@authorize(['admin'])
async def get_roles( query: Annotated[GetRolesQuery, Depends(GetRolesQuery)], limit: int = Query(default=100, ge=0), offset: int = Query(default=0, ge=0) ) -> APIResponse[list[GetRole]]:
    result: APIResponse[list[GetRole]] = await query.get_roles(limit, offset)
    
    return result

@roles_router.post("/asign-role")
@authorize(['admin'])
async def asign_role_to_user( asign_role: AsignRoleDTO, command: Annotated[AsignRole, Depends(AsignRole)] ) -> APIResponse[str]:
    
    result: APIResponse[str] = await command.asign_role_to_user( asign_role.role_name, asign_role.username )

    if result.status_code > 299:
        raise HTTPException(status_code=result.status_code, detail= { **result.model_dump() })
    
    return result   