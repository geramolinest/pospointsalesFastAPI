from fastapi import FastAPI

from infrastructure.persistence import ApplicationDBContext
from infrastructure.adapters.middlewares import GlobalContextRequestMiddleware

from presentation import main_routerv1

from utils import Config
class Server:
    
    __app: FastAPI
    __db_context: ApplicationDBContext

    __config: Config
    
    def __init__(self) -> None:
        #App creation
        self.__app = FastAPI()

        #Config initialization
        self.__config = Config()
        
        #Including routes
        self.__include_routes()
        
        #Database DB Context
        self.__configure_database()

        #Include middlewares to fastapi application
        self.__include_middlewares()
        
    def __include_routes(self) -> None:
        self.__app.include_router(main_routerv1)
        
    def get_app(self) -> FastAPI:
        return self.__app
    
    def __include_middlewares(self) -> None:
        self.__app.add_middleware(GlobalContextRequestMiddleware)
        
    def __configure_database(self) -> None:
        self.__db_context = ApplicationDBContext()
        
    