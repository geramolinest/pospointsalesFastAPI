from passlib.context import CryptContext


class BCrypt:
    
    __crypto_context: CryptContext
    
    def __new__(cls):
        
        if not hasattr(cls, '_instance'):
            cls._instance = super(BCrypt, cls).__new__(cls)          
            cls._instance.__crypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return cls._instance
    
    def hash_password(self, password: str) -> str:
        return self.__crypto_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.__crypto_context.verify(plain_password, hashed_password)