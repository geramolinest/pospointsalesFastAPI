import logging
from fastapi import Depends
from typing import Annotated

from infrastructure.repositories import CategoriesRepository
from domain.entities import APIResponse
from application.dto import GetCategory

from ...response.ServiceResponse import ServiceResponse

class GetAllCategoriesFeature:
    
    __repository: CategoriesRepository
    __response: ServiceResponse[list[GetCategory]]
    
    def __init__(self, repository: Annotated[CategoriesRepository, Depends(CategoriesRepository)]) -> None:
        self.__repository = repository
        self.__response = ServiceResponse[list[GetCategory]]()
        
    async def get_all_categories(self) -> APIResponse[list[GetCategory]]:
        try:            
            result = await self.__repository.get_all_categories()
            return self.__response.ok_response( data= [ GetCategory( **item.__dict__ ) for item in result ])
        except Exception as e:
            logging.error(e)
            return self.__response.internal_server_error()  # type: ignore