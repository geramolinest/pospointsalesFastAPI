import logging

from typing import Annotated
from fastapi import Depends

from infrastructure.repositories import CategoriesRepository
from application.dto import AddCategory, GetCategory
from domain.entities import Category, APIResponse


from .....features.response.ServiceResponse import ServiceResponse

class AddCategoryCommand:
    
    __reposotiry: CategoriesRepository
    __response: ServiceResponse[GetCategory]
    
    def __init__(self, repository: Annotated[CategoriesRepository, Depends(CategoriesRepository)]) -> None:
        self.__reposotiry = repository
        self.__response = ServiceResponse[GetCategory]()
        
    async def add_category(self, category_to_be_saved: AddCategory) -> APIResponse[GetCategory]:
        
        try:
            exists = await self.__reposotiry.any_category_by_name(category_to_be_saved.category_name)
            
            if exists:
                return self.__response.bad_request_response('Category name already exists' ) # type: ignore
            
            category_saved: Category = await self.__reposotiry.add_category(Category(**category_to_be_saved.model_dump()))
            
            return self.__response.created_response(data=GetCategory(**category_saved.__dict__))
        except Exception as e:
            logging.error('Error add_category method', e.args)
            return self.__response.internal_server_error()  # type: ignore