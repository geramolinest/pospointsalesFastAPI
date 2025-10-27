from dotenv import dotenv_values

class Config:
    
    __config: dict[str, str | None]
    
    def __new__(cls):
        
        if not hasattr(cls, '_instance'):
           
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.__config = dotenv_values()
            
        return cls._instance
    
    def get_value(self, key: str) -> str | None:
        return self.__config.get(key)
    
    