from fastapi import FastAPI

from infrastructure.persistence import ApplicationDBContext
from presentation import main_routerv1


class Server:
    
    __app: FastAPI
    __db_context: ApplicationDBContext
    
    def __init__(self) -> None:
        self.__app = FastAPI()
        
        #Including routes
        self.__include_routes()
        
        #Database DB Context
        self.__configure_database()
        
    def __include_routes(self) -> None:
        self.__app.include_router(main_routerv1)
        
    def get_app(self) -> FastAPI:
        return self.__app
        
    def __configure_database(self) -> None:
        self.__db_context = ApplicationDBContext() # type: ignore
        
    