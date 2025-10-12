import logging
from typing import Annotated
from fastapi import Depends

from infrastructure.repositories import CategoriesRepository
from domain.entities import APIResponse

from ...response.ServiceResponse import ServiceResponse
from ....dto import GetCategory

class GetCategoryByIdFeature:

    __repository: CategoriesRepository
    __response: ServiceResponse[GetCategory]
    
    def __init__(self, repository: Annotated[CategoriesRepository, Depends(CategoriesRepository)] ) -> None:
        self.__repository = repository
        self.__response = ServiceResponse[GetCategory]()
    
    async def get_category_by_id(self, id: int) -> APIResponse[GetCategory]:
        try:
            category_from_db = await self.__repository.get_category_by_id(id)

            if not category_from_db:
                return self.__response.not_found_response(msg='Category does not exists') #type: ignore
            
            return self.__response.ok_response(data=GetCategory( **category_from_db.__dict__ ))
        except Exception as e:
            logging.error(e)
            return self.__response.internal_server_error() #type: ignore

        
        