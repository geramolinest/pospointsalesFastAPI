from domain.entities import APIResponse
from typing import TypeVar, Generic

from utils import Constants

T = TypeVar('T')

class ServiceResponse(Generic[T]):
    
    @staticmethod
    def ok_response(msg: str = 'Operation completed successfully', data: T = None) -> APIResponse[T]:
        return APIResponse(
            status_code=200,
            status_text=Constants.OK_STATUS_TEXT,
            data=data,
            message=msg
        )
        
    @staticmethod
    def bad_request_response(msg: str = 'Invalid request, check your data', data: T = None) -> APIResponse[T]:
        return APIResponse(
            status_code=400,
            status_text=Constants.BAD_REQUEST_TEXT,
            data=data,
            message=msg
        )
    
    @staticmethod
    def created_response(msg: str = 'Resource created successfully', data: T = None) -> APIResponse[T]:
        return APIResponse(
            status_code=201,
            status_text=Constants.CREATED_STATUS_TEXT,
            data=data,
            message=msg
        )
    
    @staticmethod
    def internal_server_error(msg: str = 'Internal server error, contact an administrator', data: T = None) -> APIResponse[T]:
        return APIResponse(
            status_code=500,
            status_text=Constants.INTERNAL_SERVER_TEXT,
            data=data,
            message=msg
        )
    
    @staticmethod
    def not_found_response(msg: str = 'Resource does not exists', data: T = None) -> APIResponse[T]:
        return APIResponse(
            status_code=404,
            status_text=Constants.NOT_FOUND_TEXT,
            data=data,
            message=msg
        )
    
    @staticmethod
    def unatuhorized_response(msg: str = 'Invalid credentials or expired authentication token.', data: T = None) -> APIResponse[T]:
        return APIResponse(
            status_code=401,
            status_text=Constants.UNAUTHORIZED_STATUS_TEXT,
            data=data,
            message=msg
        )
    
    @staticmethod
    def forbidden_response(msg: str = 'You are not authorized to access this resource.', data: T = None) -> APIResponse[T]:
        return APIResponse(
            status_code=403,
            status_text=Constants.FORBIDDEN_STATUS_TEXT,
            data=data,
            message=msg
        )
        
    