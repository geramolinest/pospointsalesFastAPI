from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from typing import Annotated
from fastapi import Depends, Path

from application.dto import AddCategory, GetCategory
from application.features.categories.commands import AddCategoryCommand
from application.features.categories.queries import GetAllCategoriesFeature, GetCategoryByIdFeature

from domain.entities import APIResponse

categories_router: APIRouter = APIRouter(prefix='/categories', tags=['Categories'])

@categories_router.post('/create', response_model=APIResponse[GetCategory])
async def create_category( add_category: AddCategory, service: Annotated[AddCategoryCommand, Depends(AddCategoryCommand)]):
        
    result = await service.add_category( add_category )
    
    if result.status_code >299:
        raise HTTPException(result.status_code, detail={ **result.model_dump()})
    
    return result

@categories_router.get('')
async def get_all_categories(service: Annotated[GetAllCategoriesFeature, Depends(GetAllCategoriesFeature)] ) -> APIResponse[list[GetCategory]]:
    result = await service.get_all_categories()
    
    if result.status_code > 299:
        raise HTTPException(result.status_code, detail={ **result.model_dump() })
    
    return result


@categories_router.get('/{id}')
async def get_category_by_id(id: Annotated[int, Path(title='Id category to be searched')], service: Annotated[GetCategoryByIdFeature, Depends(GetCategoryByIdFeature)]) -> APIResponse[GetCategory]:
    
    result = await service.get_category_by_id(id)
    
    if result.status_code > 299:
        raise HTTPException(result.status_code, detail={ **result.model_dump() })
    
    return result